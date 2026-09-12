import Link from "next/link";
import { notFound } from "next/navigation";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { Tendencias } from "@/components/Tendencias";
import {
  getPostBySlug,
  getPostsRelacionados,
  getTendencias,
  featuredImageUrl,
  featuredImageCredit,
  categoryName,
  type WpPost,
} from "@/lib/wp";
import { formatFecha } from "@/lib/format";

type Props = {
  params: Promise<{ slug: string }>;
};

// Tarjeta del módulo "Más noticias" (ver más abajo) -- deliberadamente más
// austera que TarjetaFoto de la portada (page.tsx): solo foto, tema y
// título, sin bajada. Verificado 2026-09-12 contra el propio módulo de
// recirculación de nytimes.com (data-testid="recirc-item"): ahí tampoco
// llevan bajada, solo imagen + rótulo + título -- es lo que distingue a un
// ítem de "seguí leyendo" de una pieza de portada real.
function TarjetaRelacionada({ post }: { post: WpPost }) {
  const imagen = featuredImageUrl(post);
  const categoria = categoryName(post);
  return (
    <Link href={`/nota/${post.slug}`} className="group block">
      {imagen && (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={imagen} alt="" className="mb-2 aspect-[3/2] w-full object-cover" />
      )}
      {categoria && <p className="kicker mb-1">{categoria}</p>}
      <h3
        className="font-headline text-base font-bold leading-snug transition-colors group-hover:text-neutral-500"
        dangerouslySetInnerHTML={{ __html: post.title.rendered }}
      />
    </Link>
  );
}

export default async function NotaPage({ params }: Props) {
  const { slug } = await params;
  const post = await getPostBySlug(slug);

  if (!post) {
    notFound();
  }

  const imagen = featuredImageUrl(post);
  const creditoImagen = featuredImageCredit(post);
  const categoria = categoryName(post);
  const [relacionadas, tendencias] = await Promise.all([
    getPostsRelacionados(post),
    getTendencias(5, post.id),
  ]);

  return (
    <>
      <Header />
      <main className="w-full flex-1 px-4 py-10 sm:px-8">
        {/* Foto del mismo ancho que la columna de texto -- verificado
            2026-09-07 en wsj.com/nytimes.com con el navegador: en una nota
            de noticia dura (no una feature especial), la foto de apertura
            mide EXACTAMENTE lo mismo que el título y el cuerpo (620px en
            WSJ, 600px en NYT, ambos a 1280px de viewport), nunca más ancha.
            El contraste de escala con foto a sangre que se ve en WSJ es un
            tratamiento de feature/aniversario, no el de una nota de wire
            como las nuestras -- se probó ese ancho más grande acá y se
            descartó por no corresponder al género real que redactamos. Ese
            ancho (max-w-2xl) vive ahora en un wrapper propio, separado del
            <main>: el bloque de abajo (Más noticias + Tendencias) necesita
            más ancho -- ver comentario ahí. */}
        <div className="mx-auto max-w-2xl">
          <article>
          {categoria && <p className="kicker mb-2">{categoria}</p>}
          {/* Tamaño elegido matemáticamente, no a ojo: medido con canvas
              (actualBoundingBoxAscent/Descent) la relación título:cuerpo en
              tinta real es 1.57:1 en NYT y 2.15:1 en WSJ -- trasladando esas
              proporciones a nuestro cuerpo de 20px (14px de tinta) con la
              métrica de Playfair Display (~0.725 tinta/tamaño-CSS), el
              título "puro NYT" da ~30px y el "puro WSJ" ~41.6px. 33px cae
              un cuarto del camino desde NYT hacia WSJ -- apenas más grande
              que NYT, bastante por debajo del punto medio (36px), que a su
              vez ya había resultado más equilibrado que calcar el número
              nominal de cualquiera de los dos sitios (2026-09-07). */}
          <h1
            className="font-headline text-[1.75rem] font-bold leading-[1.15] sm:text-[2.0625rem]"
            dangerouslySetInnerHTML={{ __html: post.title.rendered }}
          />
          {post.excerpt.rendered && (
            <div
              className="mt-3 text-lg leading-snug text-neutral-700 [&_p]:m-0"
              dangerouslySetInnerHTML={{ __html: post.excerpt.rendered }}
            />
          )}
          {/* Firma fija en "Redacción", no el usuario de WordPress que
              publicó -- toda nota acá sale de reescribir un comunicado en
              estilo agencia, nunca es la voz individual de quien la subió. */}
          <div className="byline mt-4 flex items-center gap-2 border-b border-neutral-300 pb-4">
            <span>Por Redacción</span>
            <span aria-hidden>·</span>
            <span>{formatFecha(post.date)}</span>
          </div>
          {imagen && (
            <figure className="mt-6">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={imagen}
                alt=""
                className="aspect-[16/9] w-full object-cover"
              />
              {creditoImagen && (
                <figcaption className="font-ui mt-1.5 text-xs text-neutral-500">
                  {creditoImagen}
                </figcaption>
              )}
            </figure>
          )}
          {/* text-xl/leading-[1.5] = 20px/30px -- medido en el navegador
              contra nytimes.com: es exactamente el tamaño e interlineado del
              cuerpo de una nota de NYT (WSJ usa 18px, más chico; El País usa
              22px, más grande). El ancho de la columna (max-w-2xl, 672px)
              ya estaba bien calibrado contra los tres -- no hacía falta
              tocarlo, el desajuste era solo de tamaño de letra. */}
          <div
            className="mt-6 text-xl leading-[1.5] text-neutral-900 [&_p]:mb-5"
            dangerouslySetInnerHTML={{ __html: post.content.rendered }}
          />
          </article>
        </div>

        {/* Bloque de abajo (Más noticias + Tendencias): ancho mayor que el
            artículo A PROPÓSITO, verificado 2026-09-12 contra nytimes.com y
            elpais.com -- los dos reservan más marco de página que el ancho
            de lectura y lo usan recién acá, nunca antes (durante la lectura
            ese margen extra queda en blanco en los dos sitios, no es
            desperdicio, es cómo se ve un diario grande). "Más noticias" se
            queda en el mismo ancho que el artículo (42rem/672px) -- así lo
            hace elpais.com ("Más información" mide lo mismo que su columna
            de texto, a diferencia de nytimes.com que sí lo ensancha--
            replicamos la versión más conservadora). "Tendencias" pasa a un
            rail de 18rem/288px al lado, el mismo ancho que ya usa
            SeccionGrilla+Tendencias en la portada (page.tsx) -- no es un
            ancho nuevo, es el mismo patrón ya probado ahí. */}
        {(relacionadas.length > 0 || tendencias.length > 0) && (
          <div className="mx-auto mt-16 max-w-[62.5rem] border-t border-neutral-300 pt-8">
            <div className="grid grid-cols-1 gap-x-10 gap-y-10 lg:grid-cols-[42rem_18rem]">
              {/* "Más noticias": verificado 2026-09-12 contra nytimes.com y
                  wsj.com -- en los dos el recomendador va DESPUÉS del cuerpo,
                  nunca antes ni interrumpiendo la lectura. Prioriza notas
                  del mismo tema (getPostsRelacionados en wp.ts) antes que
                  simplemente "lo más nuevo", y no se muestra si no hay
                  ninguna nota más para ofrecer (sitio recién arrancado). */}
              {relacionadas.length > 0 && (
                <section className="max-w-2xl">
                  <p className="kicker border-b-2 border-neutral-900 pb-1.5">Más noticias</p>
                  <div className="mt-6 grid grid-cols-1 gap-8 sm:grid-cols-3">
                    {relacionadas.map((p) => (
                      <TarjetaRelacionada key={p.id} post={p} />
                    ))}
                  </div>
                </section>
              )}

              {/* "Tendencias": lo más leído del sitio entero, no de esta
                  nota -- ver getTendencias en wp.ts. Es la pieza que falta
                  del pie de NYT/El País ("Trending in The Times"/"Lo más
                  visto") que sí podíamos construir ya, sin páginas nuevas.
                  Lo que queda pendiente es el "Site Index" (sitemap por
                  sección) -- necesita que existan páginas de sección por
                  tema primero, hoy no existen. */}
              <Tendencias posts={tendencias} titulo="Tendencias" />
            </div>
          </div>
        )}
      </main>
      <Footer />
    </>
  );
}
