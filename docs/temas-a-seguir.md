# Temas a seguir

Listado de pistas, ángulos secundarios, menciones sueltas y observaciones que aparecen al evaluar o redactar una nota — no hace falta que sugieran una historia propia clara, alcanza con que parezcan datos que podrían servir de contexto más adelante. No es la cablera (`data/backlog.json` es para comunicados ya recibidos y con estado editorial, y conserva todo lo que entra, se publique o no) — esto es para **indicios** que todavía no son un comunicado ni una nota, solo una pista o una observación a guardar.

Sirve para dos cosas: no perder el hilo de algo que apareció al pasar, y (más adelante, si el medio suma periodistas propios) tener un banco de temas para asignar cobertura.

## Cómo se usa

Se agrega un ítem cuando, evaluando un comunicado (skill `evaluar-comunicado`) o redactando una nota (skill `redactar-noticia`), aparece:
- Un **segundo ángulo** dentro del mismo comunicado, más noticioso que el principal que plantea la fuente — algo que se les escapó sin querer (un dato que reconoce un problema, un retraso, un conflicto no anunciado como tal).
- Una señal de que el comunicado está **reencuadrando o tapando** otra historia poniendo el foco en otra cosa.
- Una **mención suelta** (un nombre, una cifra, una situación mencionada al pasar) que sugiere que hay más para investigar.

Antes de agregarlo acá, si hay indicio de que el tema ya tuvo repercusión en otro lado (otro medio, redes, un organismo distinto), vale la pena buscarlo — puede que ya haya material para armar la nota ahora en vez de dejarla pendiente.

**Esto acumula conocimiento, no baja el estándar editorial (2026-09-04, aclarado por Francisco tras una primera versión mal calibrada de esta nota)**: la idea NO es archivar cualquier cosa de cualquier comunicado, ni relajar el criterio de qué se publica como noticia (eso lo sigue marcando `docs/criterios-noticiabilidad.md` sin cambios). Es acumular, con criterio, lo que a futuro — "cuando seamos un medio de verdad" — pueda servir para tres cosas concretas:
1. **Fuente de consulta para otras historias**: contexto de fondo que hoy no amerita nota propia pero que ilumina algo cuando aparezca una historia relacionada más adelante.
2. **Ángulos de historias polémicas a seguir**: algo que suena controvertido o irregular en un comunicado, sin explicación clara, que vale la pena tener anotado para retomar cuando haya tiempo o más elementos.
3. **Fechas importantes a seguir** — esto en la práctica vive en `data/agenda.json` (ver `docs/agenda.md`), no acá; se menciona para que quede claro que es parte de la misma lógica de acumulación, no un archivo separado sin relación.

Esto sigue siendo criterio editorial, no un checklist mecánico: no hace falta (ni conviene) anotar algo de cada comunicado que se descarta — la mayoría de los descartes son pura autopromoción sin nada que valga la pena guardar, y así se anota (con su motivo en `data/backlog.json`, que ya conserva todo). Acá solo entra lo que específicamente tiene un ángulo de contexto o de controversia sin resolver.

Cada ítem lleva: fecha, tema, de qué comunicado/nota salió, por qué es interesante, estado.

**Estados**: `para investigar` (nadie lo tocó todavía) · `en investigación` · `cubierto` (se convirtió en nota — con link) · `descartado` (se investigó y no dio nada — con motivo).

## Temas

### 2026-09-04 — Conflicto de la DPV con el avance de Consorcios Camineros
**De**: `senadoer-el-senado-sanciono-la-ley-de-consorcios-camineros` (comunicado del Senado de ER, 1/9/2026).
**Por qué es interesante**: el comunicado oficial presenta la sanción como aprobación institucional sin sobresaltos. Una búsqueda en medios locales (bicameral.com.ar) confirma que la votación del 1/9 ocurrió **mientras trabajadores de la Dirección Provincial de Vialidad (DPV) protestaban** contra la reestructuración del organismo y puntualmente contra el avance de los Consorcios Camineros — el comunicado del Senado no lo menciona. Además, ya se confirmó que la ley tuvo **sanción definitiva** (media sanción de Diputados + sanción del Senado) y pasó al Poder Ejecutivo para su promulgación — no vuelve a Diputados, como se especulaba antes de chequear.
**Estado**: `en investigación` — pendiente decidir si arma una nota propia conectando la sanción + el conflicto de la DPV + lo que quedó pendiente en la misma sesión (modificación a la Ley de Municipios, expediente 26.785 de Dal Molín). Ojo con oportunidad: ya lo cubrieron medios chicos de ER desde el 1-2/9, así que el valor agregado tiene que ser conectar los puntos, no repetir.

### 2026-09-04 — Publicación de salarios y declaraciones juradas de funcionarios públicos
**De**: no viene de un comunicado puntual — anotado directamente por Francisco a partir de la investigación de medios gold-standard (ver "Visión aspiracional" en `docs/vision-y-etapas.md`).
**Por qué es interesante**: en algún momento el Gobierno de Entre Ríos anunció la publicación de salarios y declaraciones juradas de funcionarios públicos, y el tema se discutió/analizó poco en profundidad después del anuncio inicial. Encaja directo con el patrón "accountability sobre anuncio, no tomar el comunicado por cierto" — chequear qué se prometió, qué se publicó realmente, y si sigue actualizado. Candidato a primer proyecto de tipo "tracker/chequeador" (inspirado en "Full Disclosure" de VTDigger).
**Estado**: `para investigar` — todavía no se buscó el anuncio original ni se verificó qué existe hoy publicado.

### 2026-09-04 — Proyecto de alivio fiscal a comercios, estado sin confirmar
**De**: `senadoer-senadores-se-reuniran-en-comisiones-y-tendran-sesion-ordinaria` (comunicado del Senado de ER, 28/8/2026, descartado como nota por ser agenda vencida).
**Por qué es interesante**: mencionaba que la Comisión de Presupuesto y Hacienda trataría el 26/8 el expediente N° 29.362 — un proyecto del Poder Ejecutivo (con media sanción de Diputados) con "medidas tributarias orientadas a aliviar la carga fiscal que recae sobre la actividad comercial" en la provincia, con foco en pequeños contribuyentes y comercios de cercanía. No apareció en ningún comunicado posterior si se trató, dictaminó o votó.
**Estado**: `para investigar` — chequear si hubo despacho de comisión o tratamiento en el recinto en sesiones posteriores.

### 2026-09-06 — La AGN no auditó fondos nacionales en Entre Ríos en ocho años
**De**: investigación de mapeo institucional (no de un comunicado) — pedido de acceso a la información de Análisis Digital a la AGN (Ley 27.275), respondido en Nota 164/26-PL (3/7/2026, Actuación 150/26). Ver `docs/fuentes.md` (sección Nacional) y `docs/acceso-informacion-publica.md` para el marco legal del pedido.
**Por qué es interesante**: desde 2018 la AGN no hizo una sola auditoría directa sobre fondos nacionales en Entre Ríos — ni la tarifa diferencial de Salto Grande (Ley 24.954), ni la deuda provincial (Bono ERF25), ni programas alimentarios, ni obras viales, ni préstamos internacionales ejecutados en la provincia. Hallazgos puntuales ya confirmados: préstamos BID/BIRF con ejecución en ER "fuera de muestra" en todos los ejercicios (caso Hernandarias, 4 ejercicios seguidos, USD 219.260); dos obras hídricas (San José de Feliciano, Villa Elisa) pagadas sin Informe Final de Obra (Resolución 122/2022 AGN); Vialidad Nacional sin auditoría con datos de ER posterior a marzo de 2019 (nada desde la paralización de obras de diciembre 2023). El pedido original (10 puntos) es una plantilla reutilizable — replicarlo cada 1-2 años, actualizando el rango de fechas.
**Estado**: `para investigar` — evaluar si ya hay material para una nota propia ("ocho años sin auditar") o si conviene esperar la próxima repetición del pedido para tener un dato más fresco.

### 2026-09-06 — Concepción del Uruguay y Victoria no adhirieron ni al Compromiso Provincial de Transparencia
**De**: investigación de mapeo institucional — datos del Compromiso Provincial de Transparencia y Apertura Gubernamental (`portal.entrerios.gov.ar/transparencia`), distinto de la adhesión formal a la Ley 11.191 (ver `docs/acceso-informacion-publica.md`).
**Por qué es interesante**: 62 de 84 municipios relevados adhirieron al Compromiso (voluntario, sin costo político real). Concepción del Uruguay (segunda ciudad de la provincia) y Victoria directamente no firmaron — ni siquiera el mínimo. Otro grupo adhirió pero quedó con puntaje 0 (Federación, Nogoyá, Villaguay, entre otros) — "firmaron y no publicaron nada".
**Estado**: `para investigar` — confirmar vigencia del dato y si hubo pronunciamiento de esos municipios al respecto.

### 2026-09-06 — Paraná adhirió al Compromiso de Transparencia pero no completó sus declaraciones juradas
**De**: mismo relevamiento que el ítem anterior.
**Por qué es interesante**: Paraná adhirió y completó Escala Salarial y Nómina de Autoridades, pero las Declaraciones Juradas Sintéticas figuran "en proceso" — puntaje 25/30. Ángulo directo: "Paraná adhirió a la transparencia pero no completa lo que se comprometió a publicar".
**Estado**: `para investigar` — confirmar si sigue "en proceso" al momento de escribir, y desde cuándo.

### 2026-09-06 — El EPRE no tiene Directorio propio desde 1996
**De**: investigación comparada con Connecticut, ver `docs/fundacion-agenda-institucional.md`.
**Por qué es interesante**: el Decreto 1127/96 MEOSP intervino el ente regulador de energía de ER — casi 30 años después sigue sin directorio estatutario, solo un interventor con las facultades del Directorio. Contradicción llamativa: el EPRE sí convoca audiencias públicas de tarifas con defensores del usuario propuestos por colegios profesionales (participación ciudadana real), montadas sobre una estructura de gobierno vaciada.
**Estado**: `para investigar` — confirmar situación actual del interventor y si hubo algún intento de recomponer el directorio.

### 2026-09-06 — Proyecto de Comisión Bicameral de seguimiento de la Caja de Jubilaciones (Vázquez, en trámite)
**De**: investigación comparada con Connecticut, ver `docs/fundacion-agenda-institucional.md`.
**Por qué es interesante**: proyecto presentado en julio de 2026 por la diputada Erica Vázquez (Juntos por Entre Ríos) — 10 legisladores (5 senadores, 5 diputados) respetando representación proporcional de bloques, para seguimiento y evaluación de la Caja de Jubilaciones. Todavía no está aprobado. Es un caso en tiempo real de una comisión de control plural que podría nacer o quedar cajoneada.
**Estado**: `en investigación` — seguir su trámite parlamentario.

### 2026-09-06 — Uso real de la Ley 10.529 (audiencias públicas) desde 2018, nunca relevado
**De**: investigación comparada con Connecticut, ver `docs/fundacion-agenda-institucional.md` y `docs/acceso-informacion-publica.md` para el detalle legal de la ley.
**Por qué es interesante**: no se identificó ningún relevamiento de cuántas audiencias públicas se convocaron en Entre Ríos desde la sanción de la ley en 2018, ni en qué proporción fueron obligatorias vs. facultativas — dato que permitiría medir si el instituto se usa poco por falta de casos obligatorios o por decisión discrecional de no convocarlas. Relacionado: no se encontró antecedente de un acto impugnado judicialmente por omisión de audiencia pública obligatoria (art. 3).
**Estado**: `para investigar` — pedido de acceso a la información a la autoridad de aplicación de la Ley 10.529 como primer paso.
