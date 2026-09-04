---
name: evaluar-comunicado
description: Resume uno o varios comunicados/novedades entrantes (de gobierno, Legislatura, Concejo Deliberante, cámaras empresarias, sindicatos, ONGs, universidades) en formato corto para que el editor decida rápido cuáles vale la pena convertir en noticia. NO decide qué es noticiable — esa decisión es siempre del editor humano (Francisco Uranga). Usar cuando el usuario pega varios comunicados o links y pide "ayudame a triagear esto", "cuáles de estos valen la pena", o similar, ANTES de pedir la reescritura completa (para eso, `redactar-noticia`).
---

# Evaluar comunicados para triage editorial

Contexto: `[NOMBRE DEL MEDIO]` funciona como una agencia (ver `docs/vision-y-etapas.md`) — recibe comunicados de muchas fuentes y el editor tiene que decidir rápido cuáles reescribir. Con volumen (varios comunicados por día de distintos organismos), leer cada uno entero para decidir es lento. Esta skill arma un resumen de triage: no reescribe la noticia, ayuda a decidir si vale la pena reescribirla.

**Esta skill no reemplaza el criterio editorial.** Da un resumen y una observación, nunca una decisión tomada — el formato de salida siempre deja la decisión al usuario.

## Proceso

1. **Para cada comunicado/link recibido**, leer (o WebFetch si es un link) y extraer:
   - Organismo/organización emisora.
   - El hecho concreto, en una oración, separado del relato institucional (ver tabla de "comunicadoñol" en `docs/estilo-editorial.md`).
   - Si es anuncio de algo futuro o hecho ya consumado.
   - Si trae al menos un dato duro (cifra, fecha, monto, alcance) o es pura declaración de intenciones sin sustancia.

2. **Señalar por qué podría importar (o no) para la cobertura de desarrollo económico/política institucional** — sin decidir por el usuario. Ejemplos de lo que hace que algo sea más relevante: montos de inversión, empleo, cambios normativos con impacto económico, conflictos entre organismos/sectores, decisiones con efecto directo en la actividad productiva local. Ejemplos de lo que probablemente no amerita nota propia: efemérides/aniversarios sin dato nuevo, actos protocolares sin anuncio de fondo, reafirmaciones genéricas de compromiso sin acción concreta. **Consultá también `docs/criterios-noticiabilidad.md`** antes de opinar — tiene el criterio central (las cuatro preguntas: noticioso / importante / oportuno / útil o sorprendente) y patrones específicos aprendidos de lo que este editor viene descartando/publicando en la práctica (mantenido por la skill `aprender-noticiabilidad`), más afinado que el filtro genérico de arriba.

3. **Leer contra el grano, no solo el ángulo que ofrece la fuente.** Antes de resumir el ángulo principal del comunicado, revisar:
   - ¿Hay un **segundo ángulo** dentro del mismo texto, más noticioso que el que la fuente eligió destacar? A veces se les escapa un dato que reconoce un problema, un retraso, un conflicto, o una negativa a confirmar algo — cosas que no aparecerían si el comunicado estuviera bien controlado. Señalarlo aparte del ángulo principal si aparece.
   - ¿El comunicado parece estar **reencuadrando o desviando el foco** de otra cosa? (mucho énfasis en un ángulo secundario, silencio llamativo sobre algo esperable).
   - Si hay una **mención suelta** (nombre, cifra, situación) que sugiere una historia propia sin estar desarrollada: buscar primero si ya hay repercusión en otro lado (puede alcanzar para armar la nota ya); si no, anotarla en `docs/temas-a-seguir.md` en vez de perderla.

4. **Marcar duplicados o continuaciones**: si dos comunicados del lote parecen ser sobre el mismo hecho (dos organismos comunicando lo mismo desde ángulos distintos, o una continuación de algo ya cubierto), señalarlo explícitamente en vez de tratarlos como ítems independientes.

5. **Formato de salida**, por cada ítem:
   ```
   [Organismo] — [link o "sin link"]
   Hecho: [una oración, sin relleno institucional]
   Tipo: anuncio futuro | hecho consumado | contexto/estadística
   Dato duro: sí (cuál) | no
   Nota: [por qué podría importar o no — una línea, sin decidir]
   ```
   Al final del lote, si hay ítems que parecen la misma historia, agregar una línea aparte señalando cuáles.

6. **No reescribas la noticia en este paso.** Si el usuario quiere avanzar con uno o más ítems del lote, señalale que puede pedir la reescritura completa con la skill `redactar-noticia` sobre esos ítems puntuales.
