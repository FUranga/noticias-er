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

export async function getPostBySlug(slug: string): Promise<WpPost | null> {
  const mock = mockPosts.find((p) => p.slug === slug);
  if (mock) return mock;
  const posts = await wpFetch<WpPost[]>(`/posts?slug=${encodeURIComponent(slug)}&_embed`);
  return posts[0] ?? null;
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

export function categoryName(post: WpPost): string | null {
  const cat = post._embedded?.["wp:term"]?.[0]?.[0];
  return cat && cat.taxonomy === "category" && cat.slug !== "uncategorized" ? cat.name : null;
}

/**
 * Minutos de lectura estimados a partir del cuerpo -- detalle chico que
 * ayuda a que la portada se sienta "viva" (NYT lo muestra junto a la bajada
 * de sus notas destacadas: "4 MIN READ"), no una decoración sin sentido:
 * a ~200 palabras/min, redondeado hacia arriba, mínimo 1.
 */
export function minutosDeLectura(post: WpPost): number {
  const texto = post.content.rendered.replace(/<[^>]+>/g, " ");
  const palabras = texto.split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(palabras / 200));
}

export function categorySlug(post: WpPost): string | null {
  const cat = post._embedded?.["wp:term"]?.[0]?.[0];
  return cat && cat.taxonomy === "category" && cat.slug !== "uncategorized" ? cat.slug : null;
}
