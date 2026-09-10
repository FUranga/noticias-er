import type { Metadata } from "next";
import { Vollkorn, Inter } from "next/font/google";
import "./globals.css";

// 2026-09-07: se probaron Newsreader (cuerpo) y Domine (títulos) para
// acercarse más a NYT/WSJ; Francisco los vio "infantilizantes" en conjunto.
// Se decidió, mostrando 3 opciones lado a lado (Playfair+Georgia,
// Playfair+Source Serif 4, Bitter+Georgia): mantener Playfair Display en
// los títulos sin cambios, y pasar el cuerpo a Georgia -- variable CSS pura
// en globals.css, no next/font, porque es una fuente de sistema. Georgia es
// literalmente la fuente de reserva que NYT y WSJ declaran en su propio CSS
// (`nyt-imperial, georgia, ...` / `Exchange, Georgia, ...`).
//
// 2026-09-10: Francisco notó que Playfair Display (Didone, alto contraste
// de trazo) se veía "filosa" al lado de las referencias reales -- se midió
// en el navegador (no a ojo) la tipografía de título real de El País
// (MajritTx, propietaria), Texas Tribune (PT Serif) y CT Examiner (Spirits
// Neutral, sans -- descartada porque Francisco pidió mantener serif).
// Se armó /tipografia-test con candidatas lado a lado (Playfair, PT Serif,
// Lora, Source Serif 4, Vollkorn) -- misma familia de contraste moderado
// que las referencias, sin la dureza del Didone. Se probó Lora primero;
// Francisco la cambió por Vollkorn (2026-09-10, "dejemos Vollkorn por
// ahora" -- queda como preferencia provisoria, no cerrada del todo). No
// volver a tocar esto sin repetir la comparación en vivo con Francisco
// mirando.

const headline = Vollkorn({
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
