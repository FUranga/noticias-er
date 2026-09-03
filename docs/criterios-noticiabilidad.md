# Criterios de noticiabilidad (aprendidos con el uso)

Documento vivo. A diferencia de `docs/estilo-editorial.md` (cómo se escribe), esto es sobre **qué elige publicar el editor y qué no** — el criterio real de Francisco, no una regla teórica. Se actualiza con la skill `aprender-noticiabilidad`, a partir de lo que se marca `a_publicar`/`procesado` vs. `descartado` en `data/backlog.json` (con su `motivo_descarte` cuando está anotado).

**Esto es material de apoyo para `evaluar-comunicado`, nunca una regla que decida sola.** La decisión de noticiabilidad sigue siendo siempre del editor — ver `CLAUDE.md`. Este documento sirve para que las sugerencias de `evaluar-comunicado` se parezcan cada vez más a cómo piensa Francisco, no para automatizar la decisión.

## Filtro base (punto de partida, de `docs/estilo-editorial.md`)

Señales de que un comunicado probablemente **no** es noticia:
- Protocolo puro (acto, efeméride, saludo) sin decisión, anuncio o dato nuevo.
- Repite un anuncio ya cubierto sin dato adicional.
- Sin hecho concreto identificable (organismo + acción + al menos un dato duro).

## Patrones aprendidos

*(Vacío todavía — se completa la primera vez que corra `aprender-noticiabilidad` sobre descartes reales. Cada patrón nuevo va con al menos un ejemplo concreto que lo motivó, no como regla abstracta suelta.)*

## Próxima actualización

Correr `aprender-noticiabilidad` cuando haya un lote nuevo de ítems `descartado`/`procesado` sin analizar todavía — no hace falta esperar un volumen enorme, con 5-10 descartes nuevos ya vale la pena revisar si hay un patrón.
