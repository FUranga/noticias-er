# CLAUDE.md

Contexto para trabajar en este repo con Claude Code.

## Qué es este proyecto

`Agencia Entrerriana` (nombre todavía provisorio, ver README) es un medio digital en formación para cubrir política y economía institucional de Paraná y Entre Ríos, proyecto de la Fundación para el Desarrollo Entrerriano, editado por Francisco Uranga. Funciona con lógica de agencia: monitorea comunicados de organismos y organizaciones, el editor decide qué es noticiable, un agente de IA lo reescribe en estilo Bloomberg/WSJ, el editor revisa y publica. Contexto completo en `README.md` y `docs/vision-y-etapas.md`.

Estado actual: WordPress del medio (backend privado) instalado; sitio de la Fundación (`desarrolloentrerriano.org`, theme Kadence) construido de punta a punta — ver `docs/sitio-fundacion.md`; pipeline de publicación y cablera (`admin/` + `data/backlog.json`) funcionando de punta a punta pero sin ítems reales cargados todavía; frontend público del medio (Next.js/Vercel) todavía no arrancado. Ver README para el detalle actualizado.

**Importante**: son dos WordPress totalmente separados con credenciales separadas — el del medio (`pipeline/.env`) y el de la Fundación (`fundacion-wp/.env`). No confundir ni reusar credenciales entre uno y otro.

## Reglas de trabajo

- **La decisión de qué es noticia es siempre del editor (Francisco), nunca de la IA.** Ninguna skill de este repo debe decidir sola que algo se publica — como mucho, sugiere o resume para agilizar esa decisión (`evaluar-comunicado`), o reescribe algo ya elegido (`redactar-noticia`).
- **No se publica nada automáticamente.** El resultado de cualquier reescritura es un borrador para revisión editorial, nunca un post final.
- **No inventar datos.** Si falta una cifra, fecha o dato en la fuente original, se señala como faltante — nunca se completa con una suposición, aunque parezca razonable.
- **Atribución explícita siempre que el dato venga de la fuente y no de verificación propia** — es la regla central del estilo editorial de este proyecto (ver `docs/estilo-editorial.md`). Un comunicado de gobierno o de una cámara empresaria está escrito para quedar bien; nuestro trabajo es separar el hecho del relato.
- **No inventar URLs de fuentes.** Al mapear o auditar fuentes (`docs/fuentes.md`, skill `mapear-fuentes`), si no se puede confirmar una URL o un feed RSS con certeza razonable, se marca explícitamente como no confirmado en vez de completar el campo con algo plausible.
- **Fuera de alcance**: deportes, espectáculos, cultura de entretenimiento. Si aparece contenido de estos temas en una fuente monitoreada, no se convierte en nota.
- **Agencia, no repetición**: si el hecho ya está bien cubierto por otro medio (sobre todo uno chico/local), preferir linkear y atribuir antes que reescribir sin aportar nada propio. Ver `docs/vision-y-etapas.md` y `docs/aliados-y-financiamiento.md`.
- **Investigación pesada como fork, no inline.** Una auditoría grande de fuentes (una categoría entera, no un organismo puntual) o una investigación legal/comparada de varias fuentes web genera mucho output intermedio de búsqueda que no hace falta que quede en la conversación principal — solo el resultado final que se vuelca al doc correspondiente. Preferir correrla como fork (`Agent` con `subagent_type: "fork"`) cuando el volumen de WebSearch/WebFetch lo justifique.

## Dónde está cada cosa

- `docs/vision-y-etapas.md` — visión completa y hoja de ruta por etapas. Leer antes de proponer cualquier funcionalidad nueva, para ubicarla en la etapa que corresponde.
- `docs/arquitectura-tecnica.md` — decisión de infraestructura (WordPress + pipeline de agencia propio) y el razonamiento detrás. Leer antes de proponer cambios de stack.
- `docs/estilo-editorial.md` — reglas de redacción compartidas por las skills editoriales. Es la fuente de verdad del estilo; las skills la referencian, no la duplican.
- `docs/politica-imagenes.md` — de dónde sale la foto de cada nota del medio (cascada de niveles: fuente propia/redes oficiales → libres de derechos tipo Wikimedia Commons → banco propio curado/stock genérico) y cómo se acredita (visible, distinto del criterio de la Fundación). Consumida por `procesar-cablera` y `pipeline/publicar_borrador.py`.
- `docs/aliados-y-financiamiento.md` — pensamiento en curso sobre alianzas con otros medios/instituciones y vías de sostenibilidad.
- `docs/fuentes.md` — mapa de organismos y organizaciones a monitorear (provincial, órganos de control, nacional, municipal, privado/sindical/académico, medios). Mantenido con la skill `mapear-fuentes`.
- `docs/acceso-informacion-publica.md` — marco legal (Ley Nacional 27.275, Ley Provincial 11.191, Ley 10.529 de audiencias públicas) para pedidos de acceso a la información pública. Referencia editorial y base del "proyecto paralelo" de acceso a documentos de `docs/vision-y-etapas.md`.
- `docs/calendario-publicaciones.md` — cronograma de publicaciones periódicas predecibles (INDEC, boletines oficiales, rendiciones de cuentas), para monitoreo proactivo además del reactivo.
- `docs/fundacion-agenda-institucional.md` — agenda de reforma institucional para FUNDER (comparativo Entre Ríos vs. Connecticut). Es investigación de la Fundación, no cobertura editorial del medio — no aplica la regla de decisión editorial de arriba.
- `docs/boletin-oficial-proceso.md` — diseño de cómo `pipeline/monitorear_boletin_er.py` filtra y prioriza el Boletín Oficial de ER antes de cargarlo a la cablera, y de qué buscar al triagearlo (consumido por la skill `evaluar-boletin`). Leer antes de tocar ese script o de decidir qué se filtra/prioriza.
- `docs/seo-geo.md` — tema crítico a resolver desde el diseño del frontend (todavía no arrancado): SEO clásico y GEO (que los motores de IA citen al medio como fuente). Leer antes de arrancar el frontend o de tomar decisiones de arquitectura que lo afecten (ej. `robots.txt`, structured data).
- `docs/criterios-noticiabilidad.md` — patrones aprendidos de qué elige publicar el editor. Mantenido con `aprender-noticiabilidad`, consumido por `evaluar-comunicado`.
- `docs/fuentes-datos.md` — registro de fuentes de datos/informes (no de noticias) verificadas para contextualizar cifras en notas económicas, para no repetir la misma búsqueda cada vez.
- `docs/servicios-publicos-tarifas.md` — beat de fondo sobre servicios públicos regulados (energía eléctrica mapeada en profundidad; agua/gas/transporte todavía sin mapear): marco legal, mecanismo de actualización tarifaria, roles Nación/Provincia y preguntas abiertas. Leer antes de escribir sobre tarifas de cualquier servicio, para no repetir la investigación de fondo.
- `docs/impuestos.md` — mismo espíritu que el anterior pero para el sistema tributario (provincial, municipal, coparticipación) — todavía sin investigación de fondo, es agenda de investigación, no base de conocimiento.
- `data/series/` — series de datos históricas descargadas (ej. `exportaciones-sbc.json`), cada una con su propia metodología documentada adentro (fuente, cómo se mide, cómo se extrajo, alcance, periodicidad). Insumo para el "proyecto paralelo" de datos de `docs/vision-y-etapas.md`.
- `data/backlog.json` — la cablera: comunicados candidatos con estado editorial (`pendiente`/`a_publicar`/`descartado`; el Boletín Oficial suma `a_investigar` — ver `docs/boletin-oficial-proceso.md`). No hay estado `procesado`: un ítem ya subido a WordPress se marca con `wp_edit_url`/`procesado_el` sin cambiar de estado. Se edita desde `admin/index.html`, no a mano.
- `data/agenda.json` / `docs/agenda.md` — hechos futuros con fecha (o "próximo paso" sin fecha exacta) mencionados dentro de comunicados: sesiones pendientes, trámites que pasan a otra instancia, eventos programados. Se completa desde `evaluar-comunicado`, independiente de si el comunicado en sí se convierte en nota. Pensado para uso propio de Francisco (newsletter, seguimiento) y como insumo si más adelante se decide una sección pública de agenda.
- `admin/index.html` — panel de curación (noindex, no linkeado públicamente). Escribe directo a GitHub con un PAT guardado en el navegador de quien lo usa.
- `pipeline/publicar_borrador.py` — sube una nota ya redactada (con imagen opcional) a WordPress como `draft`.
- `skills/` — skills de Claude Code para el flujo editorial (`redactar-noticia`, `evaluar-comunicado`, `mapear-fuentes`, `procesar-cablera`, `aprender-noticiabilidad`).
- `docs/sitio-fundacion.md` — estado, decisiones de contenido y gotchas técnicos de WordPress/Kadence del sitio de la Fundación. Leer antes de tocar ese sitio, para no repetir investigación ya hecha (ej. el bug del panel "Additional CSS" del Customizer, o por qué cambiar el idioma vía API no alcanza).
- `fundacion-wp/` — scripts de mantenimiento del sitio de la Fundación (`desarrolloentrerriano.org`). WordPress y credenciales completamente separados del `pipeline/` del medio.
- `docs/prensa-fundacion.md` — contacto de prensa por defecto de FUNDER, reglas de embargo, y estado del listado de periodistas (todavía sin cargar). Lo consume la skill `armar-gacetilla`.
- `skills/armar-gacetilla/` — redacta gacetillas de prensa de FUNDER hacia otros medios (dirección inversa a las skills editoriales del medio: acá FUNDER emite, no recibe). El envío a periodistas todavía no está implementado.

## Reglas de trabajo específicas del sitio de la Fundación

- **Nunca usar `WebFetch` (ni ninguna herramienta que resuma con un modelo secundario) para recuperar contenido histórico o de otros sitios.** Produce versiones resumidas, no fieles al original. Usar siempre descarga de HTML crudo + extracción con BeautifulSoup del contenedor real del artículo. Ver `docs/sitio-fundacion.md`.
- **Cualquier imagen en contenido importado debe alojarse en la biblioteca de medios propia**, nunca quedar apuntando (hotlinking) a un dominio de terceros — usar `fundacion-wp/rehost_imagenes.py` como referencia.
- **Atribución de fotos con licencia CC**: crédito en el atributo `title` del `<img>` (tooltip), no como pie de foto visible, salvo que el editor pida lo contrario.

## Proyecto hermano

`despidos-tracker` (otro repo, no este) usa un patrón similar de curaduría periodística con IA pero para un dominio distinto (despidos/quiebras a nivel nacional) y con otra infraestructura (JSON + GitHub + panel admin propio, sin WordPress). Las skills de ese proyecto sirvieron de punto de partida conceptual para las de acá, pero fueron reescritas por completo — no asumas que las reglas de un proyecto aplican al otro sin chequear `docs/estilo-editorial.md` de este repo primero.
