# [NOMBRE DEL MEDIO] (nombre provisorio)

Un medio digital para cubrir la política y la economía de Paraná y Entre Ríos. Proyecto editorial de la **Fundación para el Desarrollo Entrerriano**, dirigido por **Francisco Uranga**.

> El nombre es lo único que todavía no está definido a propósito — elegirlo es parte del trabajo, no un detalle pendiente. Este documento y el resto del repo usan `[NOMBRE DEL MEDIO]` como placeholder hasta entonces.

## El diagnóstico

En Entre Ríos no falta información. Gobierno provincial, Municipalidad de Paraná, Legislatura, Concejo Deliberante, cámaras empresarias, sindicatos, ONGs y universidades emiten comunicados constantemente. Lo que falta es **curaduría y buena escritura**: esa información llega mal jerarquizada, redactada como propaganda institucional, o directamente no llega organizada a nadie. Antes de "generar más noticias", el aporte de este proyecto es recuperar el concepto de noticia — un hecho verificable, jerarquizado, sin relleno — y ponerlo en valor.

## Cómo funciona (etapa 1)

Como una agencia de noticias:

1. Monitoreamos comunicados y novedades de organismos y organizaciones de Paraná/Entre Ríos (mapa completo en [`docs/fuentes.md`](docs/fuentes.md)).
2. El editor (Francisco Uranga) decide qué es noticiable. Esa decisión es siempre humana.
3. Un agente de IA reescribe lo elegido como noticia corta, estilo Bloomberg/WSJ — pirámide invertida, sin relleno institucional, con atribución explícita de cualquier dato que venga de la fuente y no de verificación propia (reglas completas en [`docs/estilo-editorial.md`](docs/estilo-editorial.md)).
4. El editor revisa y recién ahí se publica.

Foco temático inicial: **desarrollo económico** — el eje de la Fundación. Fuera de alcance: deportes, espectáculos, cultura de entretenimiento. El resto de la hoja de ruta (nuevos módulos temáticos, sección de datos, bolsa de trabajo, periodismo de investigación, canal de denuncias, eventos) está en [`docs/vision-y-etapas.md`](docs/vision-y-etapas.md).

No competimos con los medios que ya cubren bien un nicho — linkeamos y citamos en vez de repetir, y buscamos que nuestro propio despacho sea reproducible por otros medios aliados. Más sobre esto y sobre posibles vías de financiamiento en [`docs/aliados-y-financiamiento.md`](docs/aliados-y-financiamiento.md).

## Estado actual

Preoperativo. Este repo hoy contiene la planificación del proyecto y las skills de Claude Code para el flujo editorial — todavía no hay sitio, ni infraestructura de publicación, ni fuentes verificadas al 100%. Ver [`docs/vision-y-etapas.md`](docs/vision-y-etapas.md) para la hoja de ruta completa.

## Estructura del repo

```
docs/
  vision-y-etapas.md        Visión del proyecto y hoja de ruta por etapas
  arquitectura-tecnica.md   Decisión de infraestructura (WordPress + pipeline propio) y por qué
  estilo-editorial.md       Reglas de redacción — la referencia de las skills editoriales
  aliados-y-financiamiento.md  Posibles alianzas y vías de sostenibilidad
  fuentes.md                Mapa de organismos/organizaciones a monitorear

skills/
  redactar-noticia/         Reescribe un comunicado ya elegido por el editor como noticia
  evaluar-comunicado/       Resume comunicados entrantes para agilizar el triage editorial
  mapear-fuentes/           Investiga y mantiene actualizado docs/fuentes.md
```

## Infraestructura (resumen — detalle en `docs/arquitectura-tecnica.md`)

WordPress autoalojado como backend editorial y sitio público (no un CMS propio desde cero: WordPress ya resuelve roles, revisiones, SEO, seguridad y backups). El motor específico de este proyecto — ingesta de comunicados, triage, reescritura con IA — vive por fuera, en este repo, y publica en WordPress como borrador vía su API REST. El editor revisa y publica desde ahí. Un CMS propio queda para cuando un módulo futuro lo justifique.

## Trabajando con este repo

Si estás usando Claude Code acá, ver [`CLAUDE.md`](CLAUDE.md) para el contexto y las reglas de trabajo.
