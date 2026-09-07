import Link from "next/link";
import { Header } from "@/components/Header";
import {
  getPostsParaPortada,
  featuredImageUrl,
  categoryName,
  categorySlug,
  authorName,
  type WpPost,
} from "@/lib/wp";
import { mockEconomia, mockJusticia, mockMunicipios, mockSociedad } from "@/lib/mock-posts";

// Portada inspirada en la estructura real de un diario (NYT/WSJ): tamaños de
// foto y de tipografía variables según jerarquía, no una grilla uniforme
// repetida. Cada bloque de abajo es un "módulo" con su propia relación entre
// una pieza destacada y una lista de acompañamiento -- la variación entre
// módulos es la que da la sensación de portada real, no de feed.

// Cada sección tiene su propio color de kicker, sutil (como los "flags" de
// color por sección del WSJ) -- no todas las secciones se leen igual.
const KICKER_POR_SECCION: Record<string, string> = {
  economia: "kicker-accent-2",
  justicia: "kicker-accent",
};

function Kicker({ post }: { post: WpPost }) {
  const nombre = categoryName(post);
  if (!nombre) return null;
  const slug = categorySlug(post) ?? "";
  return <p className={`kicker mb-1.5 ${KICKER_POR_SECCION[slug] ?? ""}`}>{nombre}</p>;
}

function Titular({
  post,
  tamaño = "base",
}: {
  post: WpPost;
  tamaño?: "xl" | "lg" | "base" | "sm" | "xs";
}) {
  const clases = {
    xl: "text-4xl sm:text-5xl leading-[1.02] tracking-tight",
    lg: "text-2xl sm:text-[1.75rem] leading-[1.08]",
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

// Ítem de "río": solo texto, sin foto -- la densidad típica de la columna
// "What's News" del WSJ. El primero de cada lista es levemente más grande,
// como en una portada real (nunca todos los ítems pesan igual).
function RioItem({ post, destacado = false }: { post: WpPost; destacado?: boolean }) {
  return (
    <li className="border-t border-neutral-300 py-3 first:border-t-0 first:pt-0">
      <Link href={`/nota/${post.slug}`} className="group block">
        <Kicker post={post} />
        <Titular post={post} tamaño={destacado ? "base" : "xs"} />
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
  return (
    <Link href={`/nota/${post.slug}`} className="group block">
      {imagen && (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={imagen} alt="" className={`mb-3 w-full object-cover ${proporcion}`} />
      )}
      <Kicker post={post} />
      <Titular post={post} tamaño={tamañoTitulo} />
    </Link>
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
        <div>
          <Kicker post={post} />
          <Titular post={post} tamaño="xs" />
        </div>
      </Link>
    </li>
  );
}

function EncabezadoSeccion({ titulo }: { titulo: string }) {
  return (
    <div className="mt-16 flex items-baseline gap-3 border-b-2 border-neutral-900 pb-1.5">
      <h2 className="font-headline text-xl font-bold italic">{titulo}</h2>
      <div className="h-px flex-1 bg-neutral-300" />
    </div>
  );
}

// Módulo tipo "sección de diario": una pieza destacada con foto grande a la
// izquierda + un río a la derecha. La proporción entre columnas varía por
// sección para que no todas se vean iguales.
function SeccionDestacada({
  titulo,
  posts,
  proporcion = "lg:grid-cols-[1.4fr_1fr]",
}: {
  titulo: string;
  posts: WpPost[];
  proporcion?: string;
}) {
  if (posts.length === 0) return null;
  const [destacada, ...resto] = posts;
  return (
    <section>
      <EncabezadoSeccion titulo={titulo} />
      <div className={`mt-6 grid grid-cols-1 gap-x-10 gap-y-6 ${proporcion}`}>
        <TarjetaFoto post={destacada} tamañoTitulo="lg" />
        {resto.length > 0 && <Rio posts={resto} />}
      </div>
    </section>
  );
}

// Módulo tipo "grilla" -- para secciones donde varias notas pesan parecido,
// sin una sola destacada, pero con la primera levemente más grande.
function SeccionGrilla({ titulo, posts }: { titulo: string; posts: WpPost[] }) {
  if (posts.length === 0) return null;
  const [primera, ...resto] = posts;
  return (
    <section>
      <EncabezadoSeccion titulo={titulo} />
      <div className="mt-6 grid grid-cols-1 gap-8 sm:grid-cols-2">
        <TarjetaFoto post={primera} proporcion="aspect-[4/3]" tamañoTitulo="base" />
        <ul className="grid grid-cols-1 gap-x-6 sm:grid-cols-2">
          {resto.map((post) => (
            <RioItem key={post.id} post={post} />
          ))}
        </ul>
      </div>
    </section>
  );
}

// Módulo tipo "solo texto" -- para la sección más chica, sin fotos, imitando
// los bloques de "briefs" de una portada real.
function SeccionTexto({ titulo, posts }: { titulo: string; posts: WpPost[] }) {
  if (posts.length === 0) return null;
  return (
    <section>
      <EncabezadoSeccion titulo={titulo} />
      <div className="mt-4 grid grid-cols-1 gap-x-10 sm:grid-cols-2">
        {posts.map((post, i) => (
          <RioItem key={post.id} post={post} destacado={i === 0} />
        ))}
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
        Recibí el resumen de la agenda institucional de Entre Ríos
      </p>
      <p className="font-ui mt-2 text-sm text-white/70">
        Un newsletter con lo que se decidió y lo que falta decidir. Sin spam.
      </p>
    </div>
  );
}

export default async function HomePage() {
  const posts = await getPostsParaPortada();
  const lead = posts[0];
  const columnaIzq = posts.slice(1, 5);
  const columnaDer = posts.slice(5, 9);
  const masLeidas = [...posts].reverse().slice(0, 5);

  return (
    <>
      <Header />
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-10 sm:px-8">
        {!lead && (
          <p className="font-ui py-16 text-center text-neutral-500">
            Todavía no hay notas publicadas.
          </p>
        )}

        {lead && (
          <div className="grid grid-cols-1 gap-x-10 gap-y-10 lg:grid-cols-[1fr_1.6fr_1fr]">
            <Rio posts={columnaIzq} titulo="Última hora" />

            {/* Columna central: contenida entre reglas verticales, foto
                discreta (no a sangre) -- el tratamiento clásico de apertura
                de un diario, no un banner de portal de noticias. */}
            <article className="lg:border-x lg:border-neutral-300 lg:px-10">
              <Link href={`/nota/${lead.slug}`} className="group block">
                {(() => {
                  const imagen = featuredImageUrl(lead);
                  return imagen ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img src={imagen} alt="" className="mb-5 aspect-[3/2] w-full object-cover" />
                  ) : null;
                })()}
                <Kicker post={lead} />
                <Titular post={lead} tamaño="xl" />
                <div
                  className="mt-4 max-w-xl text-lg leading-snug text-neutral-700 [&_p]:m-0"
                  dangerouslySetInnerHTML={{ __html: lead.excerpt.rendered }}
                />
                {authorName(lead) && (
                  <p className="byline mt-3">Por {authorName(lead)}</p>
                )}
              </Link>
            </article>

            <ul>
              {columnaDer.map((post) => (
                <ItemMiniatura key={post.id} post={post} />
              ))}
            </ul>
          </div>
        )}

        <SeccionDestacada titulo="Economía" posts={mockEconomia} proporcion="lg:grid-cols-[1.5fr_1fr]" />

        <BannerNewsletter />

        <SeccionTexto titulo="Justicia" posts={mockJusticia} />

        <div className="grid grid-cols-1 gap-x-10 lg:grid-cols-[1fr_18rem]">
          <SeccionGrilla titulo="Municipios" posts={mockMunicipios} />
          <div className="mt-16">
            <MasLeidas posts={masLeidas} />
          </div>
        </div>

        {mockSociedad.length > 0 && (
          <section>
            <EncabezadoSeccion titulo="Sociedad" />
            <ul className="mt-2 grid grid-cols-1 gap-x-8 sm:grid-cols-2 lg:grid-cols-3">
              {mockSociedad.map((post) => (
                <ItemMiniatura key={post.id} post={post} />
              ))}
            </ul>
          </section>
        )}
      </main>
      <footer className="font-ui border-t border-neutral-300 px-4 py-6 text-center text-xs text-neutral-500 sm:px-8">
        Agencia Entrerriana — Un proyecto editorial de la Fundación para el Desarrollo Entrerriano
      </footer>
    </>
  );
}
