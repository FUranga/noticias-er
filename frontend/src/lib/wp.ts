// Cliente minimo para la REST API de WordPress (backend editorial, nunca
// renderiza el sitio publico -- ver docs/arquitectura-tecnica.md). Solo
// lee posts publicados; no necesita autenticacion.

const WP_URL = process.env.WP_URL;

if (!WP_URL) {
  throw new Error("Falta WP_URL en frontend/.env.local (ver .env.local.example)");
}

export type WpPost = {
  id: number;
  slug: string;
  date: string;
  title: { rendered: string };
  excerpt: { rendered: string };
  content: { rendered: string };
  _embedded?: {
    "wp:featuredmedia"?: Array<{
      source_url: string;
      alt_text: string;
    }>;
    author?: Array<{ name: string }>;
  };
};

async function wpFetch<T>(path: string): Promise<T> {
  const res = await fetch(`${WP_URL}/wp-json/wp/v2${path}`);
  if (!res.ok) {
    throw new Error(`WordPress respondio ${res.status} en ${path}`);
  }
  return res.json();
}

export async function getPosts(perPage = 10): Promise<WpPost[]> {
  return wpFetch<WpPost[]>(`/posts?per_page=${perPage}&_embed`);
}

export async function getPostBySlug(slug: string): Promise<WpPost | null> {
  const posts = await wpFetch<WpPost[]>(`/posts?slug=${encodeURIComponent(slug)}&_embed`);
  return posts[0] ?? null;
}

export function featuredImageUrl(post: WpPost): string | null {
  return post._embedded?.["wp:featuredmedia"]?.[0]?.source_url ?? null;
}

export function authorName(post: WpPost): string | null {
  return post._embedded?.author?.[0]?.name ?? null;
}
