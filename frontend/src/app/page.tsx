import Link from "next/link";
import { Header } from "@/components/Header";
import {
  getPostsByCategory,
  featuredImageUrl,
  etiquetaVisible,
  SLUG_CAT_DESTACADAS,
  SLUG_CAT_SEGUNDAS_DESTACADAS,
  SLUG_CAT_ULTIMAS_NOTICIAS,
  SLUG_CAT_OTRAS_NOTICIAS,
  type WpPost,
} from "@/lib/wp";
import { mockPosts } from "@/lib/mock-posts";

// Portada inspirada en la estructura real de un diario (NYT/WSJ): tamaños de
// foto y de tipografía variables según jerarquía, no una grilla uniforme
// repetida. Cada bloque de abajo es un "módulo" con su propia relación entre
// una pieza destacada y una lista de acompañamiento -- la variación entre
// módulos es la que da la sensación de portada real, no de feed.

// Categorías de POSICIONAMIENTO (2026-09-11, decisión de Francisco): la
// portada ya no se arma cortando una lista cronológica en pedazos -- cada
// nota tiene una categoría de WordPress que dice en qué módulo va (Destacadas
// / Segundas destacadas / Últimas noticias / Otras noticias). Es un uso
// puramente interno de la categoría, nunca se muestra al lector -- la nota
// también puede tener una segunda categoría temática (Economía, Justicia...)
// que hoy no se usa para nada acá, queda guardada para el día que haga falta
// una página de sección por tema. Slugs centralizados en wp.ts porque
// categoryName/categorySlug también necesitan conocerlos, para no mostrar
// una categoría de posicionamiento como si fuera un tema en la nota individual.

// Relleno de demo mientras las categorías de posicionamiento recién creadas
// no tienen notas reales asignadas (ver mock-posts.ts) -- se completa al
// final de cada lista, nunca reemplaza contenido real. Borrar cuando ya no
// haga falta.
function conRelleno(reales: WpPost[], minimo: number, yaUsados: Set<number>): WpPost[] {
  if (reales.length >= minimo) return reales;
  const relleno = mockPosts.filter((p) => !yaUsados.has(p.id));
  return [...reales, ...relleno];
}

// Nunca es texturized/subrayado -- solo cambia de tamaño según la jerarquía
// del módulo en el que aparece. Ver Etiqueta para el único rótulo que sí se
// muestra (una tag puntual que el editor eligió hacer visible).
function Titular({
  post,
  tamaño = "base",
}: {
  post: WpPost;
  tamaño?: "xl" | "lg" | "base" | "sm" | "xs";
}) {
  const clases = {
    xl: "text-3xl sm:text-4xl leading-[1.05] tracking-tight",
    lg: "text-2xl sm:text-[1.75rem] leading-[1.1] tracking-tight",
    base: "text-lg leading-tight",
    sm: "text-base leading-snug",
    xs: "text-[0.95rem] leading-snug",
  }[tamaño];
  return (
    <h3
      className={`font-headline font-bold transition-colors group-hover:text-neutral-500 ${clases}`}
      dangerouslySetInnerHTML={{ __html: post.title.rendered }}
    />
  );
}

// Único rótulo que se muestra en la portada (2026-09-11): la categoría de
// posicionamiento nunca se ve (ver comentario arriba), y de las tags de
// WordPress solo se rinde la que esté en ETIQUETAS_VISIBLES (wp.ts) -- hoy
// "Último momento" y "En vivo". Agregar una tag nueva a esa lista es la
// única forma de sumar un rótulo visible; nada se muestra por default.
function Etiqueta({ texto }: { texto: string }) {
  return <span className="kicker kicker-accent mr-2 align-middle">{texto}</span>;
}

// Ítem de "río": solo texto, sin foto -- la densidad típica de la columna
// "What's News" del WSJ. El primero de cada lista es levemente más grande,
// como en una portada real (nunca todos los ítems pesan igual), y es el
// único que puede llevar bajada -- en El País y NYT no todos los ítems de
// una lista tienen bajada, pero varios sí, no solo la nota "hero" de toda
// la portada.
function RioItem({ post, destacado = false }: { post: WpPost; destacado?: boolean }) {
  const etiqueta = etiquetaVisible(post);
  return (
    <li className="border-t border-neutral-300 py-3 first:border-t-0 first:pt-0">
      <Link href={`/nota/${post.slug}`} className="group block">
        {etiqueta && <Etiqueta texto={etiqueta} />}
        <Titular post={post} tamaño={destacado ? "base" : "xs"} />
        {destacado && post.excerpt.rendered && (
          <div
            className="mt-1 text-sm leading-snug text-neutral-700 [&_p]:m-0"
            dangerouslySetInnerHTML={{ __html: post.excerpt.rendered }}
          />
        )}
      </Link>
    </li>
  );
}

function Rio({ posts, titulo }: { posts: WpPost[]; titulo?: string }) {
  if (posts.length === 0) return null;
  return (
    <div>
      {titulo && <p className="kicker border-b-2 border-neutral-900 pb-1.5">{titulo}</p>}
      <ul className={titulo ? "mt-1" : ""}>
        {posts.map((post, i) => (
          <RioItem key={post.id} post={post} destacado={i === 0} />
        ))}
      </ul>
    </div>
  );
}

// Siempre es la pieza "destacada" de su módulo (nunca un ítem chico de
// grilla) -- por eso, a diferencia del río, siempre lleva bajada.
function TarjetaFoto({
  post,
  proporcion = "aspect-[3/2]",
  tamañoTitulo = "base",
}: {
  post: WpPost;
  proporcion?: string;
  tamañoTitulo?: "lg" | "base" | "sm";
}) {
  const imagen = featuredImageUrl(post);
  const etiqueta = etiquetaVisible(post);
  return (
    <div>
      <Link href={`/nota/${post.slug}`} className="group block">
        {imagen && (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={imagen} alt="" className={`mb-1.5 w-full object-cover ${proporcion}`} />
        )}
      </Link>
      <Link href={`/nota/${post.slug}`} className="group block">
        {etiqueta && <Etiqueta texto={etiqueta} />}
        <Titular post={post} tamaño={tamañoTitulo} />
        <div
          className="mt-1.5 text-[0.9rem] leading-snug text-neutral-700 [&_p]:m-0"
          dangerouslySetInnerHTML={{ __html: post.excerpt.rendered }}
        />
      </Link>
    </div>
  );
}

function ItemMiniatura({ post }: { post: WpPost }) {
  const imagen = featuredImageUrl(post);
  return (
    <li className="border-t border-neutral-300 py-3 first:border-t-0 first:pt-0">
      <Link href={`/nota/${post.slug}`} className="group flex gap-3">
        {imagen && (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={imagen} alt="" className="h-16 w-20 shrink-0 object-cover" />
        )}
        <Titular post={post} tamaño="xs" />
      </Link>
    </li>
  );
}

// Módulo tipo "sección de diario": una pieza destacada con foto grande a la
// izquierda + un río a la derecha. Sin encabezado de sección (2026-09-11):
// ya no representa un tema (antes decía "Economía"), solo una jerarquía
// visual -- un título ahí ahora sería engañoso. El espaciado (`mt-16`) se
// mantiene para conservar el ritmo entre módulos aunque no haya rótulo.
function SeccionDestacada({
  posts,
  proporcion = "lg:grid-cols-[1.4fr_1fr]",
}: {
  posts: WpPost[];
  proporcion?: string;
}) {
  if (posts.length === 0) return null;
  const [destacada, ...resto] = posts;
  return (
    <section className="mt-16">
      <div className={`grid grid-cols-1 gap-x-10 gap-y-6 ${proporcion}`}>
        <TarjetaFoto post={destacada} tamañoTitulo="lg" />
        {resto.length > 0 && <Rio posts={resto} />}
      </div>
    </section>
  );
}

// Módulo tipo "grilla" -- catch-all de "Otras noticias", sin encabezado por
// el mismo motivo que SeccionDestacada. Relación de columnas 3/2 (no 50/50)
// para que no repita la proporción de las otras secciones.
function SeccionGrilla({ posts }: { posts: WpPost[] }) {
  if (posts.length === 0) return null;
  const [primera, ...resto] = posts;
  return (
    <section className="mt-16">
      <div className="grid grid-cols-1 gap-8 sm:grid-cols-[3fr_2fr]">
        <TarjetaFoto post={primera} proporcion="aspect-[4/3]" tamañoTitulo="base" />
        <ul>
          {resto.map((post) => (
            <RioItem key={post.id} post={post} />
          ))}
        </ul>
      </div>
    </section>
  );
}

function MasLeidas({ posts }: { posts: WpPost[] }) {
  if (posts.length === 0) return null;
  return (
    <aside className="border-t-2 border-accent pt-2">
      <h2 className="kicker kicker-accent">Lo más leído</h2>
      <ol className="mt-3">
        {posts.slice(0, 5).map((post, i) => (
          <li key={post.id} className="flex gap-3 border-t border-neutral-300 py-3 first:border-t-0">
            <span className="font-headline text-2xl font-bold text-neutral-300">{i + 1}</span>
            <Link href={`/nota/${post.slug}`} className="group block">
              <Titular post={post} tamaño="xs" />
            </Link>
          </li>
        ))}
      </ol>
    </aside>
  );
}

function BannerNewsletter() {
  return (
    <div className="my-16 border-y border-neutral-900 bg-neutral-900 px-6 py-7 text-center text-white sm:px-12">
      <p className="font-ui text-xs font-bold uppercase tracking-[0.15em] text-white/60">
        Todos los días, a las 8
      </p>
      <p className="font-headline mt-2 text-2xl font-bold sm:text-3xl">
        Recibí el resumen de las noticias de Entre Ríos
      </p>
      <p className="font-ui mt-2 text-sm text-white/70">
        Un newsletter con lo que se decidió y lo que falta decidir. Sin spam.
      </p>
    </div>
  );
}

export default async function HomePage() {
  const [destacadasReales, segundasReales, ultimasReales, otrasReales] = await Promise.all([
    getPostsByCategory(SLUG_CAT_DESTACADAS),
    getPostsByCategory(SLUG_CAT_SEGUNDAS_DESTACADAS),
    getPostsByCategory(SLUG_CAT_ULTIMAS_NOTICIAS),
    getPostsByCategory(SLUG_CAT_OTRAS_NOTICIAS),
  ]);

  const usados = new Set([
    ...destacadasReales,
    ...segundasReales,
    ...ultimasReales,
    ...otrasReales,
  ].map((p) => p.id));

  const destacadas = conRelleno(destacadasReales, 1, usados);
  const segundasDestacadas = conRelleno(segundasReales, 3, usados);
  const ultimasNoticias = conRelleno(ultimasReales, 8, usados);
  const otrasNoticias = conRelleno(otrasReales, 6, usados);

  const lead = destacadas[0];
  const columnaIzq = ultimasNoticias.slice(0, 4);
  const columnaDer = ultimasNoticias.slice(4, 8);
  const masLeidas = [...ultimasNoticias].reverse().slice(0, 5);

  return (
    <>
      <Header />
      <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-10 sm:px-8">
        {!lead && (
          <p className="font-ui py-16 text-center text-neutral-500">
            Todavía no hay notas publicadas.
          </p>
        )}

        {lead && (
          <div className="grid grid-cols-1 gap-x-10 gap-y-10 lg:grid-cols-[1fr_2fr_1fr]">
            <Rio posts={columnaIzq} titulo="Última hora" />

            {/* Columna central: contenida entre reglas verticales, foto
                discreta (no a sangre) -- el tratamiento clásico de apertura
                de un diario, no un banner de portal de noticias. Sin
                crédito de foto ni autor -- portada despejada, ver notas en
                Titular/TarjetaFoto de más arriba. */}
            <article className="lg:border-x lg:border-neutral-300 lg:px-10">
              <Link href={`/nota/${lead.slug}`} className="group block">
                {(() => {
                  const imagen = featuredImageUrl(lead);
                  return imagen ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img src={imagen} alt="" className="mb-1.5 aspect-[3/2] w-full object-cover" />
                  ) : null;
                })()}
              </Link>
              <Link href={`/nota/${lead.slug}`} className="group block">
                {(() => {
                  const etiqueta = etiquetaVisible(lead);
                  return etiqueta ? <Etiqueta texto={etiqueta} /> : null;
                })()}
                <Titular post={lead} tamaño="xl" />
                <div
                  className="mt-4 max-w-xl text-lg leading-snug text-neutral-700 [&_p]:m-0"
                  dangerouslySetInnerHTML={{ __html: lead.excerpt.rendered }}
                />
              </Link>
            </article>

            <ul>
              {columnaDer.map((post) => (
                <ItemMiniatura key={post.id} post={post} />
              ))}
            </ul>
          </div>
        )}

        <SeccionDestacada posts={segundasDestacadas} proporcion="lg:grid-cols-[2fr_1fr]" />

        <BannerNewsletter />

        <div className="grid grid-cols-1 gap-x-10 lg:grid-cols-[1fr_18rem]">
          <SeccionGrilla posts={otrasNoticias} />
          <div className="mt-16">
            <MasLeidas posts={masLeidas} />
          </div>
        </div>
      </main>
      <footer className="font-ui border-t border-neutral-300 px-4 py-6 text-center text-xs text-neutral-500 sm:px-8">
        Agencia Entrerriana — Un proyecto editorial de la Fundación para el Desarrollo Entrerriano
      </footer>
    </>
  );
}
