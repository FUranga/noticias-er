# Política de imágenes

Referencia compartida para la skill `procesar-cablera` (que la aplica) y para `pipeline/publicar_borrador.py` (que sube la imagen y su crédito). No la dupliques en la skill — linkeala.

Nota: esto refleja el mejor entendimiento de práctica periodística estándar sobre uso de imágenes, no es asesoría legal formal. Si algún caso puntual genera dudas reales de derechos, mejor consultarlo antes de publicar en vez de asumir.

## Crédito de foto

**Visible, debajo de la imagen destacada** (distinto del sitio de la Fundación, que usa un tooltip escondido en `title` — decisión de Francisco, 2026-09-04, por ser un estándar más propio de un medio de noticias). Formato: `Foto: [fuente]`, por ejemplo:
- `Foto: Gobierno de Entre Ríos`
- `Foto: Cámara de Senadores de Entre Ríos`
- `Foto: [Autor] / Wikimedia Commons, CC BY-SA`

El crédito se guarda como `caption` del media en WordPress (`pipeline/publicar_borrador.py`, tercer argumento) y el frontend lo renderiza (`frontend/src/lib/wp.ts` → `featuredImageCredit`, usado en `frontend/src/app/nota/[slug]/page.tsx`).

## Los tres niveles

Buscar en este orden. Cada nivel exige que el anterior no haya dado un resultado utilizable — no es "elegí el que más te guste", es una cascada de fallback.

### Nivel 1 — foto del propio hecho, de la propia fuente

La foto que el organismo/funcionario publicó sobre el hecho puntual que se está cubriendo. Dos canales:
- **Sitio oficial** — como ya se hace hoy (`skills/procesar-cablera/SKILL.md`, casos `goberer-*` y `senadoer-*`).
- **Redes oficiales** (X/Twitter, Instagram, Facebook) **del organismo o funcionario**, cuando publicaron foto de ese mismo acto/anuncio. Usar el navegador (`claude-in-chrome`) para abrir la cuenta oficial, ubicar la publicación específica del hecho cubierto, y guardar la imagen desde ahí. Registrar el handle y la fecha del posteo para el crédito.

**Por qué es válido**: usar el material de prensa que la propia fuente difundió sobre su propio hecho es práctica estándar de cobertura — es la misma lógica por la que ya se baja la foto de un comunicado.

**Límites**: tiene que ser la foto del hecho puntual que se cubre, no material suelto de la cuenta para usar como banco genérico. Una cuenta oficial del organismo/funcionario sí; una cuenta de un tercero (militante, otro medio, oposición) compartiendo la misma foto, no — hay que rastrear el original.

**Crédito**: `Foto: [Organismo]` (sitio oficial) o `Foto: [Organismo], vía [red social]` (redes).

### Nivel 2 — foto real del lugar/edificio/persona, libre de derechos

Cuando el hecho puntual no tiene foto propia, pero hay un sujeto identificable (un edificio, un lugar, a veces una persona pública con foto disponible bajo licencia libre):
- **Wikimedia Commons** — primera opción. Licencia CC clara y verificable por archivo, ya se usó para la Fundación (foto de Casa de Gobierno).
- **Flickr con filtro de licencia Creative Commons activado** — segunda opción, más variedad de fotógrafos locales, pero hay que revisar la licencia de cada foto puntual (no todo Flickr es libre, el filtro solo acota la búsqueda).

**Crédito**: `Foto: [Autor] / Wikimedia Commons, [licencia]` (ej. `CC BY-SA 4.0`) — siguiendo lo que pida la licencia específica del archivo.

### Nivel 3 — foto de concepto genérica

Cuando no hay nada real aplicable (ej. una nota sobre una cifra macro sin sujeto fotografiable):
- **Banco propio curado** (`data/imagenes/banco-libre/`, ver más abajo) — primera opción, para no partir de cero cada vez y para que las fotos genéricas tengan igual algo de identidad local (paisaje/edificios/agro de la zona) en vez de ser stock global sin relación con Entre Ríos.
- **Unsplash / Pexels vía API** — fallback si el banco propio no tiene nada que sirva. Requiere API key gratuita que tiene que generar Francisco (cuenta de desarrollador) — no implementado todavía. Ambos bancos tienen licencia de uso comercial libre sin atribución obligatoria, pero igual conviene creditar por prolijidad editorial.

**Crédito**: `Foto: [Autor] / Unsplash` o `Foto: [Autor] / Wikimedia Commons, [licencia]` según de dónde salió.

## Banco propio curado (Nivel 3)

`data/imagenes/banco-libre/` — un puñado de fotos reales de la zona (skyline de Paraná, costanera, campo/agro entrerriano, Puente Rosario-Victoria, edificios públicos), bajadas una vez de Wikimedia Commons con su licencia y crédito ya resueltos, para reutilizar como "foto de color" en notas sin sujeto propio.

Cada imagen tiene su entrada en `data/imagenes/banco-libre/manifest.json`:
```json
{
  "archivo": "parana-costanera.jpg",
  "descripcion": "Costanera de Paraná, vista general",
  "fuente_url": "https://commons.wikimedia.org/wiki/File:...",
  "autor": "Nombre del autor",
  "licencia": "CC BY-SA 4.0",
  "credito": "Foto: Nombre del autor / Wikimedia Commons, CC BY-SA 4.0"
}
```

**Todavía no está poblado** (2026-09-04) — construirlo es tarea pendiente, y como es una decisión de gusto/identidad visual del medio, las candidatas se le muestran a Francisco para elegir antes de bajarlas al repo, no se cargan solas.

## Cuando hay varias candidatas

En cualquier nivel, si aparece más de una foto posible (varias fotos en un comunicado, varias del mismo acto en redes, varias opciones de Commons para el mismo edificio): **mostrárselas a Francisco antes de subir el borrador** (con el link o una descripción de cada una) para que elija — no elegir automáticamente por criterio propio. Esto corre en una sesión interactiva con el editor presente (no es automatización headless), así que no hace falta resolverlo sin él.

## Cómo evoluciona este documento

Cuando se agregue el banco propio curado, o se resuelva la key de Unsplash/Pexels, actualizar acá. Si aparece un caso límite de derechos (una foto que no se sabe si se puede usar), documentarlo con el criterio que se termine usando.
