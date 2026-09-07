import Link from "next/link";
import { Header } from "@/components/Header";
import { getPostsParaPortada, featuredImageUrl, categoryName, type WpPost } from "@/lib/wp";
import { mockEconomia, mockBoletinOficial } from "@/lib/mock-posts";

function ItemTexto({ post }: { post: WpPost }) {
  return (
    <li className="border-t border-neutral-300 pt-3 first:border-t-0 first:pt-0">
      <Link href={`/nota/${post.slug}`} className="group block">
        {categoryName(post) && <p className="kicker mb-1">{categoryName(post)}</p>}
        <h3
          className="font-headline text-base font-bold leading-snug transition-colors group-hover:text-neutral-500"
          dangerouslySetInnerHTML={{ __html: post.title.rendered }}
        />
      </Link>
    </li>
  );
}

function ItemConMiniatura({ post }: { post: WpPost }) {
  const imagen = featuredImageUrl(post);
  return (
    <li className="border-t border-neutral-300 pt-3 first:border-t-0 first:pt-0">
      <Link href={`/nota/${post.slug}`} className="group flex gap-3">
        {imagen && (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={imagen} alt="" className="h-16 w-20 shrink-0 object-cover" />
        )}
        <div>
          {categoryName(post) && <p className="kicker mb-1">{categoryName(post)}</p>}
          <h3
            className="font-headline text-base font-bold leading-snug transition-colors group-hover:text-neutral-500"
            dangerouslySetInnerHTML={{ __html: post.title.rendered }}
          />
        </div>
      </Link>
    </li>
  );
}

function Seccion({ titulo, posts }: { titulo: string; posts: WpPost[] }) {
  if (posts.length === 0) return null;
  return (
    <>
      <p className="kicker mt-12 border-t-2 border-neutral-900 pt-2">{titulo}</p>
      <ul className="mt-2 grid grid-cols-2 gap-x-6 gap-y-8 sm:grid-cols-3 lg:grid-cols-4">
        {posts.map((post) => (
          <TarjetaGrilla key={post.id} post={post} />
        ))}
      </ul>
    </>
  );
}

function TarjetaGrilla({ post }: { post: WpPost }) {
  const imagen = featuredImageUrl(post);
  return (
    <li className="border-t border-neutral-300 pt-4">
      <Link href={`/nota/${post.slug}`} className="group block">
        {imagen && (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={imagen} alt="" className="mb-3 aspect-[16/10] w-full object-cover" />
        )}
        {categoryName(post) && <p className="kicker mb-1.5">{categoryName(post)}</p>}
        <h3
          className="font-headline text-lg font-bold leading-tight transition-colors group-hover:text-neutral-500"
          dangerouslySetInnerHTML={{ __html: post.title.rendered }}
        />
      </Link>
    </li>
  );
}

export default async function HomePage() {
  const posts = await getPostsParaPortada();
  const lead = posts[0];
  const columnaIzq = posts.slice(1, 4);
  const columnaDer = posts.slice(4, 7);
  const grilla = posts.slice(7, 15);

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
          <div className="grid grid-cols-1 gap-x-8 gap-y-10 lg:grid-cols-[1fr_1.7fr_1fr]">
            <ul>
              {columnaIzq.map((post) => (
                <ItemTexto key={post.id} post={post} />
              ))}
            </ul>

            <article className="lg:border-x lg:border-neutral-300 lg:px-8">
              <Link href={`/nota/${lead.slug}`} className="group block">
                {(() => {
                  const imagen = featuredImageUrl(lead);
                  return imagen ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={imagen}
                      alt=""
                      className="mb-5 aspect-[16/10] w-full object-cover"
                    />
                  ) : null;
                })()}
                {categoryName(lead) && <p className="kicker mb-2">{categoryName(lead)}</p>}
                <h1
                  className="font-headline text-3xl font-bold leading-[1.08] transition-colors group-hover:text-neutral-500 sm:text-4xl"
                  dangerouslySetInnerHTML={{ __html: lead.title.rendered }}
                />
                <div
                  className="mt-3 text-base leading-snug text-neutral-700 [&_p]:m-0"
                  dangerouslySetInnerHTML={{ __html: lead.excerpt.rendered }}
                />
              </Link>
            </article>

            <ul>
              {columnaDer.map((post) => (
                <ItemConMiniatura key={post.id} post={post} />
              ))}
            </ul>
          </div>
        )}

        {grilla.length > 0 && (
          <>
            <p className="kicker mt-12 border-t-2 border-neutral-900 pt-2">Más noticias</p>
            <ul className="mt-2 grid grid-cols-2 gap-x-6 gap-y-8 sm:grid-cols-3 lg:grid-cols-4">
              {grilla.map((post) => (
                <TarjetaGrilla key={post.id} post={post} />
              ))}
            </ul>
          </>
        )}

        <Seccion titulo="Economía" posts={mockEconomia} />
        <Seccion titulo="Boletín Oficial" posts={mockBoletinOficial} />
      </main>
      <footer className="font-ui border-t border-neutral-300 px-4 py-6 text-center text-xs text-neutral-500 sm:px-8">
        Agencia Entrerriana — Un proyecto editorial de la Fundación para el Desarrollo Entrerriano
      </footer>
    </>
  );
}
