---
name: procesar-cablera
description: Procesa en lote los ítems de data/backlog.json marcados con estado "a_publicar" (elegidos por el editor en el panel admin/index.html) — para cada uno, redacta la noticia siguiendo docs/estilo-editorial.md, intenta conseguir una imagen, y la sube como borrador a WordPress via pipeline/publicar_borrador.py. Usar cuando el usuario dice "procesá los marcados", "corré la cablera", "procesá el backlog" o similar.
---

# Procesar la cablera (backlog marcado para publicar)

Contexto: `admin/index.html` es el panel donde el editor (Francisco) mira `data/backlog.json` y marca qué comunicados quiere convertir en noticia (estado `a_publicar`). Ese marcado es la decisión editorial de noticiabilidad — no se vuelve a cuestionar acá. Este skill hace el trabajo de después: redactar cada ítem marcado y subirlo a WordPress como borrador, sin publicarlo nunca directamente.

## Proceso

1. **Leer `data/backlog.json`** y filtrar los ítems con `"estado": "a_publicar"`. **Excluir los que tengan `"fuente": "Boletín Oficial de Entre Ríos"`** — esos no están listos para redactar directo: "a publicar" en un ítem del Boletín significa "marcado para investigar" (ver `docs/boletin-oficial-proceso.md`), no "noticiable tal cual viene". Necesitan la skill `investigar-boletin` (todavía no construida) antes de pasar por acá — si aparecen en el lote, señalarlos aparte en el reporte final en vez de redactarlos, para que no se cuelen como si fueran un comunicado de prensa común. Si no queda ningún ítem después de esta exclusión, avisar y no hacer nada más.

2. **Para cada ítem**, en orden:
   1. Si tiene `texto_original`, usarlo como material fuente. Si además tiene `link` y el texto parece incompleto (muy corto, cortado), usar WebFetch sobre el `link` para completar — sin pisar lo que el editor ya haya escrito a mano en `texto_original`.
   2. Redactar siguiendo exactamente las reglas de `docs/estilo-editorial.md` (mismo criterio que la skill `redactar-noticia` — no la dupliques, aplicala). Si el ítem no pasa el filtro de calidad mínimo (sin hecho concreto, sin dato duro), **no lo fuerces**: dejalo con su `estado` en `a_publicar`, anotá el problema en la respuesta final para que el editor decida, y seguí con el resto del lote.
   3. **Conseguir imagen y su crédito** (best-effort, nunca bloqueante) — seguir la cascada de `docs/politica-imagenes.md` (no la dupliques acá, aplicala):
      - Si el ítem ya tiene `imagen_url`, usar esa como Nivel 1 directo.
      - **Nivel 1 — Caso especial `goberer-*` (Gobierno de Entre Ríos)**: el `link` de estos ítems (`portal.entrerios.gov.ar/noticias/<id>`) no carga contenido — es un bug confirmado del sitio de origen (ver `docs/fuentes.md`), no vale la pena intentar WebFetch ahí. Si hace falta la foto, usar el navegador (herramientas `claude-in-chrome`) para abrir `https://portal.entrerios.gov.ar/noticias/` (el listado, no el link del ítem), scrollear hasta el final (las imágenes se montan recién ahí, son de carga diferida) y ubicar la tarjeta cuya URL coincide con el id del ítem — su `img.card-img-top` trae la foto incrustada como `data:image/...;base64,...`. Crédito: `Foto: Gobierno de Entre Ríos`.
      - **Nivel 1 — Caso especial `senadoer-*` (Senado de Entre Ríos)**: no hace falta navegador ni WebFetch. El sitio es WordPress con su API REST habilitada — pedir `https://www.senadoer.gob.ar/wp-json/wp/v2/posts?slug=<slug>&_embed` (el `<slug>` es la parte del `id` del ítem después de `senadoer-`) y tomar `_embedded["wp:featuredmedia"][0].source_url`. Crédito: `Foto: Cámara de Senadores de Entre Ríos`.
      - **Nivel 1 — resto de las fuentes**: si el ítem tiene `link`, traer la página (WebFetch) y buscar la imagen principal — meta tag `og:image` primero, si no hay, la primera imagen grande del cuerpo del artículo.
      - **Nivel 1 — redes oficiales**: si el sitio oficial no trae nada usable, probar la cuenta oficial (X/Instagram/Facebook) del organismo/funcionario con `claude-in-chrome`, buscando la publicación específica del hecho cubierto (no material suelto). Crédito: `Foto: [Organismo], vía [red social]`.
      - **Nivel 2 — si Nivel 1 no dio nada**: buscar en Wikimedia Commons (preferido) o Flickr con filtro CC una foto real del edificio/lugar/persona del hecho. Crédito según la licencia del archivo puntual (ver `docs/politica-imagenes.md`).
      - **Nivel 3 — si Nivel 2 tampoco aplica** (nota sin sujeto fotografiable, ej. una cifra macro): usar `data/imagenes/banco-libre/` si ya tiene algo pertinente (ver su `manifest.json` para el crédito ya resuelto de cada archivo); si no hay banco propio con nada útil, señalarlo en el reporte final en vez de forzar una imagen que no aplica — el fallback de stock (Unsplash/Pexels) todavía no está configurado.
      - **Si hay varias candidatas en cualquier nivel** (varias fotos en un comunicado, varias del mismo acto en redes, varias opciones de Commons): no elegir sola — listarlas en la respuesta final (link o descripción de cada una) para que Francisco elija, y dejar ese ítem sin publicar hasta la próxima corrida con su elección.
      - Si no se encuentra nada con confianza razonable en ningún nivel, seguir sin imagen — no es un bloqueante, no inventar una URL de imagen.
   4. Armar un archivo temporal con el formato que espera `pipeline/publicar_borrador.py`:
      ```
      Título: ...

      Bajada: ...

      [Cuerpo, con la atribución de cada dato tejida adentro]
      ```
      Guardarlo en `pipeline/_tmp_<id>.txt` (este patrón de archivo temporal no se commitea — confirmar que `pipeline/_tmp_*.txt` esté en `.gitignore`, agregarlo si no está).
   5. Correr `python publicar_borrador.py pipeline/_tmp_<id>.txt [imagen] [credito]` (con la imagen y su crédito si se consiguieron) desde la carpeta `pipeline/`. Leer la salida para obtener el id del post y el link de edición.
   6. Borrar el archivo temporal.
   7. **Actualizar `data/backlog.json`**: ese ítem pasa a `"estado": "procesado"`, con `"procesado_el"` en la fecha/hora actual y `"wp_edit_url"` con el link de edición que devolvió el script.

3. **Commitear y pushear** los cambios a `data/backlog.json` en un solo commit al final del lote (no uno por ítem), con mensaje tipo `Cablera: procesados N items (ids: ...)`. Antes de commitear, `git pull` si hace falta — el panel admin escribe directo a GitHub y puede haber cambios ajenos en el medio (mismo chequeo que en los proyectos hermanos: `git fetch origin`, `git status`, y si `origin/main` avanzó, resolver antes de pushear en vez de sobreescribir).

4. **Reportar al final**: cuántos ítems se procesaron con éxito (con su link de borrador en WordPress cada uno), cuáles no pasaron el filtro de calidad (y por qué, para que el editor decida), y cuáles fallaron por un error técnico (ej. WordPress no respondió) — estos últimos quedan con `estado: "a_publicar"` para reintentar, no se marcan como procesados.

## Notas

- Esto es Opción A del pipeline (sin costo de API extra): el "click en publicar" del panel solo marca el ítem — la redacción efectiva pasa por una sesión de Claude Code donde el editor pide explícitamente "procesá la cablera". No hay automatización headless todavía (eso sería la Opción B: un GitHub Action llamando directo a la API de Anthropic, evaluar más adelante si hace falta).
- Nunca se publica un post directamente (`status: publish`) — `publicar_borrador.py` siempre crea `draft`. La revisión y publicación final quedan en manos del editor en WordPress.
- Si `pipeline/.env` no está configurado (falta `WP_URL`/`WP_USER`/`WP_APP_PASSWORD`), avisar y detenerse — no tiene sentido redactar todo el lote para que falle al final.
