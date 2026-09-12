import Link from "next/link";
import type { WpPost } from "@/lib/wp";

// Extraído de page.tsx (era "MasLeidas", solo vivía en la portada) porque
// ahora se repite también al pie de la nota individual, como el módulo
// "Trending in The Times" de NYT: mismo ranking (getVistas/porPopularidad en
// wp.ts, hoy siempre por fecha hasta que haya vistas reales), mismo
// tratamiento visual en los dos lugares -- a diferencia del "Más noticias"
// de la nota (que es por TEMA), esto es lo más leído del sitio entero.
export function Tendencias({
  posts,
  titulo = "Lo más leído",
}: {
  posts: WpPost[];
  titulo?: string;
}) {
  if (posts.length === 0) return null;
  return (
    <aside className="border-t-2 border-accent pt-2">
      <h2 className="kicker kicker-accent">{titulo}</h2>
      <ol className="mt-3">
        {posts.slice(0, 5).map((post, i) => (
          <li key={post.id} className="flex gap-3 border-t border-neutral-300 py-3 first:border-t-0">
            <span className="font-headline text-2xl font-bold text-neutral-300">{i + 1}</span>
            <Link href={`/nota/${post.slug}`} className="group block">
              <h3
                className="font-headline text-[0.95rem] font-bold leading-snug transition-colors group-hover:text-neutral-500"
                dangerouslySetInnerHTML={{ __html: post.title.rendered }}
              />
            </Link>
          </li>
        ))}
      </ol>
    </aside>
  );
}
