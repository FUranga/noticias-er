// Verificado 2026-09-12 contra nytimes.com: el pie real (no el módulo de
// "más noticias" que va arriba de él) es una franja angosta de utilidad --
// nombre del medio, copyright y unos pocos links institucionales en una sola
// línea, sin las columnas de secciones que a veces se confunden con "el
// footer". No sumamos acá links a políticas de privacidad/términos/contacto
// porque esas páginas todavía no existen en el sitio -- un link muerto sería
// peor que no tenerlo (misma lógica que "no inventar URLs" para fuentes,
// aplicada al propio sitio). El único link real disponible hoy es el de la
// Fundación.
export function Footer() {
  const año = new Date().getFullYear();
  return (
    <footer className="font-ui border-t border-neutral-300 px-4 py-6 text-center text-xs text-neutral-500 sm:px-8">
      © {año} Agencia Entrerriana — Un proyecto editorial de la{" "}
      <a
        href="https://desarrolloentrerriano.org"
        className="underline decoration-neutral-300 underline-offset-2 hover:text-neutral-900"
      >
        Fundación para el Desarrollo Entrerriano
      </a>
    </footer>
  );
}
