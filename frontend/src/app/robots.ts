import type { MetadataRoute } from "next";

// Bloqueo total temporal (2026-09-07) -- ver la nota en layout.tsx. Esto NO
// es la estrategia real de docs/seo-geo.md (que decide permitir crawlers de
// IA a propósito, no bloquearlos por reflejo) -- es un candado de "todavía
// no lanzamos", para sacar apenas se decida abrir el sitio de verdad.
export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      disallow: "/",
    },
  };
}
