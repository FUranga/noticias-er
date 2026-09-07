# Proceso del Boletín Oficial de Entre Ríos

Diseño de cómo se procesa el Boletín Oficial de Entre Ríos para la cablera. Distinto del resto de las fuentes (`docs/fuentes.md`) porque el Boletín no es un puñado de comunicados de prensa por día — es el registro legal completo de la actividad del Estado provincial, ~100 páginas y decenas de normas por edición. La mayoría de eso es ruido administrativo estructural; adentro también está lo que casi nadie mira (ver `docs/fuentes.md`, sección "Órganos de control"). Este documento es la referencia de diseño para `pipeline/monitorear_boletin_er.py` — no la dupliques ahí, referenciala.

## Estructura real de una edición (verificado 2026-09-06 sobre la edición Nº 28.410, 04-09-2026)

Cada edición trae un **índice (SUMARIO)** al inicio con cada norma ya clasificada — tipo, organismo emisor, código, título y página. Eso permite triagear sin leer el cuerpo completo de todo.

**Sección Administrativa**:
- **Leyes** — bajo volumen (4 en la edición de referencia). Siempre potencialmente noticiables.
- **Decretos** (por organismo, ej. Gobernación) — alto volumen (25 en la edición de referencia). La mayoría es administrativo puro: rechazos de recursos individuales, pases a retiro, reconocimientos de pago menores. Mezclados aparecen contrataciones directas vía excepción, convenios entre ministerios, designaciones.
- **Resoluciones** (por organismo, ej. EPRE) — bajo volumen, alto valor (en la edición de referencia: una suba del cuadro tarifario eléctrico).

**Sección Comercial**:
- **Edictos judiciales** (sucesorios, citaciones, usucapión, quiebras, nombres) — avisos legales individuales, prácticamente nunca noticia.
- **Licitaciones de organismos públicos** — objeto, destino, monto, fecha de apertura, todo estructurado. Foco económico directo.
- **Personas jurídicas** (designación de autoridades, transferencia de fondo de comercio, asambleas) — bajo interés general.

## Por qué hace falta un filtro (y por qué es mecánico, no editorial)

Cargar cada edición completa a la cablera (`data/backlog.json`) sin filtrar —como sí se hace con Gobierno ER y Senado ER— la ahogaría: decenas de ítems por día, la enorme mayoría administrativos. El filtro que aplica `monitorear_boletin_er.py` es **mecánico** (por patrón de título/categoría), nunca editorial: no decide qué ES noticia, solo qué tipo de registro estructuralmente nunca tiene esa chance. La decisión de noticiabilidad de lo que sí llega sigue siendo 100% humana, vía `evaluar-comunicado` como cualquier otra fuente.

**Sobre el riesgo de que el filtro tape algo real (pregunta de Francisco, 2026-09-06)**: es un riesgo genuino y no se resuelve con certeza total sin leer cada ítem uno por uno, lo cual anula el propósito del filtro. La mitigación no es "confiar en que nunca hay nada ahí" — es que **nada se pierde en silencio**: todo lo filtrado queda registrado en `data/log_filtro_boletin.jsonl` con su título completo, código y motivo. Ver "Revisión periódica del log" más abajo.

## Qué se filtra y qué no (2026-09-06, calibrado con Francisco)

**Se filtra (no llega a la cablera, sí al log)**:
- Decretos con título que matchea `RECHAZO (RECURSO|RECLAMO|SOLICITUD) INTERPUESTO POR...` — confirma una decisión ya tomada contra una persona, no revela un hecho nuevo. Es la categoría de mayor volumen (11 de 25 decretos en la edición de referencia).
- Toda la Sección Comercial excepto Licitaciones (edictos judiciales, personas jurídicas, y las subcategorías de "organismos públicos" que no son licitaciones) — se descarta **en bloque por categoría**, sin parseo item por item (ver "Fuera de alcance" abajo). Edictos judiciales en particular: Francisco confirmó que nunca importan.

**Nunca se filtra, aunque sea administrativo** (el monto/cargo importa y varía caso a caso): "reconocimiento de pago", "recupero de haberes", "renuncia de...", "pase a retiro de...". Todos llegan a la cablera con prioridad `media`.

**Siempre llega, con prioridad `alta`** (criterio explícito de Francisco, 2026-09-06):
- Licitaciones (todas).
- Resoluciones (todas — hoy solo se vio EPRE, pero el criterio es general: bajo volumen, cualquier organismo).
- Decretos cuyo título contiene "excepción" o "convenio" (contratación directa vía excepción, convenios entre organismos).

**Prioridad `baja`** (llega igual, no se oculta): leyes con patrón protocolar (ciudadano ilustre, beneplácito, adhesión, conmemoración, homenaje) — Francisco: "no me importa", pero el volumen de leyes es tan bajo (4/día) que no vale la pena excluirlas del todo.

**Todo lo demás que sobrevive** (decretos genéricos sin patrón de alta prioridad, ej. designaciones, cambios de categoría de comuna): prioridad `media` — revisar, no priorizado.

## Qué buscar al triagear un ítem que llegó a la cablera (criterios de `evaluar-boletin`)

Documento vivo — se va a ir afinando con el uso, mismo espíritu que `docs/criterios-noticiabilidad.md` (que sigue siendo la referencia de fondo: las cuatro preguntas — noticioso / importante / oportuno / útil o sorprendente — aplican igual acá). Esto es específicamente lo que ayuda a leer un ítem del Boletín, que no viene con un ángulo pre-armado como un comunicado de prensa.

**Diferencia clave con un comunicado**: un comunicado ya dice "esto es lo importante" (aunque haya que descontarle el relato institucional). Un decreto/ley/resolución no dice nada de eso — es texto legal seco. El trabajo de triage acá es primero **traducir** (qué organismo, qué hace concretamente, en una oración sin "considerandos"), y recién después preguntarse si importa.

**Señales de que puede haber ángulo, por tipo**:
- **Decretos**: contratación directa vía excepción (¿por qué se evitó la licitación pública?), convenios entre organismos (¿para qué, con qué plata?), designaciones de funcionarios de peso (no un ascenso de rutina), montos grandes en reconocimientos/recuperos, cualquier cosa que revierta o modifique una norma anterior de forma llamativa.
- **Leyes**: casi siempre ángulo potencial si no es protocolar — pero raramente alcanza para nota directa (ver el caso del Norte Entrerriano abajo). La pregunta clave no es "¿importa?" sino "¿qué se necesita investigar para que esto sea una nota real?".
- **Resoluciones**: cambios de tarifas/cuadros (impacto directo en la gente), aprobaciones que afectan a un sector regulado.
- **Licitaciones**: monto (cuanto más alto, más peso), si el objeto es inusual o llamativo para el organismo que licita, si hay antecedentes de la misma obra/compra en `data/backlog.json` o `docs/temas-a-seguir.md`.

**Señales de que probablemente no hay nada** (más allá de lo que ya filtra el mecanismo): decretos administrativos rutinarios que sobrevivieron el filtro por no matchear el patrón exacto pero son del mismo tipo (ej. una variante de "rechazo" con otra redacción), licitaciones de montos chicos y objetos genéricos (insumos de oficina, mantenimiento de rutina) sin nada que las distinga.

### Foco específico: nombramientos, ceses y renuncias (agregado 2026-09-07, pedido de Francisco)

Los decretos de designación, cese, remoción o aceptación de renuncia son, en general, rutina administrativa (un ascenso escalafonario, un reemplazo interino de bajo nivel) — pero cuando el cargo es de peso político o institucional, son de los ítems con más chance de sorprender de todo el Boletín, porque no suelen venir acompañados de un comunicado de prensa propio. Tratar este tipo de norma con un chequeo explícito, no solo como parte del rótulo genérico "designaciones" en decretos.

**Al triagear un decreto de designación/cese/renuncia, preguntarse específicamente**:
- ¿Qué nivel de cargo es? (ministro/secretario de Estado, presidente de organismo descentralizado o ente autárquico, director general/provincial, juez/fiscal, intendente/interventor — vs. un cargo de planta o escalafonario sin poder de decisión propio).
- ¿Es una designación nueva, un reemplazo, o una salida (renuncia/cese/remoción)? Una salida de un cargo de peso es al menos tan noticiable como una llegada, y a veces más (puede señalar un conflicto interno no anunciado).
- ¿El decreto da el motivo, o solo dice "acéptase la renuncia presentada por..." sin explicar por qué? La ausencia de motivo en un cargo de peso es en sí una señal a investigar, no algo que se pueda dar por rutina.
- ¿Hay antecedentes de esa persona o de conflicto en ese organismo en `data/backlog.json` o `docs/temas-a-seguir.md`?

**Calibración de expectativas (Francisco, 2026-09-07)**: la mayoría de las veces, si el nombramiento es de un cargo realmente importante, el editor ya se va a haber enterado por otra vía antes de que el Boletín lo confirme — el valor de este chequeo es la excepción, no la regla: la designación o salida de peso que pasó sin anuncio propio y que el Boletín es la primera confirmación pública. No forzar ángulo en designaciones de rutina solo por tratarse de esta categoría.

**Cómo se sigue mejorando esto**: cuando Francisco descarte o marque "a investigar" un ítem del Boletín y el motivo no esté ya cubierto acá, sumarlo a esta sección con el caso concreto (mismo criterio que el resto del proyecto: nunca una regla sin el ejemplo real detrás).

**Sobre registrar fechas de licitaciones en `data/agenda.json` (Francisco, 2026-09-07)**: no cargar mecánicamente la fecha de apertura de cada licitación que llega al Boletín solo por venir tageada `prioridad: alta` — la mayoría son montos y objetos rutinarios (un municipio comprando un vehículo, materiales de obra, un cartel) sin ninguna chance real de convertirse en seguimiento editorial, y cargarlas todas es ruido que no aporta al propósito de `agenda.json` (uso propio de Francisco / futuro newsletter). Reservar la carga a agenda para una licitación puntual que ya tenga algo que la distinga (monto fuera de lo común para el organismo, objeto inusual, o que el editor haya marcado el ítem "a investigar").

## Ejemplo real de por qué esto importa: la ley del "Norte Entrerriano"

En la edición de referencia apareció la Ley Nº 11.303, creando un marco institucional de desarrollo para el Norte Entrerriano — real interés editorial (Francisco, 2026-09-06), pero **no es una nota que se redacte directo del decreto**: el boletín solo da el texto sancionado, sin el contexto de cómo se llegó a esa ley, quién la impulsó, si hubo polémica u opiniones encontradas. Este es el caso general de por qué una norma del Boletín necesita investigación antes de convertirse en nota, a diferencia de un comunicado de prensa que ya viene con el ángulo armado — ver "Qué sigue" más abajo.

## Mecanismo técnico (resumen — ver `pipeline/monitorear_boletin_er.py` para el detalle)

1. Índice de ediciones: `https://testing54.entrerios.gov.ar/boletin/factura/inicio/get_buscador` (JSON sin auth, `{nro, fecha, nro_anual}` por edición).
2. PDF de cada edición: `https://www.entrerios.gov.ar/boletin/calendario/Boletin/{Año}/{Mes en español}/{DD-MM-AA}.pdf`.
3. Extracción de texto con `pypdf` (sin OCR, el PDF tiene texto real).
4. El SUMARIO administrativo se parsea con una máquina de estados (categoría → organismo → código → título multilínea → página); el cuerpo de cada norma se ubica buscando su código más adelante en el texto (con tolerancia a espacios sueltos que mete la extracción por kerning, ej. "DTO-2026-2302-E-GER -GOB").
5. Licitaciones (Sección Comercial) se separan por el patrón de cierre `ID:NNNNN - ... v./DD/MM/AAAA` que termina cada aviso — más confiable que el separador visual "-- -- --", que no siempre está presente entre dos avisos del mismo organismo.
6. Los IDs de la cablera llevan el prefijo `boletiner-` (ej. `boletiner-28410-dto-2026-2310-e-ger-gob`, `boletiner-28410-lic-50749`).
7. Dedup y "última edición procesada" salen de `data/log_filtro_boletin.jsonl` (se toma el `nro` más alto ya logueado) — no hay archivo de estado separado. **Primera corrida**: arranca desde la edición más reciente del índice, nunca desde el histórico completo (el índice tiene ediciones desde 2020).

## Fuera de alcance de esta versión (2026-09)

- **Sección Comercial**: solo Licitaciones se parsea item por item. Edictos judiciales, Personas Jurídicas, y las subcategorías de Organismos Públicos que no son licitaciones (Comunicados, Citaciones, Notificaciones, Decretos, Convocatorias a Elecciones) se descartan en bloque, logueadas solo como categoría + rango de página, sin extraer cada ítem individual. Si en algún momento se decide que alguna de estas vale la pena (ej. Convocatorias a Elecciones), extender el parser siguiendo el mismo patrón que Licitaciones.
- **Corrección del artefacto de negrita duplicada**: el texto extraído del PDF a veces duplica cada carácter en líneas que en el original están en negrita (ej. "GGOOBBIIEERRNNOO" en vez de "GOBIERNO"). No se corrige sistemáticamente — donde importa (títulos de norma) se toma el título limpio del SUMARIO en vez del cuerpo; en licitaciones puede colar en el título candidato ocasionalmente. Cosmético, no bloqueante.
- **Skill de investigación** (`investigar-boletin`, con las dos salidas: nota lista vs. entrada en `docs/temas-a-seguir.md`) — diseño acordado con Francisco (2026-09-06), todavía no construida.

**Panel admin (2026-09-06/07, estados rediseñados 2026-09-07, unificados de nuevo 2026-09-07, ver `admin/index.html`)**: el Boletín tiene su propia **macro-pestaña** ("Boletín Oficial", junto a "Cablera" y "Agenda") que cambia toda la vista, no un filtro adicional — un ítem del Boletín no aparece mezclado en "Cablera" (mismo motivo que el filtro mecánico: evitar volumen). Los **4 estados** (Pendientes / A publicar / A investigar / Descartadas, `ESTADOS` en `admin/index.html`) son los mismos para todas las fuentes de la cablera, no una particularidad del Boletín — se unificaron el mismo día que se separaron, apenas apareció un caso real de un ítem de otra fuente (EPRE) que también necesitaba "a investigar" (ver `docs/servicios-publicos-tarifas.md`). Los dos estados positivos son decisiones editoriales distintas, no un matiz de la misma:
- **A publicar**: el editor considera que alcanza con investigación breve — sigue el mismo camino que cualquier otro ítem de la cablera, vía `procesar-cablera` (que ya no hace ningún caso especial para esta fuente, ver `skills/procesar-cablera/SKILL.md`).
- **A investigar**: un tema de fondo para dejar sobre la mesa, que puede llevar más de un día de reporteo (antecedentes, entrevistas, comparación con otras fuentes) antes de convertirse en nota o no. `procesar-cablera` no lo toca — queda esperando la futura skill `investigar-boletin`.

**No existe un estado "procesado"** (ni acá ni en la Cablera general): cuando un ítem ya tiene un borrador subido a WordPress, se marca con un check visual (`wp_edit_url` presente, más `procesado_el`) sin sacarlo de su estado editorial ni de su pestaña — la pregunta "¿está listo/investigado?" y la pregunta "¿el pipeline ya generó el borrador?" son independientes.

**Skill `evaluar-boletin`** (nueva, 2026-09-07, ver `skills/evaluar-boletin/SKILL.md`) — triagea los ítems `pendiente` del Boletín con un resumen en limpio (qué dice, sin jerga legal) y una señal de si hay ángulo noticioso potencial, antes de que el editor decida marcarlos "a investigar" o descartarlos. Es el paso intermedio entre el filtro mecánico (`monitorear_boletin_er.py`, sin ningún juicio editorial) y la futura `investigar-boletin` (investigación completa sobre lo ya marcado).

## Revisión periódica del log de filtrado (idea de Francisco, 2026-09-06, no implementada)

Cada cierto tiempo (propuesta: mensual, o cuando el log acumule un volumen relevante) vale la pena revisar `data/log_filtro_boletin.jsonl` buscando patrones que el filtro mecánico no puede ver por sí solo, mismo espíritu que `aprender-noticiabilidad` sobre `data/backlog.json`:
- Un mismo organismo con muchos rechazos de recurso concentrados en poco tiempo (posible señal de conflicto sistemático, no solo casos individuales sueltos).
- El mismo tipo de motivo repetido de forma inusual.
- Montos que aparecen en los títulos/cuerpos filtrados y que en retrospectiva se ven grandes.

No implementar como automatización todavía — es una tarea de revisión manual o una futura skill, análoga a `aprender-noticiabilidad`, si el volumen lo justifica.

## Horario de corrida

**Corregido de nuevo 2026-09-06 (Francisco)**: dos corridas por día hábil, no cada 15 minutos. La primera corrección (cada 15 min, igual que los otros dos monitores) subestimaba el costo real — a diferencia de un JSON liviano, esta corrida levanta un job completo (checkout + setup de Python + instalar `pypdf`) aunque no haya edición nueva, y a diferencia de un comunicado de prensa, nadie nos "gana de mano" al Boletín por unos minutos de diferencia. `.github/workflows/monitorear_boletin_er.yml` corre a las 09:00 y 15:30 hora Argentina (12:00 y 18:30 UTC), de lunes a viernes — la mañana por si sale temprano, la tarde con margen sobre el único dato que tenemos hasta ahora (una edición quedó con `Last-Modified` ~13:24 ART).

**Cómo se va a ajustar con datos reales**: `procesar_edicion()` guarda el header `Last-Modified` real de cada PDF en la entrada `resumen_edicion` de `data/log_filtro_boletin.jsonl` (campo `pdf_last_modified`). Con unas semanas de corridas reales, revisar ese campo antes de seguir adivinando el horario — puede que el patrón real sea distinto al de la única edición que vimos hoy.
