import { notFound } from "next/navigation";
import { Header } from "@/components/Header";
import { getPostBySlug, featuredImageUrl, featuredImageCredit, categoryName } from "@/lib/wp";
import { formatFecha } from "@/lib/format";

type Props = {
  params: Promise<{ slug: string }>;
};

export default async function NotaPage({ params }: Props) {
  const { slug } = await params;
  const post = await getPostBySlug(slug);

  if (!post) {
    notFound();
  }

  const imagen = featuredImageUrl(post);
  const creditoImagen = featuredImageCredit(post);
  const categoria = categoryName(post);

  return (
    <>
      <Header />
      {/* Foto del mismo ancho que la columna de texto -- verificado
          2026-09-07 en wsj.com/nytimes.com con el navegador: en una nota de
          noticia dura (no una feature especial), la foto de apertura mide
          EXACTAMENTE lo mismo que el título y el cuerpo (620px en WSJ,
          600px en NYT, ambos a 1280px de viewport), nunca más ancha. El
          contraste de escala con foto a sangre que se ve en WSJ es un
          tratamiento de feature/aniversario, no el de una nota de wire como
          las nuestras -- se probó ese ancho más grande acá y se descartó
          por no corresponder al género real que redactamos. */}
      <main className="mx-auto w-full max-w-2xl flex-1 px-4 py-10 sm:px-8">
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
      </main>
      <footer className="font-ui border-t border-neutral-300 px-4 py-6 text-center text-xs text-neutral-500 sm:px-8">
        Agencia Entrerriana — Un proyecto editorial de la Fundación para el Desarrollo Entrerriano
      </footer>
    </>
  );
}
