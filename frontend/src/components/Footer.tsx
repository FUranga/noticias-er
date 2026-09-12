// Verificado 2026-09-12 contra nytimes.com: el pie real (no el módulo de
// "más noticias" que va arriba de él) es una franja angosta de utilidad --
// nombre del medio, copyright y unos pocos links institucionales en una sola
// línea, sin las columnas de secciones que a veces se confunden con "el
// footer". No sumamos acá links a políticas de privacidad/términos/contacto
// porque esas páginas todavía no existen en el sitio -- un link muerto sería
// peor que no tenerlo (misma lógica que "no inventar URLs" para fuentes,
// aplicada al propio sitio). El único link real disponible hoy es el de la
// Fundación.
//
// Frase de misión agregada 2026-09-12 tras mirar Texas Tribune y CT
// Examiner -- medios chicos sin fines de lucro, escala real comparable a
// la nuestra, a diferencia de NYT/El País -- que arrancan su pie con una
// frase de misión editorial ("Our Mission: ...", "Big Questions in Small
// Places") antes que cualquier link. No es texto nuevo inventado: es la
// misma frase que ya usábamos como description de SEO en layout.tsx.
export function Footer() {
  const año = new Date().getFullYear();
  return (
    <footer className="font-ui border-t border-neutral-300 px-4 py-6 text-center sm:px-8">
      <p className="text-sm text-neutral-700">
        Política y economía institucional de Paraná y Entre Ríos.
      </p>
      <p className="mt-2 text-xs text-neutral-500">
        © {año} Agencia Entrerriana — Un proyecto editorial de la{" "}
        <a
          href="https://desarrolloentrerriano.org"
          className="underline decoration-neutral-300 underline-offset-2 hover:text-neutral-900"
        >
          Fundación para el Desarrollo Entrerriano
        </a>
      </p>
    </footer>
  );
}
