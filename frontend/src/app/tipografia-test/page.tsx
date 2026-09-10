import { Lora, Literata, Vollkorn } from "next/font/google";

// Página temporal de comparación (ronda 2), borrar cuando se decida. Buscamos
// algo cercano a Spirits Neutral (Latinotype), la serif que usa CT Examiner
// para títulos -- remates muy suaves, casi imperceptibles, pensada
// específicamente para títulos de diario (revival de una old-style de 1912).
// Spirits es paga (Adobe Fonts la incluye con Creative Cloud; si no, hay que
// comprar licencia web a Latinotype). Literata y Vollkorn son gratuitas
// (Google Fonts) y van en la misma familia de old-style suave. Lora queda
// como referencia porque es la que está en producción ahora mismo.

const lora = Lora({ subsets: ["latin"], weight: ["700"] });
const literata = Literata({ subsets: ["latin"], weight: ["700", "900"] });
const vollkorn = Vollkorn({ subsets: ["latin"], weight: ["700", "900"] });

const TITULARES = [
  "El Senado aprobó la ley de mantenimiento de caminos rurales en medio de la primera huelga vial en 40 años",
  "Entre Ríos aceleró sus exportaciones de servicios basados en conocimiento en el primer trimestre",
];

function Bloque({
  nombre,
  detalle,
  className,
}: {
  nombre: string;
  detalle: string;
  className: string;
}) {
  return (
    <section className="border-b border-neutral-300 py-10">
      <p className="mb-4 font-sans text-xs font-bold uppercase tracking-widest text-neutral-500">
        {nombre} — {detalle}
      </p>
      {TITULARES.map((t) => (
        <h2
          key={t}
          className={`${className} mb-4 text-3xl font-bold leading-tight tracking-tight text-neutral-900 sm:text-4xl`}
        >
          {t}
        </h2>
      ))}
    </section>
  );
}

export default function TipografiaTestPage() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-16 sm:px-8">
      <p className="mb-10 font-sans text-sm text-neutral-500">
        Ronda 2: buscando algo cercano a Spirits Neutral (CT Examiner), gratis. Página de trabajo, no forma parte del sitio.
      </p>
      <Bloque nombre="Lora" detalle="actual, en producción" className={lora.className} />
      <Bloque
        nombre="Literata"
        detalle="candidata — TypeTogether, old-style suave, hecha para lectura editorial"
        className={literata.className}
      />
      <Bloque
        nombre="Vollkorn"
        detalle="candidata — old-style muy suave y redondeada"
        className={vollkorn.className}
      />
    </main>
  );
}
