---
name: evaluar-boletin
description: Resume en limpio los ítems "pendiente" del Boletín Oficial de Entre Ríos cargados por pipeline/monitorear_boletin_er.py (leyes, decretos, resoluciones, licitaciones) y señala si parecen tener ángulo noticioso potencial — sin decidir nada. Distinto de evaluar-comunicado: acá el material es texto legal seco, sin ángulo pre-armado, así que primero hay que traducirlo. Usar cuando el usuario pide "qué hay en el boletín", "resumime el boletín", "evaluá los pendientes del boletín" o similar.
---

# Evaluar pendientes del Boletín Oficial

Contexto: `pipeline/monitorear_boletin_er.py` carga a `data/backlog.json` (estado `pendiente`, `fuente: "Boletín Oficial de Entre Ríos"`) las normas que sobreviven un filtro puramente mecánico — no hay ningún juicio editorial en ese paso, solo descarte de categorías estructuralmente sin chance de ser noticia (ver `docs/boletin-oficial-proceso.md`). Esta skill es el primer paso con juicio editorial: un triage rápido para que el editor decida entre tres caminos — marcar `a_publicar` (alcanza con investigación breve), marcar `a_investigar` (tema de fondo, más de un día de reporteo) o descartar — sin tener que leer cada decreto entero.

**Esta skill no decide ni investiga.** Es el equivalente de `evaluar-comunicado` pero para material legal en vez de comunicados de prensa — dejá la decisión al editor. Un ítem marcado `a_publicar` sigue el camino normal de `procesar-cablera`. El siguiente paso después de que algo se marca `a_investigar` es una skill separada (`investigar-boletin`, todavía no construida) que sí hace el reporteo real.

## Diferencia con `evaluar-comunicado`

Un comunicado de prensa ya viene con un ángulo elegido por quien lo emite (aunque haya que descontarle el relato institucional). Un ítem del Boletín es texto legal seco — no hay "ángulo" hasta que alguien lo traduce. Por eso el proceso acá tiene un paso extra al principio: traducir antes de evaluar.

## Proceso

1. **Leer `data/backlog.json`** y filtrar los ítems con `"fuente": "Boletín Oficial de Entre Ríos"` y `"estado": "pendiente"`. Si el usuario pide un subconjunto (ej. "solo las licitaciones", "lo de hoy"), acotar ahí. Si no hay ninguno, avisar y no hacer nada más.

2. **Para cada ítem, traducir el texto legal a una oración clara** antes de opinar nada:
   - ¿Qué organismo actúa?
   - ¿Qué hace concretamente? (sin "vistos" ni "considerandos" — la acción real: aprueba, contrata, designa, rechaza, convoca)
   - ¿Hay un dato duro? (monto, plazo, alcance, a quién afecta)
   - El campo `titulo` ya viene armado como `[Organismo] Título del Sumario` — no lo repitas literal, es un punto de partida, no el resumen final.

3. **Aplicar las cuatro preguntas de `docs/criterios-noticiabilidad.md`** (noticioso / importante / oportuno / útil o sorprendente) sobre el hecho ya traducido — no sobre el texto legal crudo. Consultar también **`docs/boletin-oficial-proceso.md`, sección "Qué buscar al triagear un ítem"**, que tiene señales específicas por tipo de norma (decreto/ley/resolución/licitación) y se va actualizando con casos reales — más afinado que el filtro genérico para este tipo de material.

   **Nombramientos, ceses y renuncias**: aplicar el chequeo específico de `docs/boletin-oficial-proceso.md`, sección "Foco específico: nombramientos, ceses y renuncias" — nivel del cargo, si es llegada o salida, si el decreto da motivo, antecedentes de conflicto. La gran mayoría es rutina; el objetivo es no dejar pasar en silencio la excepción (cargo de peso, salida sin explicación, algo que no se conocía por otra vía).

4. **Señalar explícitamente cuál de los tres caminos corresponde, y por qué**:
   - **`a_publicar`**: alcanza para nota con poco reporteo adicional (raro, pero pasa con licitaciones bien documentadas o resoluciones de impacto directo tipo tarifas).
   - **`a_investigar`**: candidato a investigación más larga, no a redacción directa (el caso más común, sobre todo leyes y decretos de fondo — ver el ejemplo del "Norte Entrerriano" en `docs/boletin-oficial-proceso.md`): señalar qué habría que averiguar (quién lo impulsó, antecedentes, si hay voces críticas) para que se convierta en nota real.
   - **Descartar**: si no se identifica ángulo claro, decilo así en vez de forzar uno.

5. **Usar la `prioridad` que ya viene tageada por el script (alta/media/baja) como primera señal, no como veredicto** — está calculada mecánicamente (ver `docs/boletin-oficial-proceso.md`) y puede no capturar todo. Está bien confirmarla, matizarla o contradecirla en el resumen si el contenido real lo justifica.

6. **Registrar plazos o fechas concretas en `data/agenda.json`** cuando aparezcan (ver `docs/agenda.md`) — típicamente la fecha de apertura de una licitación, o un plazo/vencimiento mencionado en un decreto. Igual que en `evaluar-comunicado`, es independiente de si el ítem termina siendo noticia.

7. **Formato de salida**, por cada ítem:
   ```
   [Tipo: Ley | Decreto | Resolución | Licitación] [Organismo] — [link]
   Qué dice: [una oración clara, sin jerga legal]
   Dato duro: [monto/plazo/alcance] | ninguno
   Prioridad del script: alta | media | baja
   Ángulo potencial: [cuál, y qué habría que investigar] | no se identifica ángulo claro
   Sugerencia: a_publicar | a_investigar | descartar
   ```
   Al final del lote, señalar cuáles parecen más prometedores para revisar primero (no necesariamente los de prioridad "alta" del script — la lectura del contenido puede cambiar eso).

8. **No redactes nada en este paso.** Si el usuario quiere avanzar con un ítem puntual una vez marcado `a_investigar` desde el panel, eso es trabajo de la futura skill `investigar-boletin` — no de esta. Un ítem marcado `a_publicar` sigue el camino normal de `procesar-cablera`, sin paso intermedio.

## Cómo evoluciona esta skill

Cuando el editor dé feedback sobre un resumen (algo que parecía interesante no lo era, o al revés), sumar el caso concreto a `docs/boletin-oficial-proceso.md` (sección "Qué buscar al triagear un ítem") — mismo criterio que `aprender-noticiabilidad` sobre `docs/criterios-noticiabilidad.md`: nunca una regla nueva sin el ejemplo real detrás.
