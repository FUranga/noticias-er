import type { Metadata } from "next";
import { Source_Serif_4, Playfair_Display, Inter } from "next/font/google";
import "./globals.css";

const serif = Source_Serif_4({
  variable: "--font-serif",
  subsets: ["latin"],
});

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
      className={`${serif.variable} ${headline.variable} ${sans.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-white text-neutral-900">{children}</body>
    </html>
  );
}
