# Hallazgos institucionales — captura corriente (FUNDER)

Registro de vacíos de contrapesos, fallas institucionales y mejoras potenciales que van apareciendo al mapear fuentes o investigar para el medio — pensado para la Fundación para el Desarrollo Entrerriano, **no es cobertura editorial** (misma distinción que `docs/fundacion-agenda-institucional.md`, del cual este documento es el insumo crudo). Mismo espíritu que `docs/temas-a-seguir.md` (capturar apenas aparece, sin forzar análisis en el momento) pero para el costado "Fundación", no el editorial — separado a propósito para no mezclar la decisión de qué es noticia (siempre humana, siempre del medio) con la agenda de reforma institucional (de FUNDER).

**Por qué un documento aparte de `docs/fundacion-agenda-institucional.md`**: ese documento es el análisis terminado (comparación con Connecticut, huecos priorizados, propuestas concretas) — no es el lugar para anotar un hallazgo suelto a mitad de una investigación de otra cosa. Acá se anota rápido, sin pulir; cada tanto (mismo criterio que `aprender-noticiabilidad` sobre `docs/criterios-noticiabilidad.md`) se revisa este archivo y lo que ya tiene forma de propuesta se traslada a `fundacion-agenda-institucional.md`.

**Por qué no vive en la cablera (`data/backlog.json`)**: se evaluó explícitamente (2026-09-07, pedido de Francisco) y se decidió que no — la cablera es específicamente el pipeline editorial del medio (comunicados con estado de noticiabilidad), y mezclar ahí hallazgos de reforma institucional de FUNDER contaminaría esa lógica sin necesidad. Un documento aparte cumple el mismo propósito (capturar sin perder el hilo) sin tocar el modelo de datos ni el panel del medio.

**Sobre la página interactiva (idea de Francisco, 2026-09-07)**: pendiente de decidir, no construida todavía. Si en algún momento se arma, este documento (o los datos que termine acumulando) es la fuente — no reconstruir el contenido dos veces en dos formatos que se desincronizan.

## Cómo se usa

Un ítem nuevo por hallazgo, con: fecha, de dónde salió, por qué importa, y estado. Mismos estados que `docs/temas-a-seguir.md`: `para investigar` / `en investigación` / `con propuesta` (ya tiene forma de recomendación concreta, ver `fundacion-agenda-institucional.md`) / `trasladado` (ya vive en el documento de agenda, se deja acá solo como referencia con el link).

## Hallazgos

### 2026-09-06 — No existe Defensoría del Pueblo provincial
Una de solo 6 provincias argentinas sin una (junto con Mendoza, Salta, Misiones, Santa Cruz, La Pampa) — solo defensorías municipales (Paraná, desde 2003). El hueco más fácil de nombrar y más "vendible" políticamente, según el análisis comparado.
**Estado**: `con propuesta` — ver `docs/fundacion-agenda-institucional.md`, huecos priorizados #2.

### 2026-09-06 — EPRE sin Directorio propio desde 1996
Decreto 1127/96 MEOSP intervino el ente regulador de energía — casi 30 años después sigue sin directorio estatutario, solo un interventor con las facultades del Directorio, sin razón técnica que lo justifique.
**Estado**: `con propuesta` — ver `docs/fundacion-agenda-institucional.md`, huecos priorizados #3, y `docs/temas-a-seguir.md` para el ángulo editorial.

### 2026-09-06 — AGN no auditó fondos nacionales en Entre Ríos en ocho años
Desde 2018, ninguna auditoría directa sobre tarifa de Salto Grande, deuda provincial (Bono ERF25), programas alimentarios, obras viales o préstamos internacionales ejecutados en la provincia. Ver el detalle completo en `docs/temas-a-seguir.md`.
**Estado**: `en investigación` (lado editorial) / `para investigar` (lado propuesta — ¿hace falta una vía provincial de control cuando Nación no controla?).

### 2026-09-06 — CAFESG redujo su integración plural en 2000
En 2000 se redujo la Comisión Administradora del Fondo Especial de Salto Grande de 6 a 4 miembros, excluyendo a la oposición legislativa (consta en el Diario de Sesiones de Diputados) — caso concreto y citable de retroceso institucional puntual y reversible.
**Estado**: `con propuesta` — ver `docs/fundacion-agenda-institucional.md`, huecos priorizados #8. **Corrección 2026-09-07**: confirmado que la CAFESG es un organismo *provincial* (depende de la Secretaría de Gobierno de ER), no binacional/nacional — no confundir con la Comisión Técnica Mixta de Salto Grande, que sí lo es (ver `docs/fuentes.md`).

### 2026-09-06 — Municipios que no cumplen ni el mínimo de transparencia voluntaria
Concepción del Uruguay (segunda ciudad de la provincia) y Victoria no adhirieron ni al Compromiso Provincial de Transparencia (voluntario, sin costo político real). Paraná adhirió pero no completó las Declaraciones Juradas Sintéticas (25/30 puntos). Ver `docs/temas-a-seguir.md` para el detalle y el link al ranking.
**Estado**: `para investigar` (lado propuesta) — ¿alcanza con exposición pública (ranking) o hace falta algún incentivo/sanción para que adherir signifique algo?

### 2026-09-06 — Vaciamiento de transparencia activa en organismos autárquicos
Del portal de Datos Abiertos (CKAN) provincial: ATER, Caja de Jubilaciones, Consejo General de Educación, COPNAF, Consejo de la Magistratura, Contaduría General, Vialidad (DPV), los 4 entes autárquicos portuarios, Ente Región Centro, Ente del Túnel Subfluvial, Ente de Control de Telecomunicaciones, Ente de Aguas Termales, IAPSER, IAFAS, Instituto de Cooperativas, Policía, Tesorería General, Tribunal de Cuentas y UADER tienen **cero datasets publicados**, pese a que sí hay obligación formal de transparencia activa. Ver `docs/fuentes.md`, sección "Portal de Datos Abiertos".
**Estado**: `para investigar` — ¿hay sanción prevista por incumplir la obligación de transparencia activa, y se aplicó alguna vez?

### 2026-09-06 — Sin portal único de compras públicas
A diferencia de Nación (COMPR.AR), Entre Ríos no tiene un portal centralizado de licitaciones — cada organismo publica las suyas por separado. Es en sí misma una nota de transparencia, y un hueco de diseño institucional (Connecticut tiene un State Contracting Standards Board bipartidista que audita contratos grandes; ER no tiene nada equivalente).
**Estado**: `con propuesta` — ver `docs/fundacion-agenda-institucional.md`, huecos priorizados #7.

### 2026-09-06 — Uso real de la Ley 10.529 (audiencias públicas) nunca relevado
No se identificó ningún relevamiento de cuántas audiencias públicas se convocaron en Entre Ríos desde 2018, ni en qué proporción fueron obligatorias vs. facultativas. Sin antecedente de un acto impugnado judicialmente por omisión de audiencia obligatoria (art. 3). Ver `docs/temas-a-seguir.md` y `docs/acceso-informacion-publica.md`.
**Estado**: `para investigar` — pedido de acceso a la información a la autoridad de aplicación como primer paso.

### 2026-09-06 — No existe una "Ley de Reuniones Abiertas" (open meetings)
Distinto del acceso a documentos: es el derecho a presenciar en vivo cómo delibera un cuerpo colegiado provincial (IOSPER, ATER, IAPV, CGE, CMER, el propio TCER) — hoy no hay regla de base que presuma pública esa actividad ordinaria, ni obligación de cronograma anual de reuniones, ni régimen de actas con plazo fijo. Es el hueco estructural más claro que salió de comparar con Connecticut (que sí tiene "Open Meetings Law" desde hace décadas).
**Estado**: `con propuesta` — ver `docs/fundacion-agenda-institucional.md`, sección "Acceso a reuniones", con propuesta de ley concreta ya redactada.

### 2026-09-07 — Entre Ríos no tiene ente regulador provincial de agua/saneamiento
A diferencia de Santa Fe (ENRESS), Córdoba (ERSeP) o CABA (ERAS), no existe un organismo técnico independiente que regule tarifas o calidad del servicio de agua potable — está fragmentado entre municipios (Paraná lo presta directo) y cooperativas locales (federadas en FECAPER), sin autoridad de aplicación única. La Dirección Provincial de Obras Sanitarias ejecuta obra, no regula. Ver `docs/servicios-publicos-tarifas.md` y `docs/fuentes.md` (sección "Servicios públicos regulados").
**Estado**: `para investigar` — ¿alguna vez se propuso crear un ente regulador de agua en la Legislatura? Buen candidato a sumar a la tabla comparativa de `fundacion-agenda-institucional.md` (agregar una fila de "servicios públicos" a la comparación con Connecticut, que no la tiene todavía).

### 2026-09-07 — Transporte interurbano provincial sin audiencia pública, a diferencia del urbano municipal
La Secretaría de Transporte fija la tarifa interurbana por resolución ministerial directa, sin proceso participativo — a diferencia del EPRE (que sí convoca audiencia pública para revisiones tarifarias de fondo). **Aclaración importante, verificada 2026-09-07 a partir de la duda de Francisco sobre si esto se debía a que en realidad es un tema municipal**: no es que la audiencia pública "se mudó" a lo municipal — son dos competencias distintas (interurbano = provincial, urbano = municipal) y **el transporte urbano de Paraná sí tiene práctica real de audiencia pública** ante el Concejo Deliberante antes de aprobar un aumento del boleto (confirmado con casos concretos, la más reciente en julio de 2026). La asimetría real es entre niveles de gobierno para el mismo tipo de servicio: el municipio consulta, la provincia no, para la porción del transporte que a cada uno le toca regular.
**Estado**: `para investigar` — ¿por qué el nivel provincial no replica el mecanismo municipal? ¿Hay algún proyecto legislativo que lo haya propuesto?

### 2026-09-07 — Gas sin regulador provincial (menor prioridad, es lo común en otras provincias)
A diferencia de la electricidad (EPRE), no hay ente regulador provincial de gas — la tarifa de CEGSA (la distribuidora estatal) la fija ENARGAS a nivel nacional. Distinto de la asimetría del agua: esto es lo habitual en la mayoría de las provincias argentinas (el gas suele regularse a nivel nacional en general), así que es menos claramente una anomalía comparativa que el caso del agua. Se anota igual para no perder el dato.
**Estado**: `para investigar`, prioridad baja.
