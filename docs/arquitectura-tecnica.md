# Arquitectura técnica

## Recomendación: WordPress headless (backend editorial) + frontend a medida + pipeline de agencia propio

No conviene construir un CMS propio desde cero para la etapa 1. La razón no es que sea imposible — es que WordPress ya resuelve, de forma probada, todo lo que no es específico de este proyecto: usuarios y roles, revisiones de artículos, biblioteca de medios, editor de texto (Gutenberg), backups. Reconstruir eso es el uso menos eficiente del tiempo en esta etapa. Lo específico de este proyecto — el motor de agencia (ingesta de comunicados, triage, reescritura con IA) — no vive naturalmente en WordPress y no debería intentar vivir ahí: es una capa separada que le habla a WordPress por API.

**Revisión de esta recomendación (post-lanzamiento del proyecto):** el requisito de margen de edición/diseño real (estética NYT/WSJ/Texas Tribune, formatos de nota propios, sin quedar atado a la lógica de templates de un theme) pesa más que la simplicidad de un theme clásico. Un theme de WordPress, incluso un child theme a medida, sigue siendo pelear contra la lógica de bloques/templates de WP para cualquier diseño que se salga de lo estándar. La solución no es abandonar WordPress — es que **WordPress nunca renderice el sitio público**. Queda puertas adentro, como herramienta de edición únicamente; un frontend a medida se encarga de todo lo que ve el lector.

Un CMS propio (reemplazar WordPress mismo, no solo su rendering) recién se justificaría cuando un módulo futuro (bolsa de trabajo, dashboards de datos) pida algo que ni WordPress ni el frontend a medida resuelven bien — y ahí la respuesta más probable sigue siendo sumar una app separada, no reescribir todo.

### Tres capas separadas

**(a) WordPress — backend editorial únicamente, nunca lo que ve el público**
- Hosting gestionado simple y privado (no expuesto como "el sitio", lo que además reduce superficie de ataque). Con un solo editor y sin equipo de sysadmin, no vale la pena un VPS propio para esto.
- Ahí vivís vos: revisás y editás los borradores que sube el pipeline de agencia, con el editor nativo (Gutenberg), roles, historial de revisiones.
- Plugins base: seguridad y backups, y **REST API con Application Passwords** habilitado — es la puerta de entrada para que (1) el pipeline de agencia cree posts como borrador y (2) el frontend lea el contenido publicado. No hace falta plugin de SEO acá — el SEO se resuelve en el frontend, que es lo que Google efectivamente indexa.

**(b) Frontend a medida — el sitio público, sin restricciones de theme**
- Next.js (o similar), consumiendo la API REST de WordPress. Control total: tipografía, grilla de portada con jerarquía editorial propia, formatos de nota especiales, visualizaciones de datos embebidas — nada limitado por lo que un theme permita.
- Deploy en **Vercel** (nivel gratuito generoso para el tráfico inicial): despliega directo desde este repo de GitHub con cada push, sin necesidad de administrar un servidor para la parte pública. Buen SEO y performance out of the box (SSG/ISR).
- SEO, sitemap, OG tags, analytics: se manejan acá, no en WordPress.
- Esto es más piezas que un WordPress clásico todo-en-uno (dos sistemas para mantener en vez de uno), pero el desarrollo lo hacemos vos y yo con Claude Code — no depende de contratar a alguien aparte — y a cambio el techo de diseño es mucho más alto, que es justamente el requisito no negociable acá.
- Newsletter: evaluar un ESP dedicado (Beehiiv, Mailchimp, o similar) en vez de un plugin de WordPress — mejor entregabilidad y mejores herramientas de crecimiento de lista. Se integra por API o embed desde el frontend.

**(c) Pipeline de agencia — capa propia, en este repo**
No es un CMS, es un flujo de trabajo con soporte de IA. Componentes:
1. **Registro de fuentes** (`docs/fuentes.md`, y eventualmente un `fuentes.json` estructurado): organismos y organizaciones a monitorear, con su URL de prensa/comunicados y feed si existe.
2. **Backlog de comunicados entrantes**: un mecanismo simple para juntar lo nuevo de cada fuente. Al principio puede ser manual (revisar cada portal/RSS a mano o con ayuda de la skill `mapear-fuentes`); más adelante, automatizable (RSS reader, scraper liviano, o alertas). No hace falta un scraper sofisticado desde el día uno.
3. **Triage editorial**: Francisco revisa el backlog y decide qué es noticiable. Esta decisión es humana y no se automatiza (ver `CLAUDE.md`).
4. **Reescritura con IA**: para cada ítem elegido, la skill `redactar-noticia` (ver `skills/`) genera título, bajada y cuerpo en estilo Bloomberg/WSJ, atribuyendo con precisión lo que viene del comunicado.
5. **Publicación como borrador en WordPress**: el resultado se sube vía REST API como post en estado `draft` o `pending`, no como publicado. Este paso es el que reemplaza al panel de administración a medida que se usó en el proyecto hermano `despidos-tracker` — WordPress ya tiene un flujo de borrador/revisión nativo, no hace falta reconstruirlo.
6. **Revisión editorial final**: Francisco edita y publica desde el editor nativo de WordPress.

Este pipeline puede vivir como scripts (Python o Node) en este mismo repo, corriendo localmente al principio y, más adelante, en un cron/GitHub Action si el volumen lo justifica.

### Por qué no arrancar con un CMS propio (reemplazar WordPress mismo)
- Autenticación, roles, revisiones y backups son problemas resueltos en WordPress y no aportan nada distintivo a este proyecto si se reconstruyen — la ganancia de control de diseño ya la resuelve el frontend a medida, sin necesidad de tocar el backend.
- El verdadero diferencial de este proyecto (el motor de agencia) es agnóstico del backend de destino — funciona igual publicando en WordPress que en cualquier otro sistema. No hace falta resolver "dónde vive el contenido" para avanzar en "cómo decide qué publicar y cómo lo escribe".
- Si en el futuro WordPress se vuelve una traba real (por ejemplo, para los dashboards de datos de la etapa 2), la solución más probable sigue siendo sumar una app separada integrada, no migrar todo.

## Pendiente de decidir con el usuario
- Nombre de dominio (atado a la decisión de marca, ver `vision-y-etapas.md`).
- Hosting de WordPress (gestionado, privado, de bajo costo — no necesita ser potente, no sirve tráfico público).
- Confirmar Next.js + Vercel como stack del frontend, o evaluar alternativas si hay preferencia técnica distinta.
- ESP de newsletter.
- Repositorio de GitHub: ya creado y en uso — [github.com/FUranga/noticias-er](https://github.com/FUranga/noticias-er) (privado).
