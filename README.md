# Agencia Entrerriana (nombre provisorio)

Un medio digital para cubrir la política y la economía de Paraná y Entre Ríos. Proyecto editorial de la **Fundación para el Desarrollo Entrerriano**, dirigido por **Francisco Uranga**.

> El nombre es lo único que todavía no está definido a propósito — elegirlo es parte del trabajo, no un detalle pendiente. Este documento y el resto del repo usan `Agencia Entrerriana` como placeholder hasta entonces.

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

- **WordPress del medio** (backend editorial, privado, dominio temporal en Hostinger) — instalado, con la API REST y una Application Password activa para el pipeline.
- **Sitio de la Fundación** (`desarrolloentrerriano.org`, Hostinger São Paulo) — WordPress + theme Kadence, construido de punta a punta: portada, menú (con submenú "Sobre"), archivo de Novedades paginado, categorías, redes sociales y contacto en el footer, y contenido histórico real recuperado (54 notas de FUNDER + 20 de Visión Desarrollista + 1 de Análisis Digital). Detalle completo en [`docs/sitio-fundacion.md`](docs/sitio-fundacion.md), scripts de mantenimiento en [`fundacion-wp/`](fundacion-wp/), pendientes en [`docs/checklist-sitio-fundacion.md`](docs/checklist-sitio-fundacion.md).
- **Pipeline de publicación** (`pipeline/`) y **cablera** (`admin/` + `data/backlog.json`) — funcionando de punta a punta: el editor marca ítems en el panel, la skill `procesar-cablera` los redacta y los sube a WordPress como borrador. `data/backlog.json` ya tiene ítems reales del Gobierno de Entre Ríos, cargados automáticamente por `pipeline/monitorear_gobierno_er.py` (API pública + scraping con Playwright — ver `docs/fuentes.md`).
- **Frontend público del medio** (Next.js/Vercel) — todavía no arrancado.

Ver [`docs/vision-y-etapas.md`](docs/vision-y-etapas.md) para la hoja de ruta completa.

## Estructura del repo

```
docs/
  vision-y-etapas.md        Visión del proyecto y hoja de ruta por etapas
  arquitectura-tecnica.md   Decisión de infraestructura (WordPress headless + frontend propio) y por qué
  estilo-editorial.md       Reglas de redacción — la referencia de las skills editoriales
  aliados-y-financiamiento.md  Posibles alianzas y vías de sostenibilidad
  fuentes.md                Mapa de organismos/organizaciones a monitorear
  contactos-prensa.md       Lista de contactos de prensa confirmados, para suscribirse a listas de mail
  contenido-historico-fundacion.md  Contenido institucional de FUNDER rescatado de Wayback Machine
  sitio-fundacion.md        Estado, decisiones y gotchas técnicos del sitio de la Fundación
  checklist-sitio-fundacion.md  Pendientes del sitio de la Fundación, agrupados por prioridad
  prensa-fundacion.md       Contacto de prensa por defecto, reglas de embargo y estado del listado de periodistas de FUNDER

skills/
  redactar-noticia/         Reescribe un comunicado ya elegido por el editor como noticia
  evaluar-comunicado/       Resume comunicados entrantes para agilizar el triage editorial
  mapear-fuentes/           Investiga y mantiene actualizado docs/fuentes.md
  procesar-cablera/         Redacta y publica como borrador los ítems marcados en el panel admin
  aprender-noticiabilidad/  Aprende de lo publicado/descartado y actualiza docs/criterios-noticiabilidad.md
  armar-gacetilla/          Redacta gacetillas de prensa DE FUNDER hacia otros medios (dirección inversa a las demás skills)

admin/
  index.html                 Panel de curación ("la cablera") — pendientes/a publicar/descartadas

data/
  backlog.json                Backlog de comunicados candidatos, con estado editorial

pipeline/
  publicar_borrador.py        Sube una nota ya redactada (con imagen opcional) a WordPress como draft
  monitorear_gobierno_er.py   Carga a la cablera las noticias nuevas del Gobierno de ER (API + scraping)

fundacion-wp/
  armar_home.py, armar_menu.py, categorizar.py,
  corregir_fechas.py, rehost_imagenes.py    Scripts de mantenimiento del sitio de la Fundación (WordPress distinto al del medio)
```

## Infraestructura (resumen — detalle en `docs/arquitectura-tecnica.md`)

WordPress queda puertas adentro, solo como backend editorial (nunca renderiza el sitio público) — un frontend a medida (Next.js/Vercel) se encarga de todo lo que ve el lector del medio, para no quedar atado a las limitaciones de un theme. La web institucional de la Fundación, en cambio, sí es un WordPress "normal" con theme (Kadence) — no tiene el mismo requisito de diseño a medida. El motor de agencia (cablera → triage → reescritura con IA → borrador en WordPress) vive en este repo y le habla a WordPress por su API REST. El editor siempre revisa y publica desde WordPress — ninguna skill publica directamente.

## Trabajando con este repo

Si estás usando Claude Code acá, ver [`CLAUDE.md`](CLAUDE.md) para el contexto y las reglas de trabajo.
