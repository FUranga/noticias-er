import Link from "next/link";
import { Header } from "@/components/Header";
import { getPostsParaPortada, featuredImageUrl, categoryName, type WpPost } from "@/lib/wp";
import { mockEconomia, mockBoletinOficial, mockMunicipios, mockSociedad } from "@/lib/mock-posts";

// Portada inspirada en la estructura real de un diario (NYT/WSJ): tamaños de
// foto y de tipografía variables según jerarquía, no una grilla uniforme
// repetida. Cada bloque de abajo es un "módulo" con su propia relación entre
// una pieza destacada y una lista de acompañamiento -- la variación entre
// módulos es la que da la sensación de portada real, no de feed.

function Titular({
  post,
  tamaño = "base",
}: {
  post: WpPost;
  tamaño?: "base" | "lg" | "sm";
}) {
  const clases = {
    lg: "text-3xl sm:text-4xl leading-[1.05]",
    base: "text-lg leading-tight",
    sm: "text-base leading-snug",
  }[tamaño];
  return (
    <h3
      className={`font-headline font-bold transition-colors group-hover:text-neutral-500 ${clases}`}
      dangerouslySetInnerHTML={{ __html: post.title.rendered }}
    />
  );
}

// Ítem de "río": solo texto, sin foto -- la densidad típica de la columna
// "What's News" del WSJ. Se usa para acompañar a una pieza destacada con foto.
function RioItem({ post }: { post: WpPost }) {
  return (
    <li className="border-t border-neutral-300 py-3 first:border-t-0 first:pt-0">
      <Link href={`/nota/${post.slug}`} className="group block">
        {categoryName(post) && <p className="kicker mb-1">{categoryName(post)}</p>}
        <Titular post={post} tamaño="sm" />
      </Link>
    </li>
  );
}

function TarjetaFoto({
  post,
  proporcion = "aspect-[16/10]",
}: {
  post: WpPost;
  proporcion?: string;
}) {
  const imagen = featuredImageUrl(post);
  return (
    <Link href={`/nota/${post.slug}`} className="group block">
      {imagen && (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={imagen} alt="" className={`mb-3 w-full object-cover ${proporcion}`} />
      )}
      {categoryName(post) && <p className="kicker mb-1.5">{categoryName(post)}</p>}
      <Titular post={post} tamaño="base" />
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
          {categoryName(post) && <p className="kicker mb-1">{categoryName(post)}</p>}
          <Titular post={post} tamaño="sm" />
        </div>
      </Link>
    </li>
  );
}

function EncabezadoSeccion({ titulo }: { titulo: string }) {
  return (
    <div className="mt-16 flex items-center gap-3 border-b-2 border-neutral-900 pb-1.5">
      <h2 className="font-ui text-sm font-bold uppercase tracking-[0.08em]">{titulo}</h2>
      <div className="h-[3px] flex-1 bg-accent/15" />
    </div>
  );
}

// Módulo tipo "sección de diario": una pieza destacada con foto grande a la
// izquierda + una lista de río a la derecha. La proporción entre las dos
// columnas varía por sección para que no todas se vean iguales.
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
        <TarjetaFoto post={destacada} />
        {resto.length > 0 && (
          <ul>
            {resto.map((post) => (
              <RioItem key={post.id} post={post} />
            ))}
          </ul>
        )}
      </div>
    </section>
  );
}

// Módulo tipo "grilla pareja" -- para secciones donde varias notas pesan
// parecido, sin una sola destacada (ej. Municipios: varios hechos locales
// del mismo tamaño de importancia).
function SeccionGrilla({ titulo, posts }: { titulo: string; posts: WpPost[] }) {
  if (posts.length === 0) return null;
  return (
    <section>
      <EncabezadoSeccion titulo={titulo} />
      <ul className="mt-6 grid grid-cols-2 gap-x-6 gap-y-8 sm:grid-cols-4">
        {posts.map((post) => (
          <li key={post.id}>
            <TarjetaFoto post={post} proporcion="aspect-[4/3]" />
          </li>
        ))}
      </ul>
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
      <ul className="mt-4 grid grid-cols-1 gap-x-10 sm:grid-cols-2">
        {posts.map((post) => (
          <RioItem key={post.id} post={post} />
        ))}
      </ul>
    </section>
  );
}

function MasLeidas({ posts }: { posts: WpPost[] }) {
  if (posts.length === 0) return null;
  return (
    <aside className="border-t-2 border-accent pt-2">
      <h2 className="font-ui text-sm font-bold uppercase tracking-[0.08em] text-accent">
        Lo más leído
      </h2>
      <ol className="mt-3">
        {posts.slice(0, 5).map((post, i) => (
          <li key={post.id} className="flex gap-3 border-t border-neutral-300 py-3 first:border-t-0">
            <span className="font-headline text-2xl font-bold text-neutral-300">{i + 1}</span>
            <Link href={`/nota/${post.slug}`} className="group block">
              <Titular post={post} tamaño="sm" />
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
  const rioLateral = posts.slice(1, 7);
  const destacadasSecundarias = posts.slice(7, 9);
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
          <div className="grid grid-cols-1 gap-x-10 gap-y-10 lg:grid-cols-[1fr_20rem]">
            {/* Columna principal: nota de apertura grande + dos secundarias medianas debajo */}
            <div>
              <Link href={`/nota/${lead.slug}`} className="group block">
                {(() => {
                  const imagen = featuredImageUrl(lead);
                  return imagen ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={imagen}
                      alt=""
                      className="mb-5 aspect-[16/9] w-full object-cover"
                    />
                  ) : null;
                })()}
                {categoryName(lead) && <p className="kicker mb-2">{categoryName(lead)}</p>}
                <Titular post={lead} tamaño="lg" />
                <div
                  className="mt-3 max-w-2xl text-lg leading-snug text-neutral-700 [&_p]:m-0"
                  dangerouslySetInnerHTML={{ __html: lead.excerpt.rendered }}
                />
              </Link>

              {destacadasSecundarias.length > 0 && (
                <div className="mt-10 grid grid-cols-1 gap-x-8 gap-y-8 border-t border-neutral-300 pt-8 sm:grid-cols-2">
                  {destacadasSecundarias.map((post) => (
                    <TarjetaFoto key={post.id} post={post} />
                  ))}
                </div>
              )}
            </div>

            {/* Columna lateral: río denso de titulares sin foto, tipo "What's News" */}
            {rioLateral.length > 0 && (
              <div className="lg:border-l lg:border-neutral-300 lg:pl-8">
                <p className="kicker border-b-2 border-neutral-900 pb-1.5">Últimas noticias</p>
                <ul className="mt-1">
                  {rioLateral.map((post) => (
                    <RioItem key={post.id} post={post} />
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        <SeccionDestacada titulo="Economía" posts={mockEconomia} proporcion="lg:grid-cols-[1.5fr_1fr]" />

        <BannerNewsletter />

        <div className="grid grid-cols-1 gap-x-10 lg:grid-cols-[1fr_18rem]">
          <SeccionTexto titulo="Boletín Oficial" posts={mockBoletinOficial} />
          <div className="mt-16">
            <MasLeidas posts={masLeidas} />
          </div>
        </div>

        <SeccionGrilla titulo="Municipios" posts={mockMunicipios} />

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
