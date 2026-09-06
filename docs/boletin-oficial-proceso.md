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
- **Skill de investigación** (`investigar-boletin`, con las dos salidas: nota lista vs. entrada en `docs/temas-a-seguir.md`) — diseño acordado con Francisco (2026-09-06), todavía no construida. **La pestaña "Boletín Oficial" del panel admin ya está implementada** (2026-09-06, ver `admin/index.html`): agrupa todos los ítems de esta fuente por estado (Pendientes / A investigar / Procesadas / Descartadas) en una sola vista, ordenados por `prioridad` dentro de cada grupo — además de seguir apareciendo en las pestañas generales por estado. El botón de "marcar para publicar" dice "marcar para investigar" para ítems de esta fuente, para no sugerir que están listos para redactar directo. **Importante**: `procesar-cablera` excluye explícitamente los ítems de esta fuente del estado `a_publicar` (ver `skills/procesar-cablera/SKILL.md`) — necesitan pasar por `investigar-boletin` primero, no por redacción directa.

## Revisión periódica del log de filtrado (idea de Francisco, 2026-09-06, no implementada)

Cada cierto tiempo (propuesta: mensual, o cuando el log acumule un volumen relevante) vale la pena revisar `data/log_filtro_boletin.jsonl` buscando patrones que el filtro mecánico no puede ver por sí solo, mismo espíritu que `aprender-noticiabilidad` sobre `data/backlog.json`:
- Un mismo organismo con muchos rechazos de recurso concentrados en poco tiempo (posible señal de conflicto sistemático, no solo casos individuales sueltos).
- El mismo tipo de motivo repetido de forma inusual.
- Montos que aparecen en los títulos/cuerpos filtrados y que en retrospectiva se ven grandes.

No implementar como automatización todavía — es una tarea de revisión manual o una futura skill, análoga a `aprender-noticiabilidad`, si el volumen lo justifica.

## Horario de corrida

**Corregido 2026-09-06**: corre cada 15 minutos (`.github/workflows/monitorear_boletin_er.yml`), igual que `monitorear_gobierno_er.yml` y `monitorear_senado_er.yml` — no una vez por día como se decidió originalmente. El chequeo del índice de ediciones es un JSON chico y barato; el trabajo pesado (bajar y parsear el PDF de 100 páginas) solo se dispara cuando aparece una edición nueva de verdad. No hay razón para sacrificar rapidez de detección por un ahorro que no existe. La edición de referencia (Nº 28.410) quedó publicada (PDF con `Last-Modified`) a las 16:24 GMT (~13:24 hora Argentina) — con esta cadencia, el lag de detección es de minutos sin depender de acertar ese horario.
