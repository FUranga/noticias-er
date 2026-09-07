import Link from "next/link";
import { Header } from "@/components/Header";
import {
  getPostsParaPortada,
  featuredImageUrl,
  categoryName,
  tieneTag,
  type WpPost,
} from "@/lib/wp";
import { mockEconomia, mockJusticia, mockMunicipios, mockSociedad } from "@/lib/mock-posts";

// Portada inspirada en la estructura real de un diario (NYT/WSJ): tamaños de
// foto y de tipografía variables según jerarquía, no una grilla uniforme
// repetida. Cada bloque de abajo es un "módulo" con su propia relación entre
// una pieza destacada y una lista de acompañamiento -- la variación entre
// módulos es la que da la sensación de portada real, no de feed.

// Verificado 2026-09-07 contra nytimes.com y elpais.com, no a ojo (ver
// inspección de fuentes reales): el kicker SIEMPRE es sans chico en
// mayúsculas y tinta casi negra, igual en toda la portada -- no cambia de
// color por sección. Y el titular SIEMPRE es serif en negrita, nunca itálica
// ni sans, sin importar si es la nota principal o un ítem de una línea en
// una lista densa -- lo que varía entre una "nota destacada" y un "brief" es
// el tamaño, nunca la familia tipográfica.
function Kicker({ post, mostrar = true }: { post: WpPost; mostrar?: boolean }) {
  const nombre = categoryName(post);
  if (!nombre || !mostrar) return null;
  return <p className="kicker mb-1.5">{nombre}</p>;
}

// Etiqueta chica de estado -- NO se asigna sola al primer ítem de una lista
// (eso hacía que "Último momento" apareciera en cualquier nota, tuviera o no
// urgencia real, y sumado al kicker de sección quedaba sobrepoblado de
// rótulos). Depende de que el editor le haya puesto a la nota el tag de
// WordPress "ultimo-momento" -- ver tieneTag en wp.ts.
//
// Verificado 2026-09-07 (no había ningún caso "en vivo" real de NYT para
// mirar en el momento, pero sí lo vimos en El País: su etiqueta roja
// "ENCUESTA DE 40DB." era texto rojo sobre blanco, sin caja ni borde --
// mismo tratamiento que un kicker, solo que en rojo. Una caja sólida termina
// leyendo más a cupón de e-commerce que a etiqueta editorial (irónicamente
// había un banner de ofertas con ese estilo exacto al lado, en la misma
// visita a nytimes.com).
function Etiqueta({ texto }: { texto: string }) {
  return <span className="kicker kicker-accent mr-2 align-middle">{texto}</span>;
}

// El crédito de la foto (featuredImageCredit en wp.ts) NO se muestra en la
// portada -- decisión de Francisco (2026-09-07): la portada necesita un
// diseño despejado, y el crédito se ve adentro de la nota (nota/[slug]),
// donde si tiene sentido detenerse a leerlo.
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

// Ítem de "río": solo texto, sin foto -- la densidad típica de la columna
// "What's News" del WSJ. El primero de cada lista es levemente más grande,
// como en una portada real (nunca todos los ítems pesan igual), y es el
// único que puede llevar bajada -- en El País y NYT no todos los ítems de
// una lista tienen bajada, pero varios sí, no solo la nota "hero" de toda
// la portada.
//
// `mostrarCategoria` en false cuando el módulo ya tiene su propio
// EncabezadoSeccion de una sola categoría (ej. "Justicia") -- repetir el
// mismo nombre como kicker en cada ítem de abajo es redundante y es lo que
// hacía sentir la portada "sobreetiquetada". Confirmado 2026-09-07 mirando
// nytimes.com/elpais.com en el navegador: en sus portadas reales el kicker
// de categoría es la excepción (aparece en pocos ítems, casi siempre para
// marcar un quiebre de contexto, como un ítem de Opinión adentro de un río
// de noticias) y no una etiqueta que se repite en todos los ítems de una
// lista ya encabezada por esa categoría.
function RioItem({
  post,
  destacado = false,
  mostrarCategoria = true,
}: {
  post: WpPost;
  destacado?: boolean;
  mostrarCategoria?: boolean;
}) {
  const esUltimoMomento = tieneTag(post, "ultimo-momento");
  return (
    <li className="border-t border-neutral-300 py-3 first:border-t-0 first:pt-0">
      <Link href={`/nota/${post.slug}`} className="group block">
        <Kicker post={post} mostrar={mostrarCategoria} />
        {esUltimoMomento && <Etiqueta texto="Último momento" />}
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

function Rio({
  posts,
  titulo,
  mostrarCategoria = true,
}: {
  posts: WpPost[];
  titulo?: string;
  mostrarCategoria?: boolean;
}) {
  if (posts.length === 0) return null;
  return (
    <div>
      {titulo && <p className="kicker border-b-2 border-neutral-900 pb-1.5">{titulo}</p>}
      <ul className={titulo ? "mt-1" : ""}>
        {posts.map((post, i) => (
          <RioItem key={post.id} post={post} destacado={i === 0} mostrarCategoria={mostrarCategoria} />
        ))}
      </ul>
    </div>
  );
}

// Siempre es la pieza "destacada" de su sección (nunca un ítem chico de
// grilla) -- por eso, a diferencia del río, siempre lleva bajada y tiempo de
// lectura. Es la misma distinción real que ya vimos en NYT: no es que
// "algunas notas tengan bajada al azar", es que la tienen las piezas con
// tratamiento propio, no los brefs.
function TarjetaFoto({
  post,
  proporcion = "aspect-[3/2]",
  tamañoTitulo = "base",
  mostrarCategoria = true,
}: {
  post: WpPost;
  proporcion?: string;
  tamañoTitulo?: "lg" | "base" | "sm";
  mostrarCategoria?: boolean;
}) {
  const imagen = featuredImageUrl(post);
  return (
    <div>
      <Link href={`/nota/${post.slug}`} className="group block">
        {imagen && (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={imagen} alt="" className={`mb-1.5 w-full object-cover ${proporcion}`} />
        )}
      </Link>
      <Link href={`/nota/${post.slug}`} className="group block">
        <Kicker post={post} mostrar={mostrarCategoria} />
        <Titular post={post} tamaño={tamañoTitulo} />
        <div
          className="mt-1.5 text-[0.9rem] leading-snug text-neutral-700 [&_p]:m-0"
          dangerouslySetInnerHTML={{ __html: post.excerpt.rendered }}
        />
      </Link>
    </div>
  );
}

function ItemMiniatura({
  post,
  mostrarCategoria = true,
}: {
  post: WpPost;
  mostrarCategoria?: boolean;
}) {
  const imagen = featuredImageUrl(post);
  return (
    <li className="border-t border-neutral-300 py-3 first:border-t-0 first:pt-0">
      <Link href={`/nota/${post.slug}`} className="group flex gap-3">
        {imagen && (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={imagen} alt="" className="h-16 w-20 shrink-0 object-cover" />
        )}
        <div>
          <Kicker post={post} mostrar={mostrarCategoria} />
          <Titular post={post} tamaño="xs" />
        </div>
      </Link>
    </li>
  );
}

// Nada de itálica ni de una tercera voz tipográfica -- mismo tratamiento que
// el kicker (sans, mayúsculas, negrita, tinta casi negra), solo más grande,
// igual que como NYT/El País marcan una sección dentro de la portada.
function EncabezadoSeccion({ titulo }: { titulo: string }) {
  return (
    <div className="mt-16 border-b-2 border-neutral-900 pb-1.5">
      <h2 className="font-ui text-base font-bold uppercase tracking-[0.04em]">{titulo}</h2>
    </div>
  );
}

// Módulo tipo "sección de diario": una pieza destacada con foto grande a la
// izquierda + un río a la derecha. La proporción entre columnas varía por
// sección para que no todas se vean iguales.
//
// Evaluado y descartado por ahora (2026-09-07, Francisco): módulos con fondo
// tinteado/recuadrado tipo WSJ para separar "otro tipo de contenido" -- no
// aparece así en NYT/WaPo, lee "financiero", y no vamos a tener sección de
// Opinión que lo justifique. Queda pendiente para re-evaluar más adelante,
// no descartado para siempre.
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
        <TarjetaFoto post={destacada} tamañoTitulo="lg" mostrarCategoria={false} />
        {resto.length > 0 && <Rio posts={resto} mostrarCategoria={false} />}
      </div>
    </section>
  );
}

// Módulo tipo "grilla" -- para secciones donde varias notas pesan parecido,
// sin una sola destacada, pero con la primera levemente más grande. Relación
// de columnas 3/2 (no 50/50) para que no repita la proporción de las otras
// secciones -- parte de la variedad de anchos que hace de mosaico, no de
// grilla uniforme.
function SeccionGrilla({ titulo, posts }: { titulo: string; posts: WpPost[] }) {
  if (posts.length === 0) return null;
  const [primera, ...resto] = posts;
  return (
    <section>
      <EncabezadoSeccion titulo={titulo} />
      <div className="mt-6 grid grid-cols-1 gap-8 sm:grid-cols-[3fr_2fr]">
        <TarjetaFoto post={primera} proporcion="aspect-[4/3]" tamañoTitulo="base" mostrarCategoria={false} />
        <ul>
          {resto.map((post) => (
            <RioItem key={post.id} post={post} mostrarCategoria={false} />
          ))}
        </ul>
      </div>
    </section>
  );
}

// Módulo tipo "solo texto" -- para la sección más chica, sin fotos, imitando
// los bloques de "briefs" de una portada real. Tres columnas (no dos, como
// las demás secciones) para que la "pared de texto" se sienta distinta del
// resto, no una repetición del mismo patrón a otra escala.
function SeccionTexto({ titulo, posts }: { titulo: string; posts: WpPost[] }) {
  if (posts.length === 0) return null;
  return (
    <section>
      <EncabezadoSeccion titulo={titulo} />
      <ul className="mt-4 grid grid-cols-1 gap-x-8 sm:grid-cols-3">
        {posts.map((post, i) => (
          <RioItem key={post.id} post={post} destacado={i === 0} mostrarCategoria={false} />
        ))}
      </ul>
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
                <Kicker post={lead} />
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

        <SeccionDestacada titulo="Economía" posts={mockEconomia} proporcion="lg:grid-cols-[2fr_1fr]" />

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
                <ItemMiniatura key={post.id} post={post} mostrarCategoria={false} />
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
