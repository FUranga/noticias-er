# Arquitectura técnica

## Recomendación: WordPress como backend editorial + pipeline de agencia propio por fuera

No conviene construir un CMS propio desde cero para la etapa 1. La razón no es que sea imposible — es que WordPress ya resuelve, de forma probada, todo lo que no es específico de este proyecto: usuarios y roles, revisiones de artículos, biblioteca de medios, SEO, seguridad, backups, editor de texto (Gutenberg). Reconstruir eso es el uso menos eficiente del tiempo en esta etapa. Lo específico de este proyecto — el motor de agencia (ingesta de comunicados, triage, reescritura con IA) — no vive naturalmente en WordPress y no debería intentar vivir ahí: es una capa separada que le habla a WordPress por API.

Un CMS propio recién se justifica cuando un módulo futuro (bolsa de trabajo, dashboards de datos, lector de audio) pide algo que WordPress genuinamente no resuelve bien. Ahí la respuesta probablemente no es "reemplazar WordPress" sino sumar una app separada (subdominio o microservicio) que se integra con él — no una reescritura completa.

### Dos capas separadas

**(a) WordPress — el sitio público y el backend editorial**
- Autoalojado (VPS) o hosting gestionado — la diferencia es cuánto control técnico se quiere asumir desde el día uno. Con un solo editor y sin equipo de sysadmin, hosting gestionado (actualizaciones y seguridad resueltas) es probablemente más sensato para arrancar.
- Estética NYT/WSJ/Texas Tribune: esto no sale de un theme de plantilla genérico tipo "Newspaper" de ThemeForest — esos se notan. Dos caminos:
  1. Child theme a medida sobre una base sólida y liviana (Kadence o GeneratePress) con diseño propio.
  2. WordPress "headless": WP solo como backend/API de contenido, y un frontend a medida (por ejemplo Next.js) consumiendo su REST API — más control visual y de performance, más trabajo de desarrollo. Vale la pena si hay presupuesto de desarrollo desde el arranque; si no, empezar con (1) y migrar a headless más adelante es un camino razonable.
- Plugins base: SEO (Yoast o RankMath), cache/performance, seguridad y backups, y **REST API con Application Passwords** habilitado — es la puerta de entrada para que el pipeline de agencia cree posts como borrador.
- Newsletter: evaluar un ESP dedicado (Beehiiv, Mailchimp, o similar) en vez de un plugin de WordPress para esto — mejor entregabilidad y mejores herramientas de crecimiento de lista que cualquier plugin. Se integra por API o por un simple embed/formulario.

**(b) Pipeline de agencia — capa propia, en este repo**
No es un CMS, es un flujo de trabajo con soporte de IA. Componentes:
1. **Registro de fuentes** (`docs/fuentes.md`, y eventualmente un `fuentes.json` estructurado): organismos y organizaciones a monitorear, con su URL de prensa/comunicados y feed si existe.
2. **Backlog de comunicados entrantes**: un mecanismo simple para juntar lo nuevo de cada fuente. Al principio puede ser manual (revisar cada portal/RSS a mano o con ayuda de la skill `mapear-fuentes`); más adelante, automatizable (RSS reader, scraper liviano, o alertas). No hace falta un scraper sofisticado desde el día uno.
3. **Triage editorial**: Francisco revisa el backlog y decide qué es noticiable. Esta decisión es humana y no se automatiza (ver `CLAUDE.md`).
4. **Reescritura con IA**: para cada ítem elegido, la skill `redactar-noticia` (ver `skills/`) genera título, bajada y cuerpo en estilo Bloomberg/WSJ, atribuyendo con precisión lo que viene del comunicado.
5. **Publicación como borrador en WordPress**: el resultado se sube vía REST API como post en estado `draft` o `pending`, no como publicado. Este paso es el que reemplaza al panel de administración a medida que se usó en el proyecto hermano `despidos-tracker` — WordPress ya tiene un flujo de borrador/revisión nativo, no hace falta reconstruirlo.
6. **Revisión editorial final**: Francisco edita y publica desde el editor nativo de WordPress.

Este pipeline puede vivir como scripts (Python o Node) en este mismo repo, corriendo localmente al principio y, más adelante, en un cron/GitHub Action si el volumen lo justifica.

### Por qué no arrancar con un CMS propio
- Autenticación, roles, revisiones, seguridad y backups son problemas resueltos en WordPress y no aportan nada distintivo a este proyecto si se reconstruyen.
- El verdadero diferencial de este proyecto (el motor de agencia) es agnóstico del CMS de destino — funciona igual publicando en WordPress que en un CMS propio. No hace falta resolver "dónde publica" para avanzar en "cómo decide qué publicar y cómo lo escribe".
- Si en el futuro WordPress se vuelve una traba real (por ejemplo, para los dashboards de datos de la etapa 2), la solución más probable es sumar una app separada integrada, no migrar todo el sitio.

## Pendiente de decidir con el usuario
- Nombre de dominio (atado a la decisión de marca, ver `vision-y-etapas.md`).
- Hosting: gestionado vs. VPS propio, y presupuesto disponible.
- Si se arranca con theme a medida clásico o headless — depende de si hay presupuesto de desarrollo desde el día uno.
- ESP de newsletter.
- Repositorio de GitHub: se crea desde esta sesión (ver siguiente sección de este documento una vez creado, o el README).
