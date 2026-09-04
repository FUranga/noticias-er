import Link from "next/link";
import { Header } from "@/components/Header";
import { getPosts, featuredImageUrl, categoryName } from "@/lib/wp";
import { formatFecha } from "@/lib/format";

export default async function HomePage() {
  const posts = await getPosts(20);
  const [lead, ...resto] = posts;

  return (
    <>
      <Header />
      <main className="mx-auto w-full max-w-5xl flex-1 px-4 py-10 sm:px-8">
        {!lead && (
          <p className="font-ui py-16 text-center text-neutral-500">
            Todavía no hay notas publicadas.
          </p>
        )}

        {lead && (
          <article className="border-b border-neutral-300 pb-10">
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
              <div className="mx-auto max-w-3xl text-center">
                {categoryName(lead) && <p className="kicker mb-2">{categoryName(lead)}</p>}
                <h1
                  className="font-serif text-4xl font-bold leading-[1.08] group-hover:underline sm:text-5xl"
                  dangerouslySetInnerHTML={{ __html: lead.title.rendered }}
                />
                <div
                  className="mt-4 text-lg leading-snug text-neutral-700 [&_p]:m-0"
                  dangerouslySetInnerHTML={{ __html: lead.excerpt.rendered }}
                />
                <p className="byline mt-4">{formatFecha(lead.date)}</p>
              </div>
            </Link>
          </article>
        )}

        {resto.length > 0 && (
          <ul className="mt-10 grid grid-cols-1 gap-x-10 gap-y-10 sm:grid-cols-2 lg:grid-cols-3">
            {resto.map((post) => {
              const imagen = featuredImageUrl(post);
              return (
                <li key={post.id} className="border-t border-neutral-300 pt-5">
                  <Link href={`/nota/${post.slug}`} className="group block">
                    {imagen && (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img
                        src={imagen}
                        alt=""
                        className="mb-3 aspect-[16/10] w-full object-cover"
                      />
                    )}
                    {categoryName(post) && <p className="kicker mb-1.5">{categoryName(post)}</p>}
                    <h2
                      className="font-serif text-xl font-bold leading-tight group-hover:underline"
                      dangerouslySetInnerHTML={{ __html: post.title.rendered }}
                    />
                    <p className="byline mt-2">{formatFecha(post.date)}</p>
                  </Link>
                </li>
              );
            })}
          </ul>
        )}
      </main>
      <footer className="font-ui border-t border-neutral-300 px-4 py-6 text-center text-xs text-neutral-500 sm:px-8">
        [NOMBRE DEL MEDIO] — Un proyecto editorial de la Fundación para el Desarrollo Entrerriano
      </footer>
    </>
  );
}
