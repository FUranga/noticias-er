// Cliente minimo para la REST API de WordPress (backend editorial, nunca
// renderiza el sitio publico -- ver docs/arquitectura-tecnica.md). Solo
// lee posts publicados; no necesita autenticacion.

import { mockPosts } from "./mock-posts";

const WP_URL = process.env.WP_URL;

if (!WP_URL) {
  throw new Error("Falta WP_URL en frontend/.env.local (ver .env.local.example)");
}

export type WpPost = {
  id: number;
  slug: string;
  date: string;
  sticky: boolean;
  title: { rendered: string };
  excerpt: { rendered: string };
  content: { rendered: string };
  _embedded?: {
    "wp:featuredmedia"?: Array<{
      source_url: string;
      alt_text: string;
      caption: { rendered: string };
    }>;
    author?: Array<{ name: string }>;
    "wp:term"?: Array<Array<{ name: string; slug: string; taxonomy: string }>>;
  };
};

async function wpFetch<T>(path: string): Promise<T> {
  const res = await fetch(`${WP_URL}/wp-json/wp/v2${path}`);
  if (!res.ok) {
    throw new Error(`WordPress respondio ${res.status} en ${path}`);
  }
  return res.json();
}

export async function getPosts(perPage = 10): Promise<WpPost[]> {
  return wpFetch<WpPost[]>(`/posts?per_page=${perPage}&_embed`);
}

/**
 * Trae los posts para la portada, con la nota "fijada" (sticky, marcada por
 * el editor desde WordPress) primero -- sin depender de que sea la mas
 * reciente. Si no hay ninguna fijada, la mas reciente hace de lead.
 */
export async function getPostsParaPortada(perPage = 20): Promise<WpPost[]> {
  const [fijados, recientes] = await Promise.all([
    wpFetch<WpPost[]>(`/posts?sticky=true&per_page=5&_embed`),
    wpFetch<WpPost[]>(`/posts?per_page=${perPage}&_embed`),
  ]);
  const idsFijados = new Set(fijados.map((p) => p.id));
  const reales = [...fijados, ...recientes.filter((p) => !idsFijados.has(p.id))];
  // Contenido de demo (ver mock-posts.ts) va siempre despues de lo real,
  // solo para que la portada no se vea vacia mientras el WordPress real
  // tiene pocas notas -- borrar este concat cuando deje de hacer falta.
  return [...reales, ...mockPosts];
}

// Cache en memoria del mapeo slug->id de categorias dentro de un mismo
// request -- las categorias de posicionamiento (ver mas abajo) se resuelven
// varias veces por render de portada, no hace falta pegarle a la API cada vez.
const categoriaIdPorSlug = new Map<string, number | null>();

async function getCategoryId(slug: string): Promise<number | null> {
  if (categoriaIdPorSlug.has(slug)) return categoriaIdPorSlug.get(slug)!;
  const cats = await wpFetch<Array<{ id: number; slug: string }>>(
    `/categories?slug=${encodeURIComponent(slug)}`
  );
  const id = cats[0]?.id ?? null;
  categoriaIdPorSlug.set(slug, id);
  return id;
}

/**
 * Categorias de POSICIONAMIENTO en el home (Destacadas, Segundas destacadas,
 * Ultimas noticias, Otras noticias) -- ver frontend_estado / conversacion
 * 2026-09-11. Son de uso interno, nunca se muestran al lector (a diferencia
 * de la categoria "tematica" que cada nota tambien puede tener -- Economia,
 * Justicia, etc. -- que hoy no se usa para nada en el layout, queda guardada
 * en WordPress para el dia que haga falta una pagina de seccion por tema).
 *
 * Con sticky-primero igual que getPostsParaPortada, pero acotado a una sola
 * categoria de posicionamiento.
 */
export async function getPostsByCategory(slug: string, perPage = 20): Promise<WpPost[]> {
  const id = await getCategoryId(slug);
  if (id == null) return [];
  const [fijados, recientes] = await Promise.all([
    wpFetch<WpPost[]>(`/posts?categories=${id}&sticky=true&per_page=5&_embed`),
    wpFetch<WpPost[]>(`/posts?categories=${id}&per_page=${perPage}&_embed`),
  ]);
  const idsFijados = new Set(fijados.map((p) => p.id));
  return [...fijados, ...recientes.filter((p) => !idsFijados.has(p.id))];
}

export async function getPostBySlug(slug: string): Promise<WpPost | null> {
  const mock = mockPosts.find((p) => p.slug === slug);
  if (mock) return mock;
  const posts = await wpFetch<WpPost[]>(`/posts?slug=${encodeURIComponent(slug)}&_embed`);
  return posts[0] ?? null;
}

/**
 * Vistas por nota -- señal de popularidad real, para ordenar por lectura
 * efectiva en vez de solo por fecha (ver conversación 2026-09-12: NYT y WSJ
 * combinan tema + recencia CON una señal de lectura real, ver comentario de
 * getPostsRelacionados más abajo).
 *
 * Placeholder DELIBERADO: hoy no hay ninguna fuente de tracking conectada
 * (docs/arquitectura-tecnica.md ya deja dicho que el analytics se maneja acá,
 * en el frontend, y no en WordPress -- pero todavía no se implementó), así
 * que devuelve un Map vacío en vez de inventar un número. Con el Map vacío,
 * getPostsRelacionados() y MasLeidas (page.tsx) caen exactamente al
 * comportamiento actual basado en fecha -- ninguno de los dos necesita
 * volver a tocarse cuando esto deje de estar vacío.
 *
 * Para conectar una fuente real más adelante (a definir con Francisco --
 * candidatas: Vercel Analytics, Umami/Plausible autohosteado, o un contador
 * propio vía Vercel KV incrementado desde la página de la nota), ESTA es la
 * única función a reemplazar.
 */
export async function getVistas(postIds: number[]): Promise<Map<number, number>> {
  void postIds;
  return new Map();
}

/** Reordena por vistas desc si hay datos reales; si el Map viene vacío, deja el orden tal cual llegó (hoy siempre por fecha). */
async function porPopularidad(posts: WpPost[]): Promise<WpPost[]> {
  const vistas = await getVistas(posts.map((p) => p.id));
  if (vistas.size === 0) return posts;
  return [...posts].sort((a, b) => (vistas.get(b.id) ?? 0) - (vistas.get(a.id) ?? 0));
}

/**
 * "Más noticias" al pie de una nota (recirculación). Ubicación verificada
 * 2026-09-12 con el navegador contra nytimes.com/wsj.com: en los dos el
 * módulo va DESPUÉS del cuerpo, nunca antes ni interrumpiendo la lectura.
 *
 * El CRITERIO de selección (no solo la ubicación) también se chequeó, no se
 * asumió: el propio equipo de NYT documenta su recirculación como pooling
 * (armar un conjunto de candidatas por tema/similitud de contenido) ->
 * ranking (por similitud + señales de lectura, ej. más leídas) -> guardrails
 * editoriales. Acá replicamos las tres capas que son honestas con los datos
 * que tenemos: pool por tema (con el mismo patrón "reales primero, relleno
 * después" que conRelleno() en page.tsx si el tema no alcanza), reordenado
 * por vistas reales cuando existan (porPopularidad(), arriba) y por ahora
 * recencia mientras no existan -- nunca una popularidad inventada.
 *
 * Las notas de demo (id negativo, ver mock-posts.ts) no le pegan a WordPress
 * -- se resuelven solo contra el propio pool de mocks.
 */
export async function getPostsRelacionados(post: WpPost, limit = 3): Promise<WpPost[]> {
  if (post.id < 0) {
    const slug = categorySlug(post);
    const resto = mockPosts.filter((p) => p.id !== post.id);
    const mismoTema = resto.filter((p) => categorySlug(p) === slug);
    const otroTema = resto.filter((p) => categorySlug(p) !== slug);
    return porPopularidad([...mismoTema, ...otroTema].slice(0, limit));
  }

  const slug = categorySlug(post);
  let relacionados: WpPost[] = [];
  if (slug) {
    const id = await getCategoryId(slug);
    if (id != null) {
      relacionados = await wpFetch<WpPost[]>(
        `/posts?categories=${id}&exclude=${post.id}&per_page=${limit}&_embed`
      );
      relacionados = await porPopularidad(relacionados);
    }
  }
  if (relacionados.length < limit) {
    const faltan = limit - relacionados.length;
    const excluidos = [post.id, ...relacionados.map((p) => p.id)].join(",");
    const recientes = await wpFetch<WpPost[]>(
      `/posts?exclude=${excluidos}&per_page=${faltan}&_embed`
    );
    relacionados = [...relacionados, ...(await porPopularidad(recientes))];
  }
  return relacionados;
}

/**
 * "Tendencias" -- lo más leído del SITIO ENTERO (a diferencia de
 * getPostsRelacionados, que es por tema de una nota puntual). Es el
 * equivalente honesto al módulo "Trending in The Times" de NYT: no hace
 * falta ninguna página nueva para tenerlo, a diferencia del "Site Index"
 * (sitemap con una columna por sección) del mismo pie de NYT, que si
 * necesita que existan páginas de sección por tema -- hoy no existen (ver
 * comentario de categorySlug más abajo) -- antes de poder construirse sin
 * links muertos.
 */
export async function getTendencias(limit = 5, excluirId?: number): Promise<WpPost[]> {
  let posts = await getPosts(limit + 5);
  if (excluirId != null) posts = posts.filter((p) => p.id !== excluirId);
  if (posts.length < limit) {
    const usados = new Set(posts.map((p) => p.id));
    const relleno = mockPosts.filter((p) => p.id !== excluirId && !usados.has(p.id));
    posts = [...posts, ...relleno];
  }
  return porPopularidad(posts.slice(0, limit));
}

export function featuredImageUrl(post: WpPost): string | null {
  return post._embedded?.["wp:featuredmedia"]?.[0]?.source_url ?? null;
}

/**
 * Credito de la foto destacada (ver docs/politica-imagenes.md) -- viene del
 * campo "caption" del media en WordPress, que publicar_borrador.py completa
 * al subir la imagen. WordPress lo envuelve en <p>, lo sacamos para mostrarlo
 * como una linea de texto simple.
 */
export function featuredImageCredit(post: WpPost): string | null {
  const raw = post._embedded?.["wp:featuredmedia"]?.[0]?.caption?.rendered;
  if (!raw) return null;
  const texto = raw.replace(/<[^>]+>/g, "").trim();
  return texto || null;
}

export function authorName(post: WpPost): string | null {
  return post._embedded?.author?.[0]?.name ?? null;
}

// Categorias de POSICIONAMIENTO en el home (ver page.tsx para el detalle de
// que modulo alimenta cada una) -- centralizadas aca porque categoryName /
// categorySlug necesitan excluirlas: un post puede tener a la vez una
// categoria de posicionamiento (uso interno, nunca visible) y una categoria
// tematica (Economia, Justicia...) que si es la que se muestra en la nota
// individual. Sin este filtro, categoryName podria devolver "Destacadas"
// como si fuera un tema.
export const SLUG_CAT_DESTACADAS = "destacadas";
export const SLUG_CAT_SEGUNDAS_DESTACADAS = "segundas-destacadas";
export const SLUG_CAT_ULTIMAS_NOTICIAS = "ultimas-noticias";
export const SLUG_CAT_OTRAS_NOTICIAS = "otras-noticias";
const SLUGS_CATEGORIA_POSICION = new Set([
  SLUG_CAT_DESTACADAS,
  SLUG_CAT_SEGUNDAS_DESTACADAS,
  SLUG_CAT_ULTIMAS_NOTICIAS,
  SLUG_CAT_OTRAS_NOTICIAS,
]);

function categoriaTematica(post: WpPost) {
  const cats = post._embedded?.["wp:term"]?.[0] ?? [];
  return cats.find(
    (t) =>
      t.taxonomy === "category" &&
      t.slug !== "uncategorized" &&
      !SLUGS_CATEGORIA_POSICION.has(t.slug)
  );
}

export function categoryName(post: WpPost): string | null {
  return categoriaTematica(post)?.name ?? null;
}

// Etiquetas visibles: por default NINGUN tag se muestra en la portada (ver
// conversacion 2026-09-11 -- Francisco no quiere que las tags se vean salvo
// que el decida mostrar una puntual). Esta lista es el unico lugar que
// habilita una tag a mostrarse, mapeando su slug de WordPress al texto que
// se renderiza -- agregar una linea aca es la forma de "activar" una tag
// nueva, nunca se muestran por default ni todas juntas.
const ETIQUETAS_VISIBLES: Record<string, string> = {
  "ultimo-momento": "Último momento",
  "en-vivo": "En vivo",
};

/** true si la nota tiene puesto, a mano, el tag de WordPress con este slug. */
export function tieneTag(post: WpPost, slug: string): boolean {
  const terms = post._embedded?.["wp:term"] ?? [];
  return terms.flat().some((t) => t.taxonomy === "post_tag" && t.slug === slug);
}

/**
 * Primera etiqueta visible que tenga la nota (o null si no tiene ninguna de
 * la lista habilitada) -- una nota puede tener muchos tags de WordPress para
 * uso interno, pero solo los de ETIQUETAS_VISIBLES se renderizan.
 */
export function etiquetaVisible(post: WpPost): string | null {
  const terms = post._embedded?.["wp:term"]?.flat() ?? [];
  for (const t of terms) {
    if (t.taxonomy === "post_tag" && ETIQUETAS_VISIBLES[t.slug]) {
      return ETIQUETAS_VISIBLES[t.slug];
    }
  }
  return null;
}

export function categorySlug(post: WpPost): string | null {
  return categoriaTematica(post)?.slug ?? null;
}
