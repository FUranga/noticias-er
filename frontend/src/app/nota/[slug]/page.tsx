import { notFound } from "next/navigation";
import { Header } from "@/components/Header";
import { getPostBySlug, featuredImageUrl, authorName } from "@/lib/wp";
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
  const autor = authorName(post);

  return (
    <>
      <Header />
      <main className="mx-auto w-full max-w-2xl flex-1 px-4 py-10">
        <article>
          <h1
            className="font-serif text-4xl font-semibold leading-tight"
            dangerouslySetInnerHTML={{ __html: post.title.rendered }}
          />
          <p className="mt-3 text-sm text-neutral-500">
            {formatFecha(post.date)}
            {autor ? ` — ${autor}` : ""}
          </p>
          {imagen && (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={imagen}
              alt=""
              className="my-6 w-full rounded object-cover"
            />
          )}
          <div
            className="prose prose-neutral mt-6 max-w-none [&_p]:mb-4 [&_p]:leading-relaxed"
            dangerouslySetInnerHTML={{ __html: post.content.rendered }}
          />
        </article>
      </main>
    </>
  );
}
