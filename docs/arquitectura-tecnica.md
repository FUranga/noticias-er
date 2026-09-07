# Arquitectura técnica

## Recomendación: WordPress headless (backend editorial) + frontend a medida + pipeline de agencia propio

No conviene construir un CMS propio desde cero para la etapa 1. La razón no es que sea imposible — es que WordPress ya resuelve, de forma probada, todo lo que no es específico de este proyecto: usuarios y roles, revisiones de artículos, biblioteca de medios, editor de texto (Gutenberg), backups. Reconstruir eso es el uso menos eficiente del tiempo en esta etapa. Lo específico de este proyecto — el motor de agencia (ingesta de comunicados, triage, reescritura con IA) — no vive naturalmente en WordPress y no debería intentar vivir ahí: es una capa separada que le habla a WordPress por API.

**Revisión de esta recomendación (post-lanzamiento del proyecto):** el requisito de margen de edición/diseño real (estética NYT/WSJ/Texas Tribune, formatos de nota propios, sin quedar atado a la lógica de templates de un theme) pesa más que la simplicidad de un theme clásico. Un theme de WordPress, incluso un child theme a medida, sigue siendo pelear contra la lógica de bloques/templates de WP para cualquier diseño que se salga de lo estándar. La solución no es abandonar WordPress — es que **WordPress nunca renderice el sitio público**. Queda puertas adentro, como herramienta de edición únicamente; un frontend a medida se encarga de todo lo que ve el lector.

Un CMS propio (reemplazar WordPress mismo, no solo su rendering) recién se justificaría cuando un módulo futuro (bolsa de trabajo, dashboards de datos) pida algo que ni WordPress ni el frontend a medida resuelven bien — y ahí la respuesta más probable sigue siendo sumar una app separada, no reescribir todo.

### Tres capas separadas

**(a) WordPress — backend editorial únicamente, nunca lo que ve el público**
- Hosting gestionado simple y privado (no expuesto como "el sitio", lo que además reduce superficie de ataque). Con un solo editor y sin equipo de sysadmin, no vale la pena un VPS propio para esto.
- Ahí vivís vos: revisás y editás los borradores que sube el pipeline de agencia, con el editor nativo (Gutenberg), roles, historial de revisiones.
- Plugins base: seguridad y backups, y **REST API con Application Passwords** habilitado — es la puerta de entrada para que (1) el pipeline de agencia cree posts como borrador y (2) el frontend lea el contenido publicado. No hace falta plugin de SEO acá — el SEO se resuelve en el frontend, que es lo que Google efectivamente indexa.

**(b) Frontend a medida — el sitio público, sin restricciones de theme**
- Next.js (o similar), consumiendo la API REST de WordPress. Control total: tipografía, grilla de portada con jerarquía editorial propia, formatos de nota especiales, visualizaciones de datos embebidas — nada limitado por lo que un theme permita.
- Deploy en **Vercel** (nivel gratuito generoso para el tráfico inicial): despliega directo desde este repo de GitHub con cada push, sin necesidad de administrar un servidor para la parte pública. Buen SEO y performance out of the box (SSG/ISR).
- SEO, sitemap, OG tags, analytics: se manejan acá, no en WordPress.
- Esto es más piezas que un WordPress clásico todo-en-uno (dos sistemas para mantener en vez de uno), pero el desarrollo lo hacemos vos y yo con Claude Code — no depende de contratar a alguien aparte — y a cambio el techo de diseño es mucho más alto, que es justamente el requisito no negociable acá.
- Newsletter: evaluar un ESP dedicado (Beehiiv, Mailchimp, o similar) en vez de un plugin de WordPress — mejor entregabilidad y mejores herramientas de crecimiento de lista. Se integra por API o embed desde el frontend.

**(c) Pipeline de agencia — capa propia, en este repo**
No es un CMS, es un flujo de trabajo con soporte de IA. Componentes:
1. **Registro de fuentes** (`docs/fuentes.md`, y eventualmente un `fuentes.json` estructurado): organismos y organizaciones a monitorear, con su URL de prensa/comunicados y feed si existe.
2. **Backlog de comunicados entrantes — "la cablera"** (`data/backlog.json`): un ítem por comunicado/novedad candidata, con estado `pendiente` / `a_publicar` / `descartado` (el Boletín Oficial suma `a_investigar`, ver `docs/boletin-oficial-proceso.md`). No hay un estado `procesado` separado: un ítem ya subido a WordPress se marca con `wp_edit_url`/`procesado_el`, sin cambiar de estado. Al principio se carga a mano (revisando cada portal/RSS, o con ayuda de la skill `mapear-fuentes`); más adelante, automatizable por fuente (RSS reader, scraper liviano) a medida que `fuentes.md` tenga feeds confirmados — no hace falta un scraper sofisticado desde el día uno.
3. **Triage editorial — panel `admin/index.html`**: página estática (no indexada, no linkeada públicamente) que lee y escribe `data/backlog.json` directo contra la API de GitHub (con un Personal Access Token guardado en el navegador de quien lo usa, mismo patrón que el panel del proyecto hermano `despidos-tracker`). Francisco mira los ítems pendientes y decide: **marcar para publicar** o **descartar**. Esta decisión es humana y no se automatiza (ver `CLAUDE.md`) — el panel solo mueve estados, nunca redacta ni publica nada por sí mismo.
4. **Reescritura con IA — skill `procesar-cablera`**: a pedido explícito del editor ("procesá la cablera"), toma los ítems en estado `a_publicar`, aplica la skill `redactar-noticia` (estilo Bloomberg/WSJ, `docs/estilo-editorial.md`) a cada uno, e intenta conseguir una imagen (del propio comunicado si tiene, banco de stock como fallback futuro — no implementado todavía).
5. **Publicación como borrador en WordPress**: `pipeline/publicar_borrador.py` sube cada nota (con imagen si se consiguió) vía REST API como post en estado `draft`, nunca publicado. El ítem del backlog conserva su estado `a_publicar` y se le agrega `wp_edit_url` con el link directo al borrador (marca visual en el panel, no un estado nuevo).
6. **Revisión editorial final**: Francisco edita y publica desde el editor nativo de WordPress.

### Estrategia de ingesta de comunicados — por etapas

El mapeo de `docs/fuentes.md` está creciendo rápido (institucionales, sindicatos, cámaras, y pronto partidos políticos, think tanks, empresas, regulatorio/judicial, medios). Conviene agrupar la estrategia de ingesta **por mecanismo**, no por tipo de organización — es lo que realmente determina el costo de automatizar cada una. Auditoría del 2026-09-03 sobre las 4 fuentes institucionales ya mapeadas (Municipio, Legislatura, Concejo, gobierno provincial): ninguna tiene RSS confirmado, y varias bloquean fetch automatizado directamente (403). Esto vale como señal general: no asumir que scraping es la vía fácil para el resto de la lista tampoco.

**Etapa 1 (arrancar acá) — email de prensa.** La mayoría de organismos, sindicatos, cámaras, partidos y think tanks reparten comunicados por mail a listas de prensa — es el mecanismo más universal: no depende de que el sitio tenga RSS ni de que tolere scraping. Francisco da de alta una casilla dedicada y se inscribe en las listas de prensa de las fuentes ya mapeadas (varias ya tienen contacto de prensa confirmado en `fuentes.md`, ej. prensa@senadoer.gob.ar, prensa@caceper.com.ar). Conexión con la cablera en esta etapa: **manual** — copiar/pegar el comunicado relevante en `admin/index.html`, igual que hoy. Menor esfuerzo de build, y ya resuelve el problema real de los sitios sin RSS.

**Etapa 2 — lectura automática de esa casilla (IMAP) → alta automática en el backlog.** Cuando el volumen lo justifique: un script (`pipeline/leer_comunicados_email.py` o similar) que lea por IMAP los mails nuevos y cree ítems `pendiente` en `data/backlog.json` automáticamente — nunca `a_publicar`, eso sigue siendo criterio editorial exclusivo de Francisco. Agrega una pieza nueva de infraestructura (credenciales de email en `pipeline/.env`, parsing de adjuntos/imágenes, deduplicación de reenvíos). No implementar hasta que la Etapa 1 muestre que el volumen de mails lo justifica.

**Etapa 3 — RSS real donde exista.** Confirmado hasta ahora: solo CAMARCO Entre Ríos. Los medios locales/nacionales (a diferencia de los sitios de gobierno) suelen sí tener RSS — buen mecanismo para el monitoreo de medios (no para reescribir, solo para no perder hechos, ver `docs/estilo-editorial.md`). Bajo costo de automatizar con un feed reader estándar, bajo mantenimiento.

**Etapa 4 (último recurso, caso por caso) — scraping de sitios sin mailing ni RSS.** Reservar para 1-2 fuentes de altísimo valor que no ofrezcan ninguna otra vía. Es lo más frágil (se rompe con cada rediseño del sitio) y lo que más mantenimiento pide — no escalar a toda la lista de `fuentes.md`.

**Boletines oficiales y judicial**: tratarlos aparte de "comunicados de prensa" — suelen tener formato estructurado propio (PDF/HTML tabulado por norma/expediente), no una lista de mail. Categoría ya mapeada (2026-09-06, ver `docs/fuentes.md`, sección "Órganos de control, transparencia y justicia" y "Nacional") pero sin mecanismo de ingesta resuelto todavía — los tres boletines (nacional, provincial, municipal de Paraná) son candidatos de altísimo valor y bajísima cobertura periodística actual, ver `docs/calendario-publicaciones.md` para su periodicidad. Evaluar mecanismo específico (probablemente scraping de PDF/HTML, no RSS) cuando se priorice esta categoría para producción.

**Calendario de publicaciones predecibles**: `docs/calendario-publicaciones.md` reúne las fuentes con fecha o periodicidad conocida (INDEC, rendiciones de cuentas municipales, apertura de sesiones legislativas, memorias del Tribunal de Cuentas) — útil para pasar de monitoreo puramente reactivo a también proactivo (revisar una fuente *antes* de que salga el comunicado que la reempaqueta, en vez de después — ver el caso de las exportaciones de SBC en `docs/criterios-noticiabilidad.md`).

**Actualización (2026-09-03) — Gobierno de Entre Ríos terminó resolviéndose distinto al orden de arriba.** Francisco decidió priorizar confiabilidad/control propio por sobre el mecanismo de menor esfuerzo inicial (ver feedback: "arrancar por RSS o scraping de una fuente de alta calidad, no depender de que un tercero te acepte en una lista"). Investigando el sitio (`portal.entrerios.gov.ar`) con la técnica de revisar el historial de Wayback Machine para encontrar rutas `/api/...` no documentadas, apareció una API JSON pública real con texto completo — más confiable que email o RSS, y sin el costo de mantenimiento de un scraper con navegador. Implementado en `pipeline/monitorear_gobierno_er.py`, corriendo cada 15 min en GitHub Actions. Ver `docs/fuentes.md` (sección "Gobierno provincial") para el detalle completo, incluida la técnica de Wayback Machine — **vale la pena probarla primero en cada fuente de gobierno nueva**, antes de asumir que hace falta email o un scraper con navegador.

Este es el nivel "sin costo extra" del pipeline (Opción A): la redacción ocurre dentro de una sesión de Claude Code, no de forma headless. Una **Opción B** más automatizada — el botón "marcar para publicar" del panel disparando directo un GitHub Action que llama a la API de Anthropic (con costo de uso propio, separado de la suscripción de Claude) y sube el borrador sin que nadie abra Claude Code — queda como evolución futura si el volumen lo justifica.

### Por qué no arrancar con un CMS propio (reemplazar WordPress mismo)
- Autenticación, roles, revisiones y backups son problemas resueltos en WordPress y no aportan nada distintivo a este proyecto si se reconstruyen — la ganancia de control de diseño ya la resuelve el frontend a medida, sin necesidad de tocar el backend.
- El verdadero diferencial de este proyecto (el motor de agencia) es agnóstico del backend de destino — funciona igual publicando en WordPress que en cualquier otro sistema. No hace falta resolver "dónde vive el contenido" para avanzar en "cómo decide qué publicar y cómo lo escribe".
- Si en el futuro WordPress se vuelve una traba real (por ejemplo, para los dashboards de datos de la etapa 2), la solución más probable sigue siendo sumar una app separada integrada, no migrar todo.

## Idea a futuro: Opción C — automatizar también el triage (no solo la redacción)

Anotado para evaluar más adelante, no para implementar ahora: además de automatizar la redacción (Opción B), se podría automatizar la decisión de noticiabilidad en sí — un script llamando a la API de Anthropic con criterios explícitos (ver skill `aprender-noticiabilidad` y `docs/criterios-noticiabilidad.md`) que decida publicar/descartar sin intervención humana en el momento. Técnicamente es una extensión directa de la Opción B, no un cambio de arquitectura.

No es "entrenar un modelo" (no hay fine-tuning) — es afinar por escrito, con el uso real, los criterios que ya hoy `evaluar-comunicado` usa para sugerir. La distinción importante para cuando se evalúe esto: **automatizar hasta "borrador listo en WordPress" es razonable y de bajo riesgo** (un error de más es una nota de más para revisar); **automatizar qué queda realmente en vivo en el sitio sin revisión humana es una decisión de otro nivel** — el costo de un error ahí no es "trabajo de revisión de más", es algo mal publicado con la marca del medio. Recomendación cuando se llegue a este punto: mantener el clic final de publicar en manos humanas incluso con triage y redacción 100% automatizados, y decidir soltarlo (si alguna vez tiene sentido) con datos reales de tasa de acierto, no de entrada.

## Arquitectura de contenido del frontend (2026-09-04)

- **Home**: con control editorial humano, no cronología pura. Implementado con el "sticky post" nativo de WordPress — el editor marca la nota principal desde el checkbox de "fijar" en el editor de WP, sin tocar código. Si no hay ninguna fijada, cae a la más reciente.
- **Categorías y demás páginas de listado**: la idea por defecto es que sean cronológicas (no curadas a mano como la home) — todavía no implementadas.
- **Pendiente de pensar más adelante**: posibles "subportadas" por tema/categoría con su propia curación (no solo un listado cronológico), y si conviene automatizar parcialmente la home usando categorías (ej. "la última de cada categoría principal" como fallback) en vez de depender 100% del sticky manual. No implementar hasta que haya más categorías reales en uso.

## Decidido
- **Hosting**: Hostinger (datacenter São Paulo), una sola cuenta para ambos WordPress (el del medio y el de la Fundación) — más barato que dos cuentas separadas y suficiente para el tráfico esperado en esta etapa.
- **Sitio de la Fundación** (`desarrolloentrerriano.org`): WordPress + theme Kadence, construido de punta a punta. Detalle en `docs/sitio-fundacion.md`.
- **Repositorio de GitHub**: ya creado y en uso — [github.com/FUranga/noticias-er](https://github.com/FUranga/noticias-er) (privado).

## Pendiente de decidir con el usuario
- Nombre de dominio del medio (atado a la decisión de marca/nombre, ver `vision-y-etapas.md`) — el dominio del medio en Hostinger sigue siendo el temporal (`maroon-seahorse-965853.hostingersite.com`).
- Confirmar Next.js + Vercel como stack del frontend, o evaluar alternativas si hay preferencia técnica distinta.
- ESP de newsletter.
- Cuándo pasar de Etapa 1 (casilla de prensa, copiar/pegar manual a la cablera) a Etapa 2 (lectura automática por IMAP) — ver "Estrategia de ingesta de comunicados" arriba. Depende del volumen real una vez que la casilla esté activa.
