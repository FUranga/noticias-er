---
name: aprender-noticiabilidad
description: Analiza los ítems descartados y publicados en data/backlog.json para detectar patrones en qué considera noticiable el editor y qué no, y actualiza docs/criterios-noticiabilidad.md con lo aprendido. No decide nada por sí sola ni cambia el estado de ningún ítem — solo documenta el criterio para que evaluar-comunicado sugiera mejor. Usar cuando el usuario pide "aprendé de lo que descarté", "actualizá los criterios de noticiabilidad", o cada tanto como mantenimiento (ej. después de procesar un lote grande de la cablera).
---

# Aprender criterios de noticiabilidad del uso real

Contexto: `docs/criterios-noticiabilidad.md` es un documento vivo que intenta capturar cómo piensa Francisco al decidir qué comunicado se convierte en noticia y cuál no — más específico y más real que el filtro genérico de `docs/estilo-editorial.md`. Esta skill es la que lo mantiene actualizado, mirando las decisiones que ya tomó en `admin/index.html` (registradas en `data/backlog.json`).

**Esta skill nunca decide, publica ni descarta nada.** Solo lee decisiones ya tomadas y escribe un documento de referencia. La skill `evaluar-comunicado` es la que consume ese documento para dar mejores sugerencias — el criterio de noticiabilidad en sí sigue siendo enteramente humano.

## Proceso

1. **Leer `data/backlog.json`.** Separar:
   - **Negativos**: ítems `estado: "descartado"`.
   - **Positivos**: ítems `estado: "procesado"` (llegaron a convertirse en borrador — el editor los consideró noticiables) y `estado: "a_publicar"` (marcados pero todavía no procesados, también cuentan como positivos).
   - **Ítems del Boletín Oficial** (`fuente: "Boletín Oficial de Entre Ríos"`): entran al mismo análisis, pero anotá los patrones que salgan de ahí por separado en `docs/boletin-oficial-proceso.md` (sección "Qué buscar al triagear un ítem"), no en este documento — el material es texto legal, no comunicados de prensa, y mezclar los dos tipos de patrón en `docs/criterios-noticiabilidad.md` lo haría más confuso, no más útil.

2. **Para los descartes sin `motivo_descarte`** (campo vacío o null): no inventes el motivo. Si hay pocos (uno a uno es viable), preguntale directamente al usuario: "¿por qué descartaste [título]?" y esperá la respuesta antes de sacar conclusiones sobre ese ítem — no lo uses para el análisis hasta tener el motivo real. Si hay muchos sin motivo, agrupalos por similitud (misma fuente, mismo tipo de comunicado) y preguntá por lote en vez de uno por uno.

3. **Buscar patrones**, cruzando fuente, tipo de comunicado (anuncio/protocolo/estadística/conflicto), y motivo de descarte contra los positivos:
   - ¿Hay fuentes o tipos de comunicado que casi siempre se descartan? ¿Por qué (según los motivos anotados)?
   - ¿Hay algo que el filtro base de `docs/estilo-editorial.md` no captura pero que aparece repetido en los motivos de descarte (ej. "esto ya lo cubrió tal medio", "es un anuncio demasiado chico", "es de un organismo que no seguimos de cerca")?
   - ¿Los positivos comparten algo que valga la pena nombrar como señal a favor (ej. montos grandes, cierto tipo de organismo, cierto tipo de anuncio)?

   No fuerces un patrón con pocos casos (2-3 descartes con motivos distintos no son un patrón) — un patrón real necesita repetición consistente. Ante la duda, proponéselo al usuario como hipótesis ("¿esto que veo tiene sentido como criterio, o fue casualidad?") en vez de escribirlo como regla asentada.

4. **Actualizar `docs/criterios-noticiabilidad.md`**:
   - Sumar patrones nuevos a la sección "Patrones aprendidos", cada uno con: el patrón en una línea, y el/los ejemplos concretos (título del ítem, motivo de descarte) que lo motivaron — igual criterio que la memoria de este proyecto: nunca una regla sin el caso real detrás.
   - Si un patrón nuevo contradice uno ya escrito, no lo borres en silencio — señalalo al usuario y preguntá cuál pesa más antes de resolver la contradicción vos mismo.
   - No dupliques lo que ya está en el filtro base de `docs/estilo-editorial.md` — esto es específicamente lo que se aprende con el uso, no una repetición de las reglas generales.

5. **Actualizar `skills/evaluar-comunicado/SKILL.md` una sola vez** (la primera vez que se corre esta skill) para que su paso 2 explícitamente diga "consultar también `docs/criterios-noticiabilidad.md` antes de opinar" — si esa referencia ya está, no la toques de nuevo.

6. **Reportar al final**: cuántos ítems nuevos se analizaron, qué patrones se agregaron o reforzaron, y qué quedó como hipótesis sin confirmar.

## Nota

Esto es la base para la "Opción C" de automatización descripta en `docs/arquitectura-tecnica.md` (triage automatizado a futuro) — pero hoy es puramente un documento de apoyo para que `evaluar-comunicado` sugiera mejor, no un mecanismo de decisión automática.
