import type { Metadata } from "next";
import { Playfair_Display, Inter } from "next/font/google";
import "./globals.css";

// 2026-09-07: se probaron Newsreader (cuerpo) y Domine (títulos) para
// acercarse más a NYT/WSJ; Francisco los vio "infantilizantes" en conjunto.
// Se decidió, mostrando 3 opciones lado a lado (Playfair+Georgia,
// Playfair+Source Serif 4, Bitter+Georgia): mantener Playfair Display en
// los títulos sin cambios, y pasar el cuerpo a Georgia -- variable CSS pura
// en globals.css, no next/font, porque es una fuente de sistema. Georgia es
// literalmente la fuente de reserva que NYT y WSJ declaran en su propio CSS
// (`nyt-imperial, georgia, ...` / `Exchange, Georgia, ...`). No volver a
// tocar esto sin comparar variantes en vivo con Francisco mirando.

const headline = Playfair_Display({
  variable: "--font-headline",
  subsets: ["latin"],
});

const sans = Inter({
  variable: "--font-sans",
  subsets: ["latin"],
});

// noindex temporal (2026-09-07): esto todavía no es el lanzamiento real --
// tiene notas de demo (ver mock-posts.ts) y no arrancó la estrategia real de
// SEO/GEO de docs/seo-geo.md (que va a permitir explícitamente crawlers de
// IA, no bloquearlos a todos). Sacar este bloque cuando se decida lanzar de
// verdad -- hasta entonces, ningún buscador ni motor de IA debería indexar
// esto, ni siquiera si alguien comparte el link de Vercel por error.
export const metadata: Metadata = {
  title: "Agencia Entrerriana — Noticias de Paraná y la provincia",
  description:
    "Política y economía institucional de Paraná y Entre Ríos. Un proyecto editorial de la Fundación para el Desarrollo Entrerriano.",
  robots: { index: false, follow: false },
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="es"
      className={`${headline.variable} ${sans.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-white text-neutral-900">{children}</body>
    </html>
  );
}
