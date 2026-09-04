import { notFound } from "next/navigation";
import { Header } from "@/components/Header";
import { getPostBySlug, featuredImageUrl, authorName, categoryName } from "@/lib/wp";
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
  const categoria = categoryName(post);

  return (
    <>
      <Header />
      <main className="mx-auto w-full max-w-2xl flex-1 px-4 py-10 sm:px-8">
        <article>
          {categoria && <p className="kicker mb-2">{categoria}</p>}
          <h1
            className="font-serif text-3xl font-bold leading-[1.1] sm:text-4xl"
            dangerouslySetInnerHTML={{ __html: post.title.rendered }}
          />
          <div className="byline mt-4 flex items-center gap-2 border-b border-neutral-300 pb-4">
            {autor && <span>Por {autor}</span>}
            {autor && <span aria-hidden>·</span>}
            <span>{formatFecha(post.date)}</span>
          </div>
          {imagen && (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={imagen}
              alt=""
              className="mt-6 aspect-[16/9] w-full object-cover"
            />
          )}
          <div
            className="mt-6 text-lg leading-relaxed text-neutral-900 [&_p]:mb-5"
            dangerouslySetInnerHTML={{ __html: post.content.rendered }}
          />
        </article>
      </main>
      <footer className="font-ui border-t border-neutral-300 px-4 py-6 text-center text-xs text-neutral-500 sm:px-8">
        [NOMBRE DEL MEDIO] — Un proyecto editorial de la Fundación para el Desarrollo Entrerriano
      </footer>
    </>
  );
}
