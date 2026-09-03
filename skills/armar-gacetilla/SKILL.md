---
name: armar-gacetilla
description: Convierte una nota o novedad de FUNDER (ya publicada en desarrolloentrerriano.org, o un borrador todavía sin publicar) en una gacetilla de prensa profesional lista para enviar a periodistas. Usar cuando el usuario pide "armame una gacetilla", "esto lo quiero mandar a los medios", o pega/linkea contenido de FUNDER pidiendo convertirlo en comunicado de prensa. No confundir con `redactar-noticia`: esa skill reescribe comunicados de OTROS organismos para el medio; esta skill redacta un comunicado DE FUNDER hacia afuera, para que otros medios lo publiquen.
---

# Armar gacetilla de prensa de FUNDER

FUNDER (Fundación para el Desarrollo Entrerriano) a veces quiere que su propia actividad —una
publicación, un informe, un evento, una declaración— llegue a otros medios de Entre Ríos. Esta skill
toma ese contenido y lo convierte en una gacetilla con el formato que un periodista espera recibir,
lista para que el editor la revise y decida enviarla. **Nunca se envía sola** — el resultado es
siempre un borrador para aprobación editorial, igual que el resto de las skills de este repo (ver
`CLAUDE.md`).

## Proceso

1. **Conseguir el contenido de origen.** El usuario puede pasar:
   - Un link a una nota ya publicada en `desarrolloentrerriano.org` (usar descarga de HTML crudo +
     extracción del contenedor real del artículo — **nunca WebFetch**, mismo criterio que
     `docs/sitio-fundacion.md` para cualquier contenido de ese sitio).
   - El texto de un borrador todavía no publicado.
   - Una descripción suelta de lo que pasó (un evento, un anuncio) que hay que convertir en texto.

2. **Preguntar por el embargo, siempre, antes de redactar el encabezado:**
   - "¿Esto está embargado? Si sí, ¿hasta qué fecha y hora se puede publicar?"
   - Si el usuario dice que no hay embargo (o no contesta y el contexto deja claro que es algo ya
     público), el encabezado dice **"PARA DIFUSIÓN INMEDIATA"**.
   - Si hay embargo, el encabezado dice **"EMBARGADO HASTA [fecha y hora exacta que indique el
     usuario]"** — nunca asumas una fecha de embargo, tiene que ser la que te den.

3. **Identificar el ángulo noticioso**, no institucional: igual que `redactar-noticia`, separá el
   hecho concreto (qué pasó, qué se publicó, qué se dijo) de la autopromoción. Una gacetilla que un
   periodista puede levantar casi tal cual tiene título de noticia, no de folletería — "FUNDER publicó
   un informe sobre X que encontró Y", no "FUNDER continúa su compromiso con el desarrollo de la
   provincia".

4. **Redactar con esta estructura fija:**

   ```
   [PARA DIFUSIÓN INMEDIATA / EMBARGADO HASTA ...]

   [TÍTULO — noticioso, no institucional]

   Paraná, Entre Ríos, [fecha]. — [Bajada/lead: el hecho principal en 1-2 oraciones, quién-qué-cuándo-dónde]

   [Cuerpo en 2-4 párrafos cortos, pirámide invertida. Si hay una cita de un vocero de FUNDER
   disponible en el material de origen, incluirla atribuida por nombre y cargo. Si no hay cita y el
   contenido la pediría, señalalo al usuario en vez de inventarla.]

   Acerca de FUNDER:
   La Fundación para el Desarrollo Entrerriano es una organización sin fines de lucro que trabaja
   investigando y estudiando la realidad provincial y generando propuestas para promover el
   desarrollo de Entre Ríos. Inspirada en las ideas y la obra de gobierno de Raúl Uranga (gobernador
   de Entre Ríos entre 1958 y 1962), cumple la función de rendirle homenaje y mantener viva su
   memoria.

   Contacto de prensa:
   Nicolás Loza, Coordinador FUNDER
   Tel: 3434054369
   Email: funderru@gmail.com

   -30-
   ```

   El contacto es siempre Nicolás Loza salvo que el usuario indique explícitamente otro contacto para
   ese envío puntual (ver `docs/prensa-fundacion.md`). El boilerplate "Acerca de FUNDER" es el mismo
   en toda gacetilla salvo que el usuario pida cambiarlo.

5. **No inventar datos.** Si falta una cifra, una cita o un dato que la gacetilla necesitaría para ser
   creíble, señalalo en vez de completarlo — mismo criterio que el resto del proyecto (`CLAUDE.md`).

6. **Envío a periodistas — todavía no implementado.** El siguiente paso natural es mandar la gacetilla
   a una lista de contactos de prensa, pero esa lista y el mecanismo de envío no están armados
   todavía (ver `docs/prensa-fundacion.md`). Por ahora esta skill solo entrega el texto de la
   gacetilla lista para que el editor la copie y la envíe él mismo, o para pegarla en el próximo paso
   cuando el envío esté resuelto. No intentes enviar el mail vos mismo ni inventar destinatarios.

Resultado siempre: un borrador de texto para revisión editorial, nunca un envío.
