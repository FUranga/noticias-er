# SEO y GEO — tema crítico, no un detalle de lanzamiento

Marcado como prioridad crítica por Francisco (2026-09-06), a resolver **desde el diseño del frontend**, no como parche después de lanzar. Se abre este doc ahora (antes de que arranque el frontend, ver `docs/arquitectura-tecnica.md`) porque es mucho más barato bakear esto desde el primer commit que retrofittearlo sobre un sitio ya construido.

## Por qué esto es central para este proyecto en particular

El modelo del medio (ver `docs/vision-y-etapas.md`, "El principio de agencia") es ser **la fuente de referencia** en política y economía institucional de Entre Ríos — no la más viral, la más citable. Eso hace que dos canales de descubrimiento importen más que para un medio genérico:

- **SEO clásico**: alguien busca "presupuesto Entre Ríos 2026" o "Tribunal de Cuentas IOSPER" y este medio tiene que aparecer — es tráfico de intención, no de scroll casual, y calza con una audiencia de funcionarios, otros medios, y ciudadanos informados.
- **GEO (Generative Engine Optimization)**: cuando alguien le pregunta a ChatGPT/Perplexity/Claude/Google AI Overviews algo sobre Entre Ríos, que la respuesta cite (y linkee) a este medio como fuente. Para un medio que aspira a ser la referencia de un nicho geográfico/temático chico, esto puede terminar siendo tan importante como el ranking en Google — es una categoría nueva, todavía sin prácticas 100% asentadas, que conviene empezar a seguir de cerca.

Además, el modelo de republicación con medios aliados (`docs/aliados-y-financiamiento.md`, estilo Texas Tribune) hace que la gestión de URLs canónicas no sea opcional: si un medio chico republica una nota, hay que asegurarse de que Google y los motores de IA sigan atribuyendo la nota original a este medio, no a quien la reprodujo.

## Por qué la arquitectura elegida ayuda (y por qué no alcanza sola)

WordPress queda puertas adentro (`docs/arquitectura-tecnica.md`) — nunca renderiza el sitio público, así que **no hay ningún plugin de SEO tipo Yoast dando una base gratis**. Todo el SEO/GEO depende 100% de cómo se construya el frontend Next.js. La decisión de SSG/ISR ya ayuda (velocidad de carga, Core Web Vitals), pero eso es una fracción del trabajo.

El estilo editorial (`docs/estilo-editorial.md`) también ayuda sin buscarlo: pirámide invertida, atribución explícita ("según informó el Ministerio de Producción"), sin relleno — es exactamente la estructura que un sistema de IA necesita para extraer un hecho citable con su fuente clara. La tarea no es inventar contenido "optimizado para IA" (eso degradaría el estilo), es no dejar que el frontend le saque valor a algo que la redacción ya hace bien.

## Decisiones concretas a tomar cuando arranque el frontend (no implementar todavía)

**Structured data (schema.org, vía JSON-LD)**: cada nota necesita marcado `NewsArticle` (headline, fecha de publicación/modificación, autor, organización editora con logo, cuerpo) — es lo que tanto Google como los crawlers de IA usan para entender y citar con confianza. Sin esto, el frontend es indistinguible de una página cualquiera para un sistema automatizado.

**`robots.txt` frente a crawlers de IA — decisión explícita, no default**: GPTBot (OpenAI), ClaudeBot/anthropic-ai, PerplexityBot, Google-Extended, CCBot, etc. Bloquearlos por reflejo (como hacen muchos medios, por temor a que "usen" el contenido sin retribución) va directo en contra del objetivo de ser fuente citada por IA. Recomendación a confirmar con Francisco cuando se llegue a este punto: **permitir explícitamente** a los crawlers de los motores donde queremos aparecer citados, salvo que aparezca una razón concreta (ej. un modelo de negocio de licenciamiento de contenido) para restringir alguno puntual.

**`llms.txt`**: convención nueva (un archivo de texto plano que orienta a agentes de IA sobre el sitio) — barato de agregar, sin certeza todavía de cuánto lo usan los motores reales, pero de costo casi nulo.

**Canónicas y atribución para republicación**: cuando un medio aliado reproduzca una nota (`docs/aliados-y-financiamiento.md`), la nota original necesita `rel=canonical` apuntando a este medio, y cualquier acuerdo de republicación debería pedir que el aliado linkee de vuelta — no solo por cortesía editorial, también para que Google/IA sigan atribuyendo la fuente real.

**Identidad editorial visible (señales de autoridad/confianza)**: una página "Quiénes somos" clara, autoría nombrada en cada nota (no "Redacción" genérico salvo que corresponda), y una política editorial pública (versión resumida de `docs/estilo-editorial.md`) — tanto Google como los sistemas de IA ponderan la credibilidad de la fuente, no solo la estructura técnica de la página.

**Sitemap + indexación rápida**: `sitemap.xml` generado automáticamente, envío a Google Search Console/Bing Webmaster, y considerar la API de indexación de Google/IndexNow para que una nota nueva se indexe rápido — relevante para un medio que a veces compite en ser el primero en cubrir algo con contexto real (ver `docs/criterios-noticiabilidad.md`, la lección de oportunidad/timing).

**URLs y jerarquía**: slugs descriptivos, un H1 claro por nota, jerarquía de encabezados limpia, breadcrumbs con su propio structured data (`BreadcrumbList`).

## Abierto / sin decidir todavía

- ¿Vale la pena perseguir notabilidad en Wikipedia/Wikidata para el medio una vez que tenga trayectoria? Ayuda tanto a SEO como a GEO (muchos sistemas de IA usan Wikipedia/Wikidata como ancla de entidades).
- ¿Cómo medir si la estrategia de GEO está funcionando? A diferencia de SEO (Search Console da datos concretos), todavía no hay una herramienta estándar de "cuánto te citan los motores de IA" — revisar qué existe cuando se llegue a esta etapa.
- Si en algún momento se evalúa contenido patrocinado o paywall parcial (`docs/aliados-y-financiamiento.md`), verificar que no bloquee a los crawlers de los motores que sí queremos que citen la nota.

## Cuándo retomar esto

En el momento de arrancar el frontend (`docs/vision-y-etapas.md`, Etapa 1) — no antes (no hay nada que implementar sin sitio) y no después (retrofittear structured data y una estrategia de crawlers de IA sobre un sitio ya construido es mucho más trabajo que incluirlo desde el primer sprint).
