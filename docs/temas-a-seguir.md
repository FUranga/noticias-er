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

### 2026-09-04 — Proyecto de alivio fiscal a comercios, estado sin confirmar
**De**: `senadoer-senadores-se-reuniran-en-comisiones-y-tendran-sesion-ordinaria` (comunicado del Senado de ER, 28/8/2026, descartado como nota por ser agenda vencida).
**Por qué es interesante**: mencionaba que la Comisión de Presupuesto y Hacienda trataría el 26/8 el expediente N° 29.362 — un proyecto del Poder Ejecutivo (con media sanción de Diputados) con "medidas tributarias orientadas a aliviar la carga fiscal que recae sobre la actividad comercial" en la provincia, con foco en pequeños contribuyentes y comercios de cercanía. No apareció en ningún comunicado posterior si se trató, dictaminó o votó.
**Estado**: `para investigar` — chequear si hubo despacho de comisión o tratamiento en el recinto en sesiones posteriores.
