---
name: redactar-noticia
description: Reescribe un comunicado de prensa u otra información de origen (gobierno provincial, Municipalidad de Paraná, Legislatura, Concejo Deliberante, cámaras empresarias, sindicatos, ONGs, universidades) como una noticia corta en estilo Bloomberg/WSJ para Agencia Entrerriana. Se usa DESPUÉS de que el editor ya decidió que el comunicado es noticiable — esta skill no decide qué publicar, solo reescribe lo que ya fue seleccionado. Usar cuando el usuario pega un comunicado, un link, o pide "redactar esto como noticia" / "convertir este comunicado en nota".
---

# Redactar noticia a partir de un comunicado

Contexto del proyecto: `Agencia Entrerriana` cubre política y economía institucional de Paraná/Entre Ríos, con foco inicial en desarrollo económico (ver `docs/vision-y-etapas.md`). Funciona como una agencia: el editor (Francisco Uranga) elige qué comunicados son noticiables; esta skill toma esa elección y la convierte en una nota lista para revisión editorial, no en un post publicado — el resultado siempre es un borrador para que el editor revise antes de publicar.

Las reglas de estilo completas están en `docs/estilo-editorial.md`. Este documento no las repite — las aplica.

## Proceso

1. **Conseguir el material fuente.** El usuario puede pasar el texto del comunicado directamente, un link (usar WebFetch), o una captura/descripción. Si es un link y el fetch trae poco contenido, pedí el texto completo en vez de reescribir sobre datos incompletos.

2. **Identificar el hecho verificable vs. el relato institucional.** Antes de escribir una palabra, separá:
   - ¿Qué pasó, concretamente? (una medida, una cifra, una firma, un anuncio, una sesión, una resolución)
   - ¿Qué es interpretación o valoración de quien emite el comunicado? (impacto esperado, adjetivos, intenciones declaradas)
   - ¿Es un hecho ya consumado o un anuncio de algo futuro? Ver la distinción en `docs/estilo-editorial.md` — no uses verbo de hecho consumado para una promesa.

3. **Filtro de calidad mínimo — antes de redactar, confirmá que hay una noticia real:**
   - ¿Hay una acción o decisión concreta identificable, más allá del lenguaje de relaciones públicas?
   - ¿Hay al menos un dato duro (cifra, fecha, monto, alcance)?
   - Si después de sacar el "comunicadoñol" (ver tabla en `docs/estilo-editorial.md`) no queda nada concreto, decíselo al usuario en vez de forzar una nota vacía — puede ser que el comunicado no pase el filtro aunque el editor ya lo haya marcado como candidato; señalalo, no lo descartes vos mismo sin avisar.

4. **Redactar siguiendo `docs/estilo-editorial.md`:**
   - Título: sujeto + acción + dato principal.
   - Bajada: uno o dos oraciones con lo más relevante que no entró en el título.
   - Cuerpo: pirámide invertida, corto (3-6 párrafos para un comunicado estándar).
   - Atribución explícita de todo dato de impacto/logro/causa que venga de la fuente y no de verificación propia — tejida en el cuerpo ("según informó...", "de acuerdo con..."), nunca como una línea "Fuente:" separada al final (no es periodístico).
   - Moneda en letras, sin adjetivos calificativos, sin relleno de protocolo.

5. **No inventes lo que falta.** Si el comunicado no trae una cifra, fecha o dato que el título necesitaría, escribí con lo que hay y señalá explícitamente al usuario qué dato falta — no lo completes con una suposición razonable, aunque parezca obvia.

6. **Si el comunicado da una sola versión de un conflicto** (por ejemplo, una medida que un sindicato podría ver distinto), señalalo al usuario como nota aparte al final de tu respuesta — no hace falta salir a buscar la otra versión vos mismo salvo que el usuario lo pida, pero sí avisar que existe ese ángulo.

7. **Formato de salida:**
   ```
   Título: ...

   Bajada: ...

   [Cuerpo en párrafos cortos, con la atribución de cada dato tejida adentro]
   ```
   Si el comunicado no pasó el filtro de calidad del paso 3, no fuerces este formato — explicá qué falta, en una o dos líneas, para que el editor decida si igual quiere una nota con lo que hay o descarta el ítem.

Este resultado es un borrador para revisión editorial, no una publicación. La decisión de publicar y la edición final quedan siempre en manos del editor humano.
