---
name: mapear-fuentes
description: Investiga y agrega organismos/organizaciones nuevas al mapa de fuentes de Agencia Entrerriana (docs/fuentes.md) — gobierno provincial, Legislatura, Municipalidad de Paraná, Concejo Deliberante, cámaras empresarias, sindicatos, ONGs, universidades, medios locales. También audita periódicamente el listado existente para detectar links caídos o portales que cambiaron. Usar cuando el usuario menciona una organización que no está en el listado y pide sumarla, o pide "revisar que las fuentes sigan vigentes".
---

# Mapear y mantener el listado de fuentes

Contexto: `docs/fuentes.md` es el registro de organismos y organizaciones a monitorear para la cobertura reactiva de `Agencia Entrerriana` (ver `docs/vision-y-etapas.md`). Es la base de la que se alimenta el triage editorial (`evaluar-comunicado`) — si una fuente relevante no está mapeada, sus comunicados directamente no entran al flujo.

## Agregar una fuente nueva

1. **Confirmar la categoría** (usar las mismas de `docs/fuentes.md`: Gobierno provincial, Legislatura de Entre Ríos, Municipalidad de Paraná, Concejo Deliberante de Paraná, Organizaciones privadas/empresarias, Sindicatos, ONGs e instituciones académicas, Medios locales). Si la organización no encaja bien en ninguna, proponé sumar una categoría nueva en vez de forzarla — y avisá al usuario antes de crearla.

2. **Buscar su canal de comunicados/prensa** (WebSearch/WebFetch): portal de noticias/prensa propio, sección de comunicados, o — si no tiene nada formal — su cuenta de redes sociales principal (a falta de mejor opción, es válido registrar eso, pero dejarlo marcado como "sin portal de prensa formal, monitorear redes").

3. **Verificar si tiene RSS.** No asumas que existe — confirmalo accediendo a la URL candidata (`/feed`, `/rss`, etc.) o buscando el link de feed en el HTML de la página. Si no lo encontrás con confianza razonable, escribí explícitamente "sin RSS confirmado" en vez de una URL adivinada.

4. **No inventes URLs.** Si no encontrás con certeza razonable el portal de prensa de una organización, decilo así ("no confirmado, revisar manualmente") en vez de completar el campo con una URL que parece plausible pero no verificaste.

5. **Agregar la entrada** a `docs/fuentes.md` en la categoría correspondiente, con el mismo formato que las entradas existentes (nombre, URL, RSS si existe o "no confirmado").

## Auditar el listado existente

Cuando el usuario pida revisar que las fuentes sigan vigentes:

1. Recorrer las entradas de `docs/fuentes.md` (podés acotar a una categoría si el usuario lo pide, o a las marcadas "no confirmado" primero — son las que más probablemente necesitan trabajo).
2. Para cada una, verificar con WebFetch que la URL sigue resolviendo y sigue siendo la sección de prensa/comunicados correcta (los sitios de organismos públicos cambian de estructura seguido).
3. Si una URL cambió o dejó de funcionar, actualizarla; si la organización ya no existe o se fusionó con otra, señalarlo al usuario en vez de borrar la entrada en silencio.
4. Reportar al final cuántas se revisaron, cuántas se corrigieron y cuántas quedaron marcadas para revisión manual.

No hace falta reauditar todo el listado en cada pasada — priorizar lo marcado como "no confirmado" y lo que no se revisó hace más tiempo.
