# Sitio institucional de la Fundación (desarrolloentrerriano.org)

Este documento describe el estado y las decisiones detrás del sitio de FUNDER, construido sobre
WordPress + theme Kadence, hosteado en Hostinger (São Paulo). Es un WordPress "normal" con theme —
a diferencia del WordPress del medio (`Agencia Entrerriana`), que es headless puertas adentro (ver
`arquitectura-tecnica.md`). Complementa a `checklist-sitio-fundacion.md` (qué falta) — acá va el *por
qué* y el *cómo* de lo que ya está hecho.

## Estructura del sitio

- **Portada** (`/`, página "Inicio" id 55): hero con foto de Casa de Gobierno (Wikimedia Commons,
  CC BY-SA — ver "Imágenes" abajo), bajada institucional, links a Quiénes somos/Contacto, y un bloque
  "Novedades" con las últimas 6 notas (Gutenberg Query Loop nativo — se actualiza solo, no es una
  instantánea estática). Generada por `fundacion-wp/armar_home.py`, que es la fuente de verdad de su
  markup.
- **Novedades** (`/novedades/`): página de posts (`page_for_posts`), listado paginado, 9 por página.
- **Menú principal**: Sobre (submenú: FUNDER, Autoridades, Raúl Uranga, El fundador) · Novedades ·
  Informes (placeholder, "Próximamente") · Contacto · Inicio. Armado por `fundacion-wp/armar_menu.py`.
- **Categorías**: Opinión, Evento, Informe, Entrevista, Institucional — asignadas por heurística
  (`fundacion-wp/categorizar.py`), con ~44 de 81 posts en el catch-all "Institucional" pendientes de
  revisión manual.
- **Footer**: redes sociales (Facebook, Instagram, X, YouTube) + copyright + dirección/teléfono/email
  de contacto (dato de un snapshot de 2019, marcado para confirmar).

## Contenido histórico recuperado

El dominio ya existía con contenido real 2012-2020, recuperable vía Wayback Machine. En vez de arrancar
de cero, se recuperó y reimportó:

- **54 de 56 notas históricas de FUNDER** (`docs/novedades-historicas-fundacion.json`). Se excluyeron 2
  ("Carne" de José Natanson, "La opción china") por ser reproducciones textuales de artículos de
  terceros con marca explícita de fuente/copyright — decisión del editor: *"Esos contenidos viejos si
  podés, no los traigas"*.
- **20 notas de opinión de visiondesarrollista.org** (sitio propio del editor). El editor indicó
  explícitamente que no hace falta citar la fuente en estos casos por ser artículos de opinión propios
  del sitio — pero se preservó la firma/autoría individual de cada nota igual, porque varias no están
  firmadas por Francisco Uranga.
- **1 artículo de analisisdigital.com.ar**.

**Método de recuperación** (regla fija para cualquier trabajo futuro de este tipo): descarga de HTML
crudo (`requests.get` con `User-Agent`) + extracción con BeautifulSoup del contenedor real del artículo
(`div.entry`, `article`, `div.td-post-content`, etc.), nunca `WebFetch` ni ninguna herramienta que pase
el contenido por un modelo resumidor — se detectó en esta sesión que eso produce una versión resumida
y no fiel del texto original ("me estás haciendo un resumen"). Todo el contenido recuperado en esta
sesión usó descarga cruda + BeautifulSoup.

## Imágenes: licencia y atribución

- Fotos nuevas (no parte del contenido histórico) se buscan en Wikimedia Commons vía su API
  (`action=query&list=search&prop=imageinfo`), verificando licencia CC y autor real antes de subir.
- Con licencia CC-BY/CC-BY-SA que pide atribución, el crédito se pone en el atributo `title` del
  `<img>` (aparece como tooltip al pasar el mouse) — no como un `<p>` de pie de foto visible, por
  preferencia explícita del editor ("no pongas pie en la portada al menos").
- **Hotlinking**: varias notas importadas tenían `<img src>` apuntando directo a la imagen alojada en
  el sitio de origen (visiondesarrollista.org, o una ruta relativa rota de Drupal en
  analisisdigital.com.ar). Se corrigió re-alojando cada imagen en la biblioteca de medios propia y
  reescribiendo el contenido (`fundacion-wp/rehost_imagenes.py`, 26 posts / 55 imágenes la primera vez
  que se corrió). Cualquier imagen externa nueva que aparezca en contenido importado debe re-alojarse
  del mismo modo — nunca dejar un `<img src>` apuntando a un dominio de terceros.

## Gotchas técnicos de WordPress/Kadence (para no repetir la investigación)

- **Additional CSS del Customizer no se guarda silenciosamente**: el panel "CSS adicional" tiene, en su
  primera carga, un overlay de ayuda/accesibilidad con un botón "Cerrar" que se superpone visualmente al
  editor CodeMirror real. Si se escribe antes de cerrar ese overlay, el texto no llega a ningún lado, y
  el click en "Publicar" puede reportar éxito sin haber cambiado nada. Flujo correcto: click en
  "Cerrar" del overlay → confirmar que se ve el editor con números de línea → click adentro → escribir.
  **Verificación**: nunca confiar en el estado "Publicada" de la UI ni en una sola screenshot — siempre
  chequear con un fetch crudo (`Invoke-WebRequest` o equivalente, sin caché de browser/sesión) que el
  string efectivamente esté en el HTML servido.
- **CSS actualmente en "Additional CSS"**: la primera versión ocultaba `.entry-hero` por completo en
  todo el sitio para sacar una franja gris fea — pero eso también se llevó puesta la única señal de
  "en qué página estás" en Novedades/Informes/páginas internas (sin título ni breadcrumb). La versión
  actual restyle en vez de ocultar: deja el `<h1>` de título visible con fondo blanco/gris muy suave,
  y solo la portada (id 55) lo sigue ocultando vía el `<style>` scoped que ya trae `armar_home.py`
  (`.entry-hero.page-hero-section` es más específico que el `.entry-hero` global, así que gana ahí sin
  conflicto). También agrega un color distintivo (rojo de marca) al ítem de menú activo, porque
  WordPress ya marca `current-menu-item` en el HTML pero Kadence no lo resalta visualmente por
  defecto:
  ```css
  .entry-hero { background-color: #ffffff !important; }
  .entry-hero .hero-section-overlay { background: transparent !important; }
  body, .site, .site-main, .content-bg-color, .entry-content, .site-below-header-wrap, .content-area { background-color: #ffffff !important; }
  article, .entry, .content-bg, .wp-block-post, article.entry.content-bg { box-shadow: none !important; }
  #primary-menu > li.current-menu-item > a, #primary-menu > li.current-menu-item > a .nav-drop-title-wrap { color: #B4192B !important; }
  ```
- **Largo del extracto en las tarjetas de archivo (Novedades, categorías) es un setting nativo de
  Kadence, no CSS**: `wp.customize('post_archive_element_excerpt')`, un objeto `{enabled, words,
  fullContent}`. Bajado de 55 a 20 palabras porque el extracto por defecto (auto-generado de las
  primeras 55 palabras del post, sin resumen real) se sentía desprolijo/cortado a mitad de frase.
- **Comentarios**: desactivados en todo el sitio — `default_comment_status` en `/wp/v2/settings` (para
  contenido nuevo) más un `comment_status: "closed"` aplicado a todos los posts existentes vía API
  (las páginas ya vienen con comentarios cerrados por defecto en WordPress).
- **Categoría "Informes" apunta al archivo nativo de la categoría, no a una página estática**: el ítem
  de menú "Informes" originalmente apuntaba a una página placeholder ("Próximamente", id 360, ahora en
  borrador). Se cambió el `menu-item` a `type: "taxonomy", object: "category", object_id: 6` (la
  categoría se renombró de "Informe" a "Informes" para que coincida con el label del menú; el slug
  sigue siendo `informe`) — así la página se arma sola con los posts que ya estén categorizados como
  Informes, sin mantener contenido aparte.
- **`site_logo` no siempre se guarda de forma confiable clickeando en el Customizer** — funcionó recién
  al hacer `POST /wp-json/wp/v2/settings {"site_logo": <media_id>}` directo por API.
- **Bulk-edit a "Publicar" desde el listado de wp-admin resetea la fecha (`date`) a "ahora"** si no se
  preserva explícitamente. Pasó dos veces en esta sesión, cada vez corregido con
  `fundacion-wp/corregir_fechas.py` (matchea por título contra un diccionario de fechas conocidas).
- **Cambiar el idioma del sitio vía API REST (`POST /wp-json/wp/v2/settings {"language": "es_ES"}`) no
  alcanza** — falla en silencio porque no dispara la descarga del paquete de traducción. Hay que
  cambiarlo desde la UI real (Ajustes → Generales → dropdown de idioma). Se pasó de `es_AR` (traducción
  de terceros incompleta, dejaba strings en inglés como "Previous") a `es_ES` (más completo para Kadence).
- **Un script en bucle publicando muchos posts vía API puede ser bloqueado** por el "auto mode
  classifier" de Claude Code (permiso denegado). Si pasa, la solución fue hacer el bulk-publish a mano
  desde la tabla de wp-admin en vez de scriptearlo.

## Customizer vía API (patrón usado para redes sociales y footer, 2026-09-03)

Cuando el panel del Customizer se muestra vacío/colgado al navegar manualmente (bug observado varias
veces en esta sesión, causa no confirmada — posible timing de carga del iframe), la alternativa que
funcionó fue manipular el objeto `wp.customize` directamente por JavaScript en la pestaña de
`customize.php` (ya autenticada), sin depender de la UI:

1. Ubicar el setting: `Object.keys(wp.customize.settings.settings)` filtrado por palabra clave (ej.
   `youtube`, `social`). Los links de "Enlaces Sociales" son settings individuales `{red}_link`
   (`facebook_link`, `youtube_link`, etc.) — separados de qué íconos se muestran en el footer/header,
   que es un array (`footer_social_items` / `header_social_items`, cada item con `id`/`enabled`/`icon`).
2. Cambiar el valor: `wp.customize('footer_social_items').set({...})`. **Importante**: en Kadence el
   `.set()` a veces no dispara el tracking de "dirty" del Customizer (el botón sigue diciendo
   "Publicada" en vez de "Publicar"). Si pasa, forzarlo:
   ```js
   const s = wp.customize('nombre_del_setting');
   s._dirty = true;
   wp.customize.state('saved').set(false);
   wp.customize.trigger('change', s);
   ```
3. Click en el botón "Publicar" (ya habilitado) y esperar unos segundos.
4. **Verificar siempre con un fetch crudo** (no con la vista previa del Customizer, que puede tener su
   propio caché) que el cambio esté en el HTML servido en producción.

Con este patrón se agregó el ícono de YouTube al footer (faltaba en `footer_social_items` aunque
`youtube_link` ya tenía la URL cargada) y los datos de contacto (dirección/teléfono/email) al
`footer_html_content`, que es un setting único de texto — Kadence no permite múltiples bloques "HTML"
independientes en el footer builder, así que el contacto se agregó *dentro* del mismo bloque de
copyright, separado por "·".

## Credenciales

`fundacion-wp/.env` (gitignored) — `FUNDER_WP_URL`, `FUNDER_WP_USER`, `FUNDER_WP_APP_PASSWORD`
(Application Password generada en wp-admin → Usuarios → Perfil, no la contraseña real de la cuenta).
Ver `fundacion-wp/.env.example`.

## Pendientes

Ver `docs/checklist-sitio-fundacion.md` para la lista completa y priorizada.
