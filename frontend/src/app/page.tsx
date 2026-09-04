import Link from "next/link";
import { Header } from "@/components/Header";
import { getPosts, featuredImageUrl } from "@/lib/wp";
import { formatFecha } from "@/lib/format";

export default async function HomePage() {
  const posts = await getPosts(20);

  return (
    <>
      <Header />
      <main className="mx-auto w-full max-w-3xl flex-1 px-4 py-10">
        {posts.length === 0 && (
          <p className="text-neutral-500">
            Todavía no hay notas publicadas.
          </p>
        )}
        <ul className="divide-y divide-neutral-200">
          {posts.map((post) => {
            const imagen = featuredImageUrl(post);
            return (
              <li key={post.id} className="py-6 first:pt-0">
                <Link href={`/nota/${post.slug}`} className="group block">
                  {imagen && (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={imagen}
                      alt=""
                      className="mb-3 aspect-video w-full rounded object-cover"
                    />
                  )}
                  <h2
                    className="font-serif text-2xl leading-tight group-hover:underline"
                    dangerouslySetInnerHTML={{ __html: post.title.rendered }}
                  />
                  <p className="mt-1 text-sm text-neutral-500">
                    {formatFecha(post.date)}
                  </p>
                  <div
                    className="mt-2 text-neutral-700 [&_p]:m-0"
                    dangerouslySetInnerHTML={{ __html: post.excerpt.rendered }}
                  />
                </Link>
              </li>
            );
          })}
        </ul>
      </main>
    </>
  );
}
