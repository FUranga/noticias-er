---
name: analizar-cobertura-medios
description: Analiza los ítems capturados por pipeline/monitorear_medios.py (fuente "medios-*" en data/backlog.json) para detectar patrones en cómo cubren otros medios Entre Ríos — temas más cubiertos, huecos de cobertura, y tendencia a reproducir comunicados oficiales sin trabajo propio — y actualiza docs/analisis-medios.md con lo aprendido. No decide nada por sí sola, no cambia el estado de ningún ítem de la cablera. Usar cuando el usuario pide "analizá cómo están cubriendo los medios", "qué huecos hay en la cobertura", o cada tanto como mantenimiento (no en cada corrida diaria del agregador — necesita volumen acumulado para decir algo real).
---

# Analizar la cobertura de otros medios

Contexto: el agregador "Medios" (`pipeline/monitorear_medios.py`, ver `docs/fuentes.md`) captura notas de otros medios de Entre Ríos que matchean el filtro de tópico+lugar, para que el editor las mire en su propia macro-pestaña de `admin/index.html`. Esta skill es un segundo uso de esos mismos datos: no mirar cada nota para decidir si citarla, sino mirar el conjunto para entender **cómo está cubierto el panorama mediático de la provincia** — conecta directo con la "Visión aspiracional" de `docs/vision-y-etapas.md` ("accountability sobre anuncio, no tomar el comunicado por cierto") y con el principio de "agencia, no repetición" (`docs/vision-y-etapas.md`, `docs/aliados-y-financiamiento.md`): un hueco real en la cobertura de otros medios es evidencia concreta de dónde este proyecto puede aportar algo que nadie más está haciendo.

**Esta skill nunca decide qué cubrir, nunca cambia el estado de un ítem de la cablera.** Solo lee lo ya capturado y escribe un documento de referencia — la decisión editorial de qué hacer con un hueco detectado (investigarlo, sumarlo a `docs/temas-a-seguir.md`, ignorarlo) sigue siendo de Francisco.

**Aviso sobre volumen (igual que `aprender-noticiabilidad`, que espera "5-10 descartes nuevos" antes de correr)**: con pocos días de captura acumulada, cualquier patrón es apenas una hipótesis débil, no una conclusión. No fuerces un patrón con una muestra chica — señalalo como "todavía no hay suficiente data para decir esto con confianza" en vez de escribirlo como hallazgo firme.

## Proceso

1. **Leer los ítems `medios-*` de `data/backlog.json`** agregados desde la última corrida de esta skill (ver fecha registrada al final de `docs/analisis-medios.md`; si nunca corrió, todos). Para cada uno tenés: `fuente` (medio de origen), `fecha`, `topicos_matcheados`, `lugares_matcheados`, `link`, `texto_original` (el resumen/copete del RSS, no siempre el cuerpo completo de la nota).

2. **Temas más cubiertos, por medio y en conjunto**: contar frecuencia de cada tópico (`data/topicos_medios.json` tiene el listado completo de categorías posibles) — tanto en total como desglosado por medio, para ver si algún medio tiene un sesgo temático marcado (ej. uno que solo cubre judicial, otro que casi no toca economía).

3. **Huecos de cobertura**: tópicos de `data/topicos_medios.json` que aparecen muy poco o nada en el conjunto capturado. Antes de anotar un hueco como real, distinguí dos causas posibles (no son lo mismo):
   - **Hueco genuino**: el tema tiene actividad real (hay comunicados en `data/backlog.json` de fuentes institucionales sobre eso) pero ningún medio lo cubre — esto sí es una señal fuerte de oportunidad editorial.
   - **Filtro débil, no hueco real**: puede que el tópico simplemente no esté bien capturado por las palabras clave de `data/topicos_medios.json` (ver el log `data/log_filtro_medios.jsonl` para chequear si hay ítems filtrados que en realidad sí eran de ese tema) — en ese caso el hallazgo es "hay que ajustar el filtro", no "hay un hueco editorial".

4. **Tendencia a reproducir comunicados oficiales sin trabajo propio ("oficialismo")**: esto necesita leer con criterio editorial, no un cálculo mecánico de palabras clave (a diferencia de los pasos anteriores). Señales a buscar nota por nota (usando el link para leer la nota completa cuando el copete del RSS no alcanza, con la misma restricción de no usar WebFetch para resumir sitios de terceros — bajar el HTML crudo y leer el contenido real):
   - ¿Repite la estructura y las citas de un comunicado oficial casi palabra por palabra, sin una sola fuente/voz que no sea la del organismo que lo emitió?
   - ¿Hay contraste, pregunta incómoda, o al menos contexto adicional que el comunicado no traía?
   - ¿El título del medio es prácticamente el título que habría puesto el propio organismo?
   No generalices con 1-2 notas — necesitás ver un patrón consistente en varias notas del mismo medio antes de anotar "este medio tiende al oficialismo" como hallazgo, y siempre con los ejemplos concretos (título + link) que lo sostienen.

5. **Actualizar `docs/analisis-medios.md`** (crear si no existe, con esta misma estructura):
   - **Temas más cubiertos** (agregado, y por medio si hay algo notable).
   - **Huecos detectados**, marcando cuáles parecen genuinos y cuáles son sospecha de filtro débil (ver paso 3).
   - **Notas sobre tendencia editorial por medio** (oficialismo/independencia), cada una con los ejemplos concretos que la sostienen — nunca una afirmación sin el caso real detrás, mismo criterio que `docs/criterios-noticiabilidad.md`.
   - Fecha de esta corrida y cuántos ítems nuevos se analizaron (para que la próxima corrida sepa desde dónde seguir).

6. **Si un hueco genuino sugiere una pista de investigación concreta**, sumalo a `docs/temas-a-seguir.md` (no lo dupliques en `analisis-medios.md` con el detalle completo — un puntero alcanza). Si un medio muestra una señal clara y sostenida de rigor/independencia editorial, señalalo también en `docs/aliados-y-financiamiento.md` como dato a favor de una futura alianza — ninguna de las dos cosas es automática, son sugerencias para que Francisco las pondere.

7. **Reportar al final**: cuántos ítems nuevos se analizaron, qué patrones/huecos se agregaron o reforzaron, y qué quedó señalado explícitamente como hipótesis débil por falta de volumen.

## Nota

El volumen de `medios-*` en `data/backlog.json` depende enteramente de qué tan seguido corra `pipeline/monitorear_medios.py` (hoy manual, no automatizado con GitHub Actions todavía — ver `docs/fuentes.md`). Esta skill es tan buena como la cantidad de días de captura acumulados; no tiene sentido correrla dos veces en el mismo día.
