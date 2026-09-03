# Estilo editorial

Referencia: Bloomberg / WSJ. Notas cortas, directas, sin relleno. El lector tiene que entender el hecho principal en la primera oración, sin tener que llegar al tercer párrafo.

Este documento es la referencia compartida para las skills `redactar-noticia` y `evaluar-comunicado`. No lo dupliques dentro de las skills — linkealo.

## El problema específico de este dominio

A diferencia de una nota de despidos (hecho concreto, verificable, con una empresa como sujeto), acá la materia prima principal son **comunicados institucionales** — de gobierno, legislatura, cámaras empresarias, sindicatos. Ese tipo de texto viene con un sesgo estructural: está escrito para hacer quedar bien a quien lo emite. Nuestro trabajo no es transcribirlo con otras palabras — es **separar el hecho verificable del relato que lo envuelve**, y dejar bien claro qué es dato y qué es la versión de quien lo dice.

## Reglas de título

- **Sujeto + acción + dato principal, en ese orden.** El sujeto es el actor real del hecho (el organismo, la empresa, la persona), no una descripción abstracta ("Gobierno anuncia..." está bien si el gobierno es efectivamente quien actúa; "Se anunció..." en voz pasiva sin sujeto, no).
- **Voz activa. Sin adjetivos calificativos** ("histórico", "contundente", "sin precedentes") salvo que sean del propio hecho y no una opinión sobre él.
- Sin mayúsculas de énfasis, sin signos de exclamación, sin preguntas retóricas.
- **Cifras exactas, no vagas**: si el comunicado da un número, usalo ("120 puestos de trabajo", no "numerosos puestos").
- **Aposición descriptiva solo si hace falta para identificar al sujeto** — si ya es reconocible (el gobernador, la Legislatura, un organismo conocido), no hace falta explicarlo en el título; si es una entidad menos conocida, sumá lo mínimo para ubicarla.
- **Nada de afirmaciones sin dato concreto detrás.** Si el comunicado dice que una medida "va a dinamizar la economía regional" sin ninguna cifra o mecanismo concreto, esa frase no entra al título — es relato, no dato.
- **Moneda siempre en letras**: "1.200 millones de pesos", nunca "$1.200 millones" ni "u$s".
- **Anuncio vs. hecho consumado — distinción central en este dominio.** Un comunicado de gobierno frecuentemente anuncia una intención futura ("se pondrá en marcha", "prevé", "el plan contempla"), no un hecho ya ocurrido. El título tiene que reflejar cuál es: "El gobierno anunció un plan de..." es distinto de "El gobierno lanzó...", y ambos son distintos de "El gobierno destinó/pagó/entregó...". No uses un verbo de hecho consumado para lo que todavía es una promesa.

## Traducir el "comunicadoñol"

Los comunicados institucionales tienen un vocabulario propio que no es el de una noticia. Traducilo a lenguaje directo:

| Comunicadoñol | Noticia |
|---|---|
| "en el marco de..." | eliminar, o reemplazar por el hecho concreto |
| "con el objetivo de fortalecer/potenciar/impulsar..." | decir qué se hace concretamente, no la intención declarada |
| "se llevó a cabo una reunión de trabajo..." | quién se reunió con quién, y para qué (si hay un resultado concreto, eso va primero) |
| "en pos de..." | eliminar |
| "una nueva e importante herramienta para..." | describir qué hace la herramienta, sin el adjetivo de valor |
| "reafirmó su compromiso con..." | generalmente no es noticia por sí sola — buscar si hay una acción concreta detrás |

Si después de sacar el relleno institucional no queda un hecho concreto, probablemente no es una noticia — es una nota de color o directamente prensa sin sustancia (ver skill `evaluar-comunicado`).

## Atribución — la regla más importante de este dominio

**Todo logro, cifra de impacto o causa que venga de la fuente y no de una verificación independiente tiene que quedar explícitamente atribuido a esa fuente.** No como hecho objetivo del medio.

- "El proyecto generará 300 empleos, según el Ministerio de Producción" — no "El proyecto generará 300 empleos."
- "La medida busca reducir la informalidad laboral, de acuerdo con la Legislatura" — no presentarlo como un resultado ya verificado.
- Si dos organismos dan versiones distintas de un mismo hecho (por ejemplo, gobierno y sindicato sobre el mismo conflicto), no elegir una versión en silencio — mostrar ambas, atribuidas.

Esto es el corazón del valor editorial: cualquiera puede copiar un comunicado. Nuestro trabajo es dejar claro qué es verificable y qué es la versión de quien lo emitió.

## Bajada y cuerpo

- **Bajada**: una o dos oraciones con lo más relevante que no entró en el título (quién más participa, cifras adicionales, próximos pasos, plazos). No repite el título con otras palabras.
- **Cuerpo en pirámide invertida**: el dato más importante arriba, el contexto y detalle secundario después. Sin introducción genérica ("En el día de la fecha, en un acto realizado en...") — eso va, si acaso, al final como dato de color.
- **Sin acumular protocolo**: no hace falta detallar la lista completa de funcionarios presentes en un acto salvo que sea relevante para el hecho. Priorizar qué pasó y a quién afecta.
- **Cierre con fuente**: cada nota termina indicando de dónde sale la información ("Fuente: comunicado de prensa de [organismo]" o "Fuente: [organismo], consultado por [nombre del medio]" una vez que haya verificación directa).
- **No inventar datos faltantes.** Si el comunicado no da una cifra o fecha, no se la inventa — se escribe con lo que hay, y si hace falta, se señala qué dato falta para el editor.

## Extensión

Corta. Un comunicado normal debería resultar en una nota de 3 a 6 párrafos cortos. Si el hecho es mayor (un anuncio de política pública grande, un conflicto relevante), puede ser más larga, pero la regla por defecto es Bloomberg-corto, no crónica extensa.

## Medios y empresas como fuente (no solo comunicados)

El mapa de fuentes (`fuentes.md`) también va a incluir monitoreo de medios (nacionales y locales) y de empresas relevantes a nivel local (presentaciones regulatorias, causas judiciales, prensa especializada). El estándar de atribución acá es más exigente que con un comunicado institucional:

- **Un comunicado es información pública que cualquiera puede reescribir.** Una nota original de otro medio — una investigación, un dato que consiguieron ellos — no. Si el dato central lo consiguió otro medio y no lo verificamos de forma independiente, se atribuye de forma explícita y prominente en el cuerpo ("según publicó [medio], ..."), no con un link al pasar al final.
- **Usar la cobertura ajena como disparador, no como producto final.** El aporte propio es sumar contexto local o confirmar con la fuente primaria (el organismo o la empresa), no una versión corta del artículo ajeno. Si no hay nada que agregar, alcanza con una mención breve o un link, no una nota propia.
- **Cuanto más chico el medio de origen, más cuidado.** Reescribir sin agregar nada propio le saca tráfico a un actor con menos recursos que nosotros — y va en contra del principio de "agencia, no repetición" (`vision-y-etapas.md`). Ante la duda con un medio hiperlocal, mejor linkear que reescribir.
- **Empresas locales**: para hechos societarios (presentaciones regulatorias, causas judiciales, inversiones), preferir el documento público original cuando exista, citándolo directamente, antes que solo la nota de prensa especializada que lo resume.

## Cómo evoluciona este documento

Estas reglas van a afinarse con el uso real — cuando aparezcan casos límite (comunicados ambiguos, conflictos de versiones, jerarquía de fuentes cuando haya más de una por hecho), documentalos acá con un ejemplo concreto, siguiendo el mismo criterio con el que se armó el estilo del proyecto hermano `despidos-tracker`.
