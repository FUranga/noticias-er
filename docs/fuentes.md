# Mapa de fuentes

Registro de organismos y organizaciones a monitorear para la cobertura reactiva de `Agencia Entrerriana` (ver `docs/vision-y-etapas.md`). Mantenido con la skill `mapear-fuentes`.

**Estado de esta primera versión**: armada con una pasada de búsqueda web puntual (no un relevamiento exhaustivo). Las URLs marcadas "confirmado por búsqueda" resolvieron en la búsqueda pero no fueron verificadas ítem por ítem con WebFetch (RSS, estructura de la sección de prensa). Todo lo marcado "no confirmado" necesita trabajo manual o una pasada de `mapear-fuentes`. Priorizar desarrollo económico/producción dentro de cada organismo, por el foco inicial del proyecto.

## Gobierno provincial

- **Casa de Entre Ríos** — https://www.casadeentrerios.gov.ar/ — **no es el portal de prensa del gobierno provincial**: es la Representación del Gobierno de Entre Ríos en la Ciudad de Buenos Aires (Suipacha 844, CABA), con agenda de gestión, servicios a estudiantes/residentes entrerrianos y actividades culturales/turísticas — confirmado por búsqueda y WebFetch (2026-09-03). No es fuente prioritaria para cobertura de desarrollo económico provincial; podría servir puntualmente para novedades institucionales de esa delegación, no más.
- **Portal de noticias/comunicación del Gobierno de Entre Ríos** — https://portal.entrerios.gov.ar/noticias/ (equivalente a https://portal.entrerios.gov.ar/comunicacion; `noticias.entrerios.gov.ar` redirige acá). Confirmado por navegador real (2026-09-03): la página sirve 25+ notas del día con fecha/categoría/bajada — excelente fuente, la más rica de todas las auditadas. Contacto: **Secretaría de Comunicación y Prensa — seccomunicacion@entrerios.gov.ar** (confirmado por WebFetch, pie de página del sitio), Casa de Gobierno, 0800-555-8500.
  - **API JSON pública encontrada (2026-09-03) — no hace falta navegador/scraping para esta fuente**: `https://portal.entrerios.gov.ar/api/public/home/noticias` responde con una petición HTTP simple (sin JS, sin cookies) y devuelve JSON limpio con título, copete, texto completo en HTML, fecha, imagen y organismo de cada nota — confirmado con `curl`/`Invoke-WebRequest` directo. **Confirmado que las 6 son estrictamente las últimas por `fecha_publicacion`** (no una selección curada a mano) — ritmo observado el 2026-09-03: ~1 nota cada 45 minutos, así que sondear cada 30-60 min no debería perder ninguna en un día normal (ajustar el intervalo en días de mucho volumen).
  - **Limitación confirmada como definitiva (2026-09-03), no solo "sin resolver"**: `/api/public/home/noticias` es un endpoint fijo de portada — probado con más de 10 nombres de parámetro de paginación (pagina, page, limit, cantidad, cant, top, n, registros, qty, max) y siempre devuelve exactamente 6, incluso por POST (rechazado, 405 — es GET-only). Se investigó si el listado completo de la página `/noticias/` (25+ notas) se arma con una llamada aparte del lado del cliente: **no es así** — se confirmó bajando y grepeando el bundle JS principal (sin la ruta ahí) y, de forma concluyente, revisando la pestaña de red de un navegador real mientras se cargaba y scrolleaba la página completa hasta el pie: cero llamadas nuevas, ni siquiera al hacer scroll (no hay "cargar más" ni scroll infinito). **Conclusión: el listado completo se arma enteramente en el servidor (SSR) al pedir la página HTML, y no hay ninguna API pública separada para obtenerlo.**
  - **Bug adicional del sitio, también confirmado (2026-09-03)**: la página de detalle de cada nota (`/noticias/<id>`) no carga contenido — ni accediendo directo ni haciendo click real dentro de la propia app (probado de las dos formas, y con la consola del navegador limpia, sin errores — no hay nada que arreglar de nuestro lado). Es un problema del lado de ellos. Consecuencia práctica: el texto completo de una nota solo se puede conseguir si esa nota está entre las 6 últimas de `/api/public/home/noticias` en el momento de la consulta — una vez que sale de esa ventana, se pierde para siempre por esta vía. Por eso `pipeline/monitorear_gobierno_er.py` **no carga títulos sueltos sin texto** (ensuciaban la cablera sin ser accionables) — la mitigación real es correr el script seguido (cada 15-20 min) para que casi nada se escape de la ventana de 6.
  - **Fotos**: no hay URL de imagen descargable aparte — vienen incrustadas en el HTML como `data:image/...;base64,...`, y solo se montan en el DOM después de hacer scroll (carga diferida; sin scrollear, cero imágenes aparecen). Confirmado que son fotos reales y distintas por nota (no un placeholder repetido), 1920px de ancho típico. **Decisión (2026-09-03)**: no vale la pena pre-bajar la foto de las 6 en cada corrida automática "por las dudas" — se busca en vivo con el navegador recién cuando el editor elige una nota puntual para publicar (ver `skills/procesar-cablera/SKILL.md`).
  - **Implementado (2026-09-03)**: `pipeline/monitorear_gobierno_er.py` — script liviano (sin navegador, solo `requests`) que carga a `data/backlog.json` como `pendiente` (deduplicado por id) las noticias con texto completo real de la API. Corre cada 15 min en GitHub Actions (`.github/workflows/monitorear_gobierno_er.yml`), no depende de que la compu del editor esté prendida ni logueada. Ver `pipeline/README.md`.
  - **Cómo se encontró**: la página web en sí está detrás de un filtro anti-bot (un cliente HTTP simple recibe una respuesta casi vacía; solo un navegador real ve el contenido completo), pero **el endpoint de la API no está protegido igual** y responde directo. Se localizó consultando el historial de URLs indexadas por Wayback Machine (`web.archive.org/cdx/search/cdx?url=portal.entrerios.gov.ar*&output=json`) — reveló rutas `/api/public/...` que en algún momento alguien (browser o crawler) visitó directamente. **Técnica reutilizable para las demás fuentes de gobierno** (Municipio, Concejo, Legislatura) antes de asumir que hace falta un scraper con navegador — barato de probar.
- **Ministerio de Producción, Turismo y Desarrollo Económico** — http://www.entrerios.gov.ar/minpro/ (confirmado por búsqueda). Es probablemente la fuente individual más importante del proyecto dado el foco en desarrollo económico — priorizar su verificación y la de si tiene sección de prensa/comunicados propia o depende de la de comunicación general del gobierno.
- Redes: X/Twitter @gobiernoER, Facebook /GobiernoER (confirmado por búsqueda).
- RSS: no confirmado en ninguno de los portales de arriba — revisar manualmente.
- **Secretaría de Trabajo y Seguridad Social** — el dominio histórico `entrerios.gov.ar/sectrabajo/` redirige (302) a https://portal.entrerios.gov.ar/gobiernoytrabajo/ (Ministerio de Gobierno y Trabajo), confirmado por WebFetch (2026-09-03). No se pudo inspeccionar la estructura de secciones/RSS: el portal usa carga dinámica y WebFetch solo devuelve el encabezado — revisar manualmente en el navegador.
- **Ministerio de Economía, Hacienda y Finanzas** — el dominio histórico `entrerios.gov.ar/minecon/` redirige (302) a https://portal.entrerios.gov.ar/haciendayfinanzas/, confirmado por WebFetch (2026-09-03). Mismo problema de inspección (sitio dinámico) — revisar manualmente.
- **Nota general**: el gobierno provincial parece estar migrando todos sus sitios de organismo (`entrerios.gov.ar/<sigla>/`) al portal unificado `portal.entrerios.gov.ar/<área>/` — al auditar cualquier URL vieja de `entrerios.gov.ar`, esperar un redirect y actualizar al dominio nuevo.

## Legislatura de Entre Ríos

- **Cámara de Diputados** — https://www.hcder.gov.ar/ (confirmado por búsqueda; tiene sección de prensa según la propia búsqueda). Sin verificar en detalle — el sitio dio timeout en las pruebas de conexión directa (2026-09-04), revisar más adelante.
- **Cámara de Senadores** — https://www.senadoer.gob.ar/ (confirmado por búsqueda). Contacto de prensa: prensa@senadoer.gob.ar (según resultado de búsqueda, no verificado directamente).
  - **Implementado (2026-09-04)**: es WordPress real, con **RSS estándar completo y funcional** en `https://www.senadoer.gob.ar/feed/` — título, fecha, autor y texto completo (`content:encoded`) de las últimas 10 notas, sin autenticación, sin bloqueo. La fuente más simple de todas las auditadas hasta ahora, mucho más fácil que Gobierno de ER (no hizo falta Wayback Machine ni ninguna técnica especial). También tiene la **API REST de WordPress habilitada** (`/wp-json/wp/v2/posts?_embed`), útil para conseguir la foto destacada de una nota puntual sin navegador — ver `skills/procesar-cablera/SKILL.md`.
  - `pipeline/monitorear_senado_er.py` carga a `data/backlog.json` las notas del feed con texto completo, deduplicado por slug. Corre cada 15 min en GitHub Actions (`.github/workflows/monitorear_senado_er.yml`).
  - Límite conocido: el feed trae solo las últimas 10 notas por defecto (no confirmada paginación) — correr seguido para no perderse ninguna, igual que con Gobierno de ER.
- Cobertura agregada de ambas cámaras: https://www.legislaturasconectadas.gob.ar/Legislatura/8/Camara-de-Diputados-Provincia-de-Entre-Rios y https://www.legislaturasconectadas.gob.ar/Legislatura/94/Honorable-Camara-de-Senadores-de-Entre-Rios (portal nacional que agrega prensa legislativa provincial — confirmado por búsqueda, útil como fuente secundaria).

## Municipalidad de Paraná

- **Sitio oficial y noticias** — https://www.parana.gob.ar/ , sección de noticias en https://www.parana.gob.ar/noticias (confirmado por búsqueda).
- **Boletín Oficial Digital** — https://boletinoficial.parana.gob.ar/ (confirmado por búsqueda) — relevante para ordenanzas/decretos con impacto económico.
- Redes: X/Twitter @MuniParana (confirmado por búsqueda).
- **Secretaría de Producción, Innovación y Empleo** (área de desarrollo económico municipal) — sección temática en https://parana.gob.ar/areastematicas/desarrolloeconomico/ (confirmado por búsqueda, ej. subsección de Programas de Empleo; menciona también Subsecretaría de Producción). **No verificado por WebFetch**: tanto esta URL como `parana.gob.ar/autoridades` devolvieron error 403 (el sitio bloquea fetch automatizado) — confirmar estructura y sección de prensa accediendo manualmente desde un navegador.
- RSS: no confirmado.

## Concejo Deliberante de Paraná

- **Sitio oficial** — https://hcdparana.gob.ar/ (confirmado por búsqueda).
- **Gobierno Abierto (actividad legislativa histórica de concejales)** — https://gobiernoabierto.hcdparana.gob.ar/index.php (confirmado por búsqueda) — potencialmente útil para verificar votos/autoría de proyectos.
- RSS: no confirmado.

## Organizaciones privadas/empresarias

- **Unión Industrial de Entre Ríos (UIER)** — https://uier.org.ar/ (confirmado por búsqueda, fundada en 2003).
- **Consejo Empresario de Entre Ríos (CEER)** — https://www.ceer.org/ (confirmado por búsqueda; publica notas de prensa directamente en el sitio, ej. reuniones con el gobernador).
- **Centro Comercial e Industrial de Paraná** (cámara de comercio local, fundada 1898) — https://centrocomercialparana.com.ar/ (confirmado por búsqueda). Contenido verificado mayormente institucional/histórico; no se confirmó una sección de prensa/comunicados activa — revisar manualmente antes de depender de esta fuente para novedades.
- **Federación Económica de Entre Ríos (FEDER)** — https://federentrerios.com.ar/ (confirmado). Sección de prensa: https://federentrerios.com.ar/prensa/ (confirmado por WebFetch). Federa centros comerciales, cámaras y asociaciones de toda la provincia (comercio, industria, turismo, servicios) — buena fuente agregada para desarrollo económico. RSS no confirmado.
- **CACEPER — Cámara de Comercio Exterior de Entre Ríos** — https://caceper.com.ar/wordpress/ (confirmado por búsqueda, contacto de prensa: prensa@caceper.com.ar según búsqueda, no verificado directamente). No verificado en detalle.
- **CAMARCO — Cámara Argentina de la Construcción, Delegación Entre Ríos** — https://camarcoentrerios.org.ar/ (confirmado por WebFetch). Sección de novedades: https://camarcoentrerios.org.ar/novedades. **RSS confirmado**: https://camarcoentrerios.org.ar/rss.xml.
- **Bolsa de Cereales de Entre Ríos** (agro) — https://www.bolsacer.org.ar/site/ (confirmado por WebFetch). Sección de noticias: https://www.bolsacer.org.ar/site/blog/ (incluye "Actualidad institucional", "Actualidad de interés", "Publicaciones"). RSS no confirmado (el sitio ofrece suscripción por WhatsApp, no feed tradicional).
- **Sociedad Rural de Paraná** (agro) — sin sitio propio confirmado en esta pasada. Dirección física: Almafuerte 2954, Paraná. Monitorear vía redes o prensa local hasta confirmar canal propio — revisar manualmente.
- RSS: confirmado solo en CAMARCO Entre Ríos (ver arriba); no confirmado en el resto.

## Sindicatos

- **AGMER — Asociación Gremial del Magisterio de Entre Ríos** (docentes) — https://2025.agmer.org.ar/ (confirmado por búsqueda). **Atención**: el dominio parece versionarse por año (`2025.agmer.org.ar`); verificar en próximas auditorías si cambió a `2026.agmer.org.ar` u otro esquema estable. Sección de noticias en el home, bajo categorías como "Acción Social" y "Generales"; RSS no confirmado.
- **ATE Entre Ríos — Asociación Trabajadores del Estado** (estatales) — https://ateentrerios.org.ar/ (confirmado por WebFetch). Sección de noticias en el home; RSS no confirmado explícitamente (sitio en WordPress, podría tener `/feed/` sin verificar).
- **UPCN Entre Ríos — Unión del Personal Civil de la Nación**, seccional (estatales) — https://www.upcndigital.org/entre-rios/ (confirmado por búsqueda). **No verificado por WebFetch** (error de certificado SSL al intentar acceder) — revisar manualmente.
- **Sindicato de Empleados de Comercio de Paraná** — https://secparana.com.ar/ (confirmado por búsqueda). No verificado en detalle — revisar sección de novedades/prensa manualmente.
- **UOM Paraná — Unión Obrera Metalúrgica**, seccional (industria) — http://uomparana.org.ar/ (confirmado por búsqueda). Sección de novedades: https://uomparana.org.ar/novedades.asp.
- **UOCRA — Unión Obrera de la Construcción**, seccional Paraná — sin sitio propio de la seccional; sitio nacional https://www.uocra.org/ (listado de seccionales: https://www.uocra.org/?z=2). Seccional Paraná: Andrés Pazos 176, Paraná — monitorear vía sitio nacional o redes (@uocra_seccparana en Instagram, confirmado por búsqueda) hasta confirmar canal propio.
- **Excepción — Sindicato de Empleados de Comercio de Gualeguaychú** — https://secgchu.org/ (confirmado por WebFetch, tiene sección de noticias). Es de Gualeguaychú, no Paraná; se mantiene en el listado como caso aparte (no como fuente prioritaria de la capital) porque ya fue verificado y puede servir de referencia si se cubre algo a nivel provincial.
- **ATSA Entre Ríos — Asociación de Trabajadores de la Sanidad Argentina** (salud privada) — https://atsaentrerios.com.ar/ (confirmado por WebFetch). Sección de noticias: https://atsaentrerios.com.ar/noticias/. RSS no confirmado.
- **AGDU — Asociación Gremial de Docentes Universitarios de Entre Ríos** (docentes UNER) — https://agdu.org.ar/ (confirmado por WebFetch). Sección de novedades: https://agdu.org.ar/novedades/. RSS no confirmado.
- **SADOP Entre Ríos — Sindicato Argentino de Docentes Privados** (docentes de gestión privada) — https://sadopentrerios.org/ (confirmado por WebFetch). Sección provincial: https://sadopentrerios.org/cat/entre-rios/ (paritarias, medidas de fuerza, comunicados de la seccional). RSS no confirmado.
- **CGT Regional Paraná** — sin sitio propio confirmado; agrupa 53 sindicatos de la región según búsqueda. Canales: X/Twitter @cgtparana, Facebook /cgtregionalparana (confirmado por búsqueda) — monitorear vía redes hasta confirmar sitio propio.
- **CTA (Central de Trabajadores) Entre Ríos** — sin sitio propio; comunicados publicados en el sitio nacional bajo la etiqueta Entre Ríos: https://www.cta.org.ar/_cta-entre-rios_.html (confirmado por búsqueda). Nota: existen dos ramas (CTA-T y CTA Autónoma) a nivel nacional — no confirmado en esta pasada si ambas tienen actividad diferenciada en Entre Ríos, revisar.
- **Pendiente**: no se identificó una federación única que centralice todos los gremios estatales/docentes/salud — cada uno publica por separado. Revisar en el futuro si conviene sumar algún gremio sectorial adicional (ej. camioneros, docentes AGMER ya cubierto arriba).
- RSS: no confirmado en ninguna entrada de esta categoría.

## ONGs e instituciones académicas

- **Universidad Nacional de Entre Ríos (UNER)** — https://uner.edu.ar/ (confirmado por búsqueda; rectorado en Concepción del Uruguay, sede también en Paraná/Oro Verde).
- **Universidad Autónoma de Entre Ríos (UADER)** — portal de noticias: https://noticias.uader.edu.ar/ (confirmado por búsqueda).
- **ONGs de desarrollo económico/social locales**: no confirmadas en esta pasada — pendiente de investigación específica.

## Medios locales (para pensar alianzas, no para replicar cobertura)

Ver `docs/aliados-y-financiamiento.md` sobre la lógica de citar/linkear en vez de competir.

- **Elonce** — https://www.elonce.com/ (confirmado por búsqueda). El primer portal de noticias de Entre Ríos (2003); cobertura generalista amplia.
- **Análisis Digital** — https://www.analisisdigital.com.ar/ (confirmado por búsqueda). Dirigido por Daniel Enz; foco declarado en política, judiciales, gestión y economía — es el que más se superpone temáticamente con este proyecto, vale la pena pensarlo primero como posible aliado/competidor a diferenciar.
- **APF Digital** — https://www.apfdigital.com.ar/ (confirmado por búsqueda).
- **El Diario** — https://www.eldiario.com.ar/ (confirmado por búsqueda). El diario papel histórico de Paraná (1914) — máxima jerarquía dentro de los medios locales tradicionales.

## Próximos pasos

- **Sindicatos y cámaras sectoriales** (agro, comercio, construcción, salud, docentes universitarios/privados, CGT/CTA regional): completados en esta pasada (2026-09-03) — ver secciones arriba.
- **Verificar manualmente** (URLs encontradas pero no confirmadas en detalle): UPCN Entre Ríos (error de certificado SSL al intentar WebFetch), Sindicato de Empleados de Comercio de Paraná, CACEPER, Centro Comercial e Industrial de Paraná (sección de prensa no confirmada), Sociedad Rural de Paraná (sin sitio propio encontrado), CGT Regional Paraná (sin sitio propio, solo redes).
- **RSS**: se confirmó un caso (CAMARCO Entre Ríos, https://camarcoentrerios.org.ar/rss.xml). El resto sigue sin verificar — antes de armar cualquier automatización de ingesta, confirmar cuáles fuentes tienen feed real vs. cuáles requieren revisión manual o scraping.
- ~~Área de desarrollo económico municipal (Paraná) y Secretaría de Trabajo/Economía provincial~~ — resuelto (2026-09-03), ver secciones "Gobierno provincial" y "Municipalidad de Paraná" arriba. Pendiente de verificación manual en varios casos porque los sitios oficiales (provincial y municipal) bloquean o limitan el fetch automatizado — revisar en navegador antes de depender de ellos para producción.
- ~~Confirmar si "Casa de Entre Ríos" es el portal de prensa oficial~~ — resuelto (2026-09-03): es la oficina de representación en Buenos Aires, no el portal de prensa. El portal correcto es https://portal.entrerios.gov.ar/noticias/ (ver sección Gobierno provincial).
- Esta lista prioriza cantidad de cobertura sobre verificación exhaustiva de cada URL (RSS, vigencia de la sección de prensa) — antes de depender de ella para producción, correr una auditoría con `mapear-fuentes`.
