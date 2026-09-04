# Visión y etapas

## Qué es esto

Agencia Entrerriana es un proyecto editorial de la Fundación para el Desarrollo Entrerriano, dirigido por Francisco Uranga, para cubrir la política y la economía de Paraná y Entre Ríos. Nace de un diagnóstico puntual: hoy no falta información en Entre Ríos — organismos públicos, la Legislatura, el Concejo Deliberante, cámaras empresarias, sindicatos, ONGs y universidades emiten comunicados todo el tiempo. Lo que falta es **curaduría y buena escritura**. La información existe pero está mal jerarquizada, redactada como propaganda institucional, o simplemente no llega organizada a quien la necesita. Nuestro primer aporte no es "generar más noticias" — es recuperar el concepto de noticia (hecho verificable, jerarquizado, sin relleno) y ponerlo en valor.

Alcance temático: política y economía institucional de la capital provincial y su entorno (gobierno provincial, municipio de Paraná, Legislatura, Concejo Deliberante), con foco inicial en **desarrollo económico** — el eje de la Fundación. Fuera de alcance, ahora y a futuro: deportes, espectáculos/cultura de entretenimiento (si en el futuro cubrimos "agenda cultural" es como servicio informativo — qué hay para hacer — no como crítica o cobertura editorial de cultura).

## El principio de agencia, no de repetición

No competimos con los medios que ya cubren bien un nicho. El objetivo es ser la fuente de referencia en lo que hoy nadie cubre con seriedad — política y economía institucional, desarrollo económico — y linkear/citar al resto en vez de duplicarlo. Ver [aliados-y-financiamiento.md](aliados-y-financiamiento.md).

Funcionamos como una agencia de noticias: recibimos comunicados e información de organismos y organizaciones, un editor humano decide qué es noticiable, un agente de IA lo reescribe como noticia, el editor revisa y recién ahí se publica. La ambición de mediano plazo es que este método sea reproducible — que otros medios (aliados) puedan levantar nuestro despacho igual que levantarían el de una agencia tradicional.

## Etapas

### Etapa 0 — Fundamentos (ahora)
Definir identidad (nombre, marca), infraestructura técnica, mapa de fuentes, estilo editorial. Este repo es el punto de partida: documentación + skills de Claude Code para el flujo editorial. Ver [arquitectura-tecnica.md](arquitectura-tecnica.md), [fuentes.md](fuentes.md), [estilo-editorial.md](estilo-editorial.md).

### Etapa 1 — Sitio profesional + cobertura reactiva
- Sitio web con estética seria (referencia: NYT, WSJ, Clarín, The Texas Tribune) — ver [arquitectura-tecnica.md](arquitectura-tecnica.md).
- Cobertura reactiva: monitoreo de comunicados y novedades de gobierno provincial (áreas de desarrollo económico/producción/trabajo), Municipalidad de Paraná, Legislatura, Concejo Deliberante, y organizaciones privadas (UIER, Consejo Empresario de Entre Ríos, cámaras sectoriales), sindicatos, ONGs e instituciones académicas.
- Además de comunicados institucionales, monitoreo de **medios nacionales y locales** (para no perder hechos relevantes que no pasan por un comunicado) y de **empresas relevantes a nivel local** (presentaciones regulatorias, causas judiciales, cobertura en prensa especializada). Esto es más delicado que reescribir un comunicado público — ver el estándar de atribución específico en [estilo-editorial.md](estilo-editorial.md#fuentes-que-no-son-comunicados-medios-y-empresas): siempre atribuido a la fuente primaria, y con preferencia por sumar valor propio antes que reescribir el trabajo original de otro medio, sobre todo si es chico.
- **Orden de expansión de fuentes** (definido 2026-09-03): (1) gobierno — provincial y Paraná primero, luego organismos nacionales con sede en ER o con comunicados nacionales que tengan ángulo/impacto local; (2) organizaciones de la sociedad civil (sindicatos, cámaras empresarias, empresas, ONGs, instituciones educativas, asociaciones profesionales); (3) organizaciones vecinales; (4) partidos políticos y otras agrupaciones; (5) medios de comunicación locales/provinciales/nacionales que cubran ER. Ver `docs/fuentes.md` para el mapeo concreto y `docs/arquitectura-tecnica.md` (sección "Estrategia de ingesta de comunicados") para el mecanismo de captura por etapa.
- Flujo: fuente → triage editorial (Francisco decide qué es noticia) → reescritura con IA en estilo Bloomberg/WSJ (corta, directa, pirámide invertida) → revisión editorial → publicación.
- Distribución fuerte en redes sociales y, sobre todo, **newsletter** (diaria y/o semanal — a definir con el uso real).
- Todo el contenido en texto por ahora.

### Etapa 2 — Ampliación temática y módulos de servicio
- Nuevos módulos temáticos: política/policy en general, economía en general, judiciales.
- Módulos de servicio que respondan a necesidades detectadas: bolsa de trabajo (agregación de ofertas de distintas fuentes/medios), agenda cultural (como servicio, no como cobertura editorial), y otros que surjan.
- Sección de datos: datos públicos locales hechos accesibles (presupuesto, ejecución, indicadores económicos), datos del sector privado, datos electorales. Requiere pensar bien qué datasets, con qué periodicidad, y cómo presentarlos — es un proyecto en sí mismo, no una nota más.

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
