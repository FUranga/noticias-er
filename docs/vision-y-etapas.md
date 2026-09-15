# Visión y etapas

## Qué es esto

Agencia Entrerriana es un proyecto editorial de la Fundación para el Desarrollo Entrerriano, dirigido por Francisco Uranga, para cubrir la política y la economía de Paraná y Entre Ríos. Nace de un diagnóstico puntual: hoy no falta información en Entre Ríos — organismos públicos, la Legislatura, el Concejo Deliberante, cámaras empresarias, sindicatos, ONGs y universidades emiten comunicados todo el tiempo. Lo que falta es **curaduría y buena escritura**. La información existe pero está mal jerarquizada, redactada como propaganda institucional, o simplemente no llega organizada a quien la necesita. Nuestro primer aporte no es "generar más noticias" — es recuperar el concepto de noticia (hecho verificable, jerarquizado, sin relleno) y ponerlo en valor.

Alcance temático: política y economía institucional de la capital provincial y su entorno (gobierno provincial, municipio de Paraná, Legislatura, Concejo Deliberante), con foco inicial en **desarrollo económico** — el eje de la Fundación. Fuera de alcance, ahora y a futuro: deportes, espectáculos/cultura de entretenimiento (si en el futuro cubrimos "agenda cultural" es como servicio informativo — qué hay para hacer — no como crítica o cobertura editorial de cultura).

## El principio de agencia, no de repetición

No competimos con los medios que ya cubren bien un nicho. El objetivo es ser la fuente de referencia en lo que hoy nadie cubre con seriedad — política y economía institucional, desarrollo económico — y linkear/citar al resto en vez de duplicarlo. Ver [aliados-y-financiamiento.md](aliados-y-financiamiento.md), que también describe la sinergia con la agenda de reforma institucional de FUNDER (`docs/fundacion-agenda-institucional.md`).

Funcionamos como una agencia de noticias: recibimos comunicados e información de organismos y organizaciones, un editor humano decide qué es noticiable, un agente de IA lo reescribe como noticia, el editor revisa y recién ahí se publica. La ambición de mediano plazo es que este método sea reproducible — que otros medios (aliados) puedan levantar nuestro despacho igual que levantarían el de una agencia tradicional.

**Procesar un comunicado no es solo "¿se convierte en nota o no?" (2026-09-04, definido por Francisco).** La mayoría de los comunicados no van a ser noticia — eso es normal y esperable, no una falla del filtro (una oficina de prensa de gobierno está diseñada para producir autopromoción constante). Pero procesarlos igual sirve para cuatro cosas, no solo una:
1. **Identificar anuncios que ocasionalmente sí son noticia** — el caso más directo, el que ya hace `evaluar-comunicado`.
2. **Identificar reacciones o respuestas que valga la pena incluir en una historia futura**, aunque hoy no alcancen para nota propia.
3. **Identificar temas que, combinados con otras fuentes, terminen siendo una historia** (o anuncios que solos no alcanzan pero sí en conjunto) — ver la idea de combinar comunicados más abajo.
4. **Juntar información para armar trackers y llevar registro** — ver "Visión aspiracional" más abajo.

Esto es la base de por qué `docs/temas-a-seguir.md` y `data/agenda.json` guardan cosas aunque el comunicado en sí se descarte como noticia: no es indecisión, es reconocer que el valor de procesar un comunicado no se agota en la decisión de publicarlo o no.

## Visión aspiracional: el "gold standard" del periodismo local (2026-09-04)

Referencia explícita, a pedido de Francisco, para pensar hacia dónde crecer — **no es el criterio de noticiabilidad de hoy** (eso sigue siendo `docs/criterios-noticiabilidad.md`, calibrado a lo que este medio puede hacer ahora). Se investigaron medios nonprofit de referencia: THE CITY (NYC), CT Mirror, The Texas Tribune, Mississippi Today, City Bureau (Chicago), VTDigger (Vermont), Baltimore Banner, Spotlight PA, Voice of San Diego.

Patrones que se repiten en lo que estos medios eligen cubrir (no en cómo escriben, eso ya está resuelto acá):
- **Accountability sobre anuncio, no tomar el comunicado por cierto**: tratan lo que dice un funcionario como una afirmación a verificar, no un hecho a reproducir — investigar y exigir rendición de cuentas activamente, con tácticas concretas: pedidos de acceso a la información pública (FOIA), filtraciones, reporteo en persona, declaraciones juradas, bases de datos propias (ej. la franquicia de Fact Check de Voice of San Diego).
- **Seguir la plata**: el género recurrente es "¿a dónde fue realmente el dinero anunciado?", no "el gobierno anunció fondos para X".
- **Trackers persistentes, no notas sueltas**: bases que se actualizan (leyes, declaraciones juradas), no artículos de una sola vez — ver CT Mirror y VTDigger.
- **Agenda desde la comunidad, no desde la oficina de prensa** — el caso extremo es City Bureau, que paga y entrena vecinos para cubrir reuniones municipales.
- **Las investigaciones fuertes casi nunca nacen de un comunicado** — nacen de una fuente humana, un documento filtrado, o un pedido de información pública (Mississippi Today, Pulitzer 2023, es el ejemplo puro).
- **Foco en sistemas, no en eventos puntuales.**

Lo que parece alcanzable ya, sin redacción propia en el territorio: el hábito de verificar antes de reproducir (ya pasó una vez, con Consorcios Camineros — ver `docs/temas-a-seguir.md`); el seguimiento de promesas en el tiempo (`data/agenda.json`); trackers livianos armados con lo que ya se ingesta (ver abajo). Lo que sí depende de tener gente/infraestructura real: fuentes humanas, filtraciones, pedidos de acceso a la información pública (Etapa 4).

**Proyecto paralelo: acceso a documentos públicos, no construido todavía (Francisco, 2026-09-04)**: además de trackers de *estado* (leyes, ordenanzas), construir con el tiempo un repositorio propio de *documentos* públicos hechos accesibles (declaraciones juradas, actas, presupuestos ejecutados, resoluciones) — una biblioteca de fuentes primarias, no solo un tablero de seguimiento. Francisco lo marcó como un proyecto en sí mismo, en paralelo al flujo editorial diario, pero que sí quiere construir. La base legal ya está mapeada en `docs/acceso-informacion-publica.md` (Ley 27.275 nacional, Ley 11.191 provincial, procedimiento paso a paso) — incluye ideas concretas para una futura herramienta de generación/seguimiento de pedidos.

**Primer proyecto candidato concreto: chequeador de declaraciones juradas y salarios de funcionarios públicos.** En algún momento el gobierno de ER anunció la publicación de salarios y declaraciones juradas de funcionarios, y el tema se discutió/analizó poco en profundidad después del anuncio — exactamente el patrón "accountability sobre anuncio" de arriba, aplicado a un caso real y concreto. Es un buen primer candidato porque es acotado, verificable, y calza con el ejemplo de VTDigger ("Full Disclosure"). Anotado como pista a investigar en `docs/temas-a-seguir.md`.

**Fuentes individuales para la categoría de órganos de control** (refinamiento al orden de expansión de fuentes de abajo, 2026-09-04): además de las instituciones formales, **activistas, políticos de oposición y abogados** son fuentes importantes para identificar este tipo de problemas — muchas veces son quienes primero detectan y denuncian una irregularidad, antes de que llegue a un organismo de control formal.

**Trackers de leyes y ordenanzas — "SUPER CLAVE" (Francisco, 2026-09-04), pensados como herramienta interna primero, no necesariamente contenido publicado**: inspirados en el bill tracker de CT Mirror y la base de declaraciones juradas de VTDigger — un tracker del estado de los proyectos de ley en trámite en el Senado y Diputados de ER, y de ordenanzas del Concejo Deliberante de Paraná si es viable. No construir todavía; queda anotado en el roadmap (candidato natural para la Etapa 2, sección de datos) porque se puede armar en gran parte con lo que ya se ingesta de comunicados, sin depender de reporteo nuevo.

## Foco actual (2026-09-15): investigación propia sobre huecos, no volumen

Decisión de Francisco, a partir de una sesión de triage real donde quedó claro el problema en carne propia: varias notas redactadas mecánicamente ese mismo día terminaron pisando cobertura que **nosotros mismos** ya habíamos hecho días antes, o que otro medio ya cubría bien — mientras que el trabajo que más valor generó en la misma sesión fue el que no salió de reescribir un comunicado (cruzar un informe de una cámara empresaria contra fuentes primarias, conectar cuatro cierres de empresas que nadie había juntado, una discrepancia de coparticipación sin resolver, un tip para investigar). La "Visión aspiracional" de arriba (accountability sobre el anuncio, seguir la plata, ángulos que el comunicado no da) ya estaba escrita desde el 2026-09-04 — lo que cambia ahora es que deja de ser aspiración de etapas futuras y **pasa a ser el criterio central mientras el proyecto sea Francisco + una IA**, no una capacidad a construir más adelante.

Esto no es un proyecto nuevo — es un reordenamiento de seis líneas de trabajo que ya estaban, dispersas, en este documento y en `docs/aliados-y-financiamiento.md`:

1. **Investigaciones/huecos propios — el foco actual.** Cambia el criterio de triage de "¿esto se reescribe?" a "¿esto revela un hueco o un ángulo que nadie más tiene?". La mayoría de los comunicados sigue sin convertirse en nota (normal, ver arriba) — lo que sube es la barra para publicar. Conectado directo con la sinergia FUNDER (`docs/aliados-y-financiamiento.md`, sección "Sinergia con la investigación institucional de FUNDER"): un hueco de gobernanza real sirve a la vez de nota y de insumo para la agenda de reforma de la Fundación — no son dos tareas separadas.
2. **Datos y visualizaciones**, 3. **Newsletter** (qué encontramos + qué hay que seguir) y 6. **Servicio** (agenda/alertas) son subproductos casi gratis del punto 1, no proyectos aparte — `data/series/` y `data/agenda.json` ya son la semilla de 2 y 6.
4. **Agencia con destinatario otros medios** (el "despacho" de la sección de aliados) y 5. **Cobertura amplia para todo lector** son el modelo de volumen — quedan pospuestos explícitamente hasta que el punto 1 tenga trayectoria propia y/o haya más manos que Francisco solo.

**El pipeline de monitoreo (los scripts de `pipeline/monitorear_*.py` y la cablera) no se apaga** — cambia su rol de fábrica de notas a **radar de huecos**: el volumen sigue entrando, pero la mayoría se triagea con la lógica de abajo en vez de convertirse en borrador.

### Triage de tres capas (usar los estados que ya tiene `admin/index.html`, no inventar uno nuevo)

El panel ya soporta `referido` y `a_investigar` desde el 2026-09-07 (ver comentario de diseño en `admin/index.html`) — la sesión del 09-15 los subutilizó, redactando de más en vez de usarlos. De acá en más:
- **`a_investigar`**: candidato a hueco/ángulo propio, necesita más reporteo antes de decidir si da para nota.
- **`referido`**: noticiable pero ya bien cubierto por otro medio — se atribuye y linkea (newsletter/redes/portada), no se reescribe (aplicación directa de "agencia, no repetición" y de la sección "Medios y empresas como fuente" de `docs/estilo-editorial.md`).
- **`descartado`**: sin valor en ninguna capa. Reservado para cuando Francisco lo confirma explícitamente (individual o en lote) — no es una decisión que la IA tome sola.

**Sobre el descarte en bloque por antigüedad (pregunta abierta de Francisco, 09-15)**: tiene sentido dejar de usarlo como default a medida que el proyecto profundiza. El descarte automático por vencimiento (`"Vencido: pasaron mas de 48 horas..."`) es una herramienta de triage por volumen — calza con el modelo de los puntos 4/5, no con el foco actual en huecos, donde un `pendiente` viejo sin revisar es candidato a hueco tanto como uno nuevo. Reemplazo propuesto: los ítems que hoy expirarían solos pasan primero por un filtro liviano (mecánico, tipo el que ya usa `monitorear_boletin_er.py` para lo puramente administrativo) y lo que sobrevive ese filtro se reparte entre `a_investigar`/`referido`/`descartado` con criterio, no por el simple paso del tiempo — todavía no implementado, evaluar cuando el volumen real lo exija.

## Etapas

### Etapa 0 — Fundamentos (ahora)
Definir identidad (nombre, marca), infraestructura técnica, mapa de fuentes, estilo editorial. Este repo es el punto de partida: documentación + skills de Claude Code para el flujo editorial. Ver [arquitectura-tecnica.md](arquitectura-tecnica.md), [fuentes.md](fuentes.md), [estilo-editorial.md](estilo-editorial.md).

### Etapa 1 — Sitio profesional + cobertura reactiva
- Sitio web con estética seria (referencia: NYT, WSJ, Clarín, The Texas Tribune) — ver [arquitectura-tecnica.md](arquitectura-tecnica.md).
- **SEO y GEO desde el diseño del frontend, no como parche después** (Francisco, 2026-09-07) — ver [seo-geo.md](seo-geo.md): structured data, política de crawlers de IA, canónicas para republicación con aliados, todo tiene que decidirse cuando arranque el frontend, no agregarse encima después.
- Cobertura reactiva: monitoreo de comunicados y novedades de gobierno provincial (áreas de desarrollo económico/producción/trabajo), Municipalidad de Paraná, Legislatura, Concejo Deliberante, y organizaciones privadas (UIER, Consejo Empresario de Entre Ríos, cámaras sectoriales), sindicatos, ONGs e instituciones académicas.
- Además de comunicados institucionales, monitoreo de **medios nacionales y locales** (para no perder hechos relevantes que no pasan por un comunicado) y de **empresas relevantes a nivel local** (presentaciones regulatorias, causas judiciales, cobertura en prensa especializada). Esto es más delicado que reescribir un comunicado público — ver el estándar de atribución específico en [estilo-editorial.md](estilo-editorial.md#fuentes-que-no-son-comunicados-medios-y-empresas): siempre atribuido a la fuente primaria, y con preferencia por sumar valor propio antes que reescribir el trabajo original de otro medio, sobre todo si es chico.
- **Orden de expansión de fuentes** (definido 2026-09-03, actualizado 2026-09-04): (1) gobierno — provincial y Paraná primero, luego organismos nacionales con sede en ER o con comunicados nacionales que tengan ángulo/impacto local; **(2) órganos de control, auditoría y oposición — prioridad TOP agregada 2026-09-04, mapeada 2026-09-06**: Tribunal de Cuentas, Fiscalía de Estado, OAIP/Portal de Transparencia, Datos Abiertos ER, Poder Judicial/STJ, Tribunal Electoral, entes autárquicos — ver la sección "Órganos de control, transparencia y justicia" en `docs/fuentes.md` (más una capa nacional equivalente: AGN, SIGEN, Oficina Anticorrupción, ver sección "Nacional" del mismo doc). Falta todavía: bloques de oposición en su rol específico de control (pedidos de informe, denuncias, cuestionamientos a la gestión — no su actividad política general, que cae en la categoría de partidos), fallos judiciales relevantes para accountability de gestión, y **fuentes individuales** — activistas, políticos de oposición y abogados que muchas veces detectan y denuncian una irregularidad antes de que llegue a un organismo formal. Es la fuente más directa para cubrir en el espíritu de "seguir la plata" y "accountability sobre anuncio" de la visión aspiracional de arriba — la razón de la prioridad alta es que hoy casi toda la cablera sale de la propia comunicación oficial del gobierno, sin ningún contrapeso. Nota: "mapeada" significa documentada en `fuentes.md`, no ingestada — la mayoría no tiene RSS y el mecanismo de monitoreo todavía no está resuelto (ver `docs/calendario-publicaciones.md` y `docs/arquitectura-tecnica.md`); (3) organizaciones de la sociedad civil (sindicatos, cámaras empresarias, empresas, ONGs, instituciones educativas, asociaciones profesionales); (4) organizaciones vecinales; (5) partidos políticos y otras agrupaciones (actividad política general, distinta del rol de control de la oposición ya cubierto en el punto 2); (6) medios de comunicación locales/provinciales/nacionales que cubran ER. Ver `docs/fuentes.md` para el mapeo concreto (todavía sin mapear la categoría 2, pendiente de correr `mapear-fuentes` sobre ella) y `docs/arquitectura-tecnica.md` (sección "Estrategia de ingesta de comunicados") para el mecanismo de captura por etapa.
- Flujo: fuente → triage editorial (Francisco decide qué es noticia) → reescritura con IA en estilo Bloomberg/WSJ (corta, directa, pirámide invertida) → revisión editorial → publicación.
- **Idea a moldear con uso real, no construida todavía (2026-09-04)**: combinar varios comunicados (de una o distintas fuentes) en una sola historia cuando ninguno solo alcanza para ser noticia pero juntos sí cuentan algo — en vez de descartar cada uno por separado. No hay skill para esto todavía; se va a ir moldeando en la práctica (posiblemente con un subagente si el flujo se vuelve complejo) antes de formalizarla. Implicancia para la cablera cuando exista: varios ítems de `data/backlog.json` (en `estado: "a_publicar"`) apuntarían al mismo `wp_edit_url` (un borrador combinado), no un campo nuevo — el ejemplo motivador es Consorcios Camineros + el conflicto de la DPV + la modificación a la Ley de Municipios, todo de la misma sesión del Senado (ver `docs/temas-a-seguir.md`).
- Distribución fuerte en redes sociales y, sobre todo, **newsletter** (diaria y/o semanal — a definir con el uso real).
- Todo el contenido en texto por ahora.

### Etapa 2 — Ampliación temática y módulos de servicio
- Nuevos módulos temáticos: política/policy en general, economía en general, judiciales.
- Módulos de servicio que respondan a necesidades detectadas: bolsa de trabajo (agregación de ofertas de distintas fuentes/medios), agenda cultural (como servicio, no como cobertura editorial), y otros que surjan.
- Sección de datos: datos públicos locales hechos accesibles (presupuesto, ejecución, indicadores económicos), datos del sector privado, datos electorales. Requiere pensar bien qué datasets, con qué periodicidad, y cómo presentarlos — es un proyecto en sí mismo, no una nota más.
- **Tracker de leyes y ordenanzas** (ver "Visión aspiracional" más arriba) — estado de los proyectos de ley en trámite en el Senado y Diputados de ER, y de ordenanzas del Concejo Deliberante si es viable. Pensado primero como herramienta interna, no necesariamente contenido publicado.
- **Pregunta abierta (2026-09-04, sin resolver): ¿opinión/cartas al editor?** Por ahora, **solo noticias** — sin sección de opinión, siguiendo el modelo puro del Texas Tribune. La duda real es sobre "cartas al editor" específicamente (no opinión editorial propia): podrían funcionar como vínculo con la comunidad sin comprometer la línea de solo-noticias — a diferencia de una sección de opinión con voces propias, una carta al editor es la comunidad hablando, no el medio. La tensión: ¿vale la pena invertir en esto por el valor de comunidad que genera, o es mejor mantenerse 100% noticioso como referencia? Si en algún momento se implementa, tiene que quedar **claramente identificado como otro tipo de contenido** — tipografía distinta (cursiva en el título, por ejemplo) y etiquetado explícito, nunca mezclado visualmente con una noticia.

### Etapa 3 — Nuevos formatos
- Data journalism como área propia (no solo una sección, sino una forma de reportar).
- Lector de noticias en audio con IA.
- Explorar otros formatos según lo que la audiencia use.

### Etapa 4 — Periodismo humano en el terreno
- Periodistas locales que cubran en persona: reuniones de gobierno, entrevistas, sesiones legislativas y del Concejo.
- **Adelantable, no depende de tener periodistas propios**: analizar la grabación/transmisión original de conferencias de prensa, audiencias públicas y sesiones legislativas (cuando existan) en vez de depender solo del comunicado/acta que las resume — puede revelar algo que el resumen oficial omite. Ver `docs/criterios-noticiabilidad.md`, sección "Preguntas abiertas".
- Pedidos de acceso a la información pública.
- Investigaciones y especiales.
- **Canal de denuncias/whistleblower** — a diferencia del resto de esta etapa, esto podría adelantarse: no depende de tener redacción propia, solo de un canal seguro y un protocolo claro de manejo. Vale la pena evaluarlo antes que el resto de la etapa 4.

### Etapa 5 — Sostenibilidad y expansión
- Eventos, capacitaciones.
- Formas de financiamiento más allá del respaldo inicial de la Fundación — ver [aliados-y-financiamiento.md](aliados-y-financiamiento.md).

## Qué NO es este proyecto (por ahora)
- No es un agregador que reproduce notas ajenas sin transformarlas.
- No es un medio de deportes, espectáculos o cultura de entretenimiento.
- No reemplaza el criterio editorial humano: la IA reescribe, no decide qué es noticia ni publica sola.
