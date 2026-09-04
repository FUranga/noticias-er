# Criterios de noticiabilidad (aprendidos con el uso)

Documento vivo. A diferencia de `docs/estilo-editorial.md` (cómo se escribe), esto es sobre **qué elige publicar el editor y qué no** — el criterio real de Francisco, no una regla teórica. Se actualiza con la skill `aprender-noticiabilidad`, a partir de lo que se marca `a_publicar`/`procesado` vs. `descartado` en `data/backlog.json` (con su `motivo_descarte` cuando está anotado).

**Esto es material de apoyo para `evaluar-comunicado`, nunca una regla que decida sola.** La decisión de noticiabilidad sigue siendo siempre del editor — ver `CLAUDE.md`. Este documento sirve para que las sugerencias de `evaluar-comunicado` se parezcan cada vez más a cómo piensa Francisco, no para automatizar la decisión.

## El criterio central (2026-09-04, definido por Francisco)

Lo que hace que algo sea publicable no es que tenga un dato duro o un organismo detrás — es que sea **relevante**: información que la gente quiera saber o que le sea útil, objetiva y verdadera. En la práctica, esto se traduce en cuatro preguntas — no hace falta que un ítem cumpla las cuatro, pero cuantas más cumpla, más fuerte el caso:

1. **¿Es noticioso?** ¿Cambió algo, o es la enésima foto de una actividad de rutina? Un comunicado puede tener cifras y seguir sin ser noticia si no representa un cambio de estado real.
2. **¿Es importante?** ¿Afecta a mucha gente, mueve montos grandes, o es una decisión con consecuencias reales — a diferencia de algo protocolar o de alcance muy acotado?
3. **¿Es oportuno (timely)?** ¿Es información fresca, o es un re-empaquetado de algo que ya se sabía (aunque el comunicado lo presente como novedad)?
4. **¿Es útil o sorprendente?** ¿El lector puede hacer algo distinto con esta información, o le cambia lo que entendía de la situación? Si no pasa ninguna de las dos, probablemente es relleno aunque esté bien escrito.

**Filtro base** (de `docs/estilo-editorial.md`) — señales de que un comunicado probablemente **no** es noticia:
- Protocolo puro (acto, efeméride, saludo) sin decisión, anuncio o dato nuevo.
- Repite un anuncio ya cubierto sin dato adicional.
- Sin hecho concreto identificable (organismo + acción + al menos un dato duro).

**Importante: tener un dato duro no alcanza por sí solo** si el comunicado no pasa las cuatro preguntas de arriba — ver el patrón "programa en curso" abajo, que es exactamente ese caso.

## Preguntas abiertas (para pensar, no resueltas todavía)

- **Analizar la fuente audiovisual primaria en sí, no solo el comunicado escrito que la resume.** Aplica no solo a conferencias de prensa — también a audiencias públicas, reuniones de gobierno y sesiones legislativas (Cámara de Diputados, Senado, Concejo Deliberante) cuando estén grabadas o transmitidas. El comunicado/acta es una versión curada de lo que pasó — puede que se le escape (o se omita a propósito) algo que sí está en el video/audio/transcripción original: una negativa a responder algo, una admisión, una pregunta incómoda, un desacuerdo en el recinto que no queda en el resumen oficial. No implementado — requiere conseguir el material original (muchas legislaturas transmiten sus sesiones en vivo o las archivan) y evaluar cuándo conviene el esfuerzo de revisarlo (probablemente casos de conflicto o alto interés, no de forma sistemática para todo). Sería una capa de cobertura fuerte incluso antes de tener periodistas propios en el territorio (ver "Etapa 4" en `docs/vision-y-etapas.md`) — no depende de estar presente, solo de acceso a la grabación.
- **¿Hace falta una sección de "servicio" separada de las noticias?** Cosas como alertas climáticas, cortes de calle, cambios de trámites — pueden ser útiles para el lector sin ser "noticia" en el sentido de este medio (no son política/economía institucional, no tienen el mismo estándar de hecho verificable con dato duro). `docs/vision-y-etapas.md` ya prevé algo parecido para agenda cultural en etapa 2 ("como servicio informativo, no como cobertura editorial"). Evaluar si conviene un formato/sección aparte con criterio propio (utilidad/oportunidad, no noticiabilidad) en vez de mezclarlo con la portada de noticias — no implementar todavía, solo señalado.

## Patrones aprendidos

- **Un programa en curso puede ser noticia sin que cada visita/hito dentro de él lo sea.** Caso motivador (2026-09-04): el plan de Enersa contra conexiones eléctricas clandestinas es una historia real (recupera ingresos, atiende una inequidad tarifaria, ya alcanzó 1.000 hogares regularizados en Paraná — eso se cubrió en mayo de 2026). Un comunicado sobre una visita de funcionarios a un barrio más dentro de ese mismo programa, meses después, **no es noticia por sí sola** — no hay dato nuevo, es el calendario de prensa del gobierno, no un cambio de estado. Reformular el título en tono interpretativo (en vez de repetir cifras del comunicado) no alcanza si la pregunta 1 y 3 de arriba ("¿cambió algo? ¿es oportuno?") siguen dando negativo.
  - **Qué sí sería noticia dentro del mismo programa**: un hito redondo nuevo (ej. llegar a 2.000 hogares), una cifra de impacto no difundida antes (plata recuperada, no solo usuarios), una voz crítica, o un problema de ejecución — cualquier cosa que sea información nueva, no una repetición del marco ya conocido.
  - **Tratamiento recomendado**: en vez de una nota por cada visita/barrio, una nota de seguimiento periódica que actualice el estado completo del programa (cada varios meses, o cuando haya un hito real).

- **Una reacción de un funcionario a un hecho ya confirmado no es noticia por sí sola — salvo que la reacción misma traiga algo nuevo.** Caso motivador (2026-09-04): un comunicado con una declaración de un funcionario celebrando una decisión ajena (la relocalización de una planta, decidida por otro gobierno) no pasa el filtro si es pura autocelebración sin dato nuevo. **Pero si la reacción implica algo por sí misma** — un anuncio propio, una negativa a reconocer algo, un cambio de postura — ahí sí puede ser noticia, con la reacción como eje. La pregunta clave: ¿la declaración agrega información que no existía antes, o solo reacciona a algo que ya se sabía?
- **Ojo con la oportunidad (timing) al armar una historia a partir de una reacción tardía.** Mismo caso: el hecho de fondo (la relocalización) lo confirmó Uruguay el 2/9 y lo cubrieron medios grandes (Infobae, La Nación, Perfil) ese mismo día. La reacción del gobierno provincial llegó recién el 3/9, y para cuando se investigó y redactó (4/9) la historia ya tenía dos días y estaba sobreexpuesta — no pasaba el criterio de oportunidad aunque sí el de importancia. **Chequear la fecha real del hecho antes de invertir tiempo en investigar y redactar**, no después — si el hecho de fondo ya tiene más de un día y fue ampliamente cubierto, probablemente no vale la pena salvo que haya un ángulo local genuinamente nuevo que nadie más tenga.

*(Se sigue completando con `aprender-noticiabilidad` sobre descartes reales y con casos discutidos en sesión, como los de arriba.)*

## Próxima actualización

Correr `aprender-noticiabilidad` cuando haya un lote nuevo de ítems `descartado`/`procesado` sin analizar todavía — no hace falta esperar un volumen enorme, con 5-10 descartes nuevos ya vale la pena revisar si hay un patrón.
