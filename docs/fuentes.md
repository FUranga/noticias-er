# Mapa de fuentes

Registro de organismos y organizaciones a monitorear para la cobertura reactiva de `[NOMBRE DEL MEDIO]` (ver `docs/vision-y-etapas.md`). Mantenido con la skill `mapear-fuentes`.

**Estado de esta primera versión**: armada con una pasada de búsqueda web puntual (no un relevamiento exhaustivo). Las URLs marcadas "confirmado por búsqueda" resolvieron en la búsqueda pero no fueron verificadas ítem por ítem con WebFetch (RSS, estructura de la sección de prensa). Todo lo marcado "no confirmado" necesita trabajo manual o una pasada de `mapear-fuentes`. Priorizar desarrollo económico/producción dentro de cada organismo, por el foco inicial del proyecto.

## Gobierno provincial

- **Portal de noticias del Gobierno de Entre Ríos** — https://www.casadeentrerios.gov.ar/ (confirmado por búsqueda; verificar si es el portal de prensa oficial vigente o un espacio de representación en Buenos Aires — el nombre "Casa de Entre Ríos" sugiere lo segundo, revisar).
- **Portal de comunicación del Gobierno de Entre Ríos** — https://portal.entrerios.gov.ar/comunicacion (confirmado por búsqueda, no verificado en detalle).
- **Ministerio de Producción, Turismo y Desarrollo Económico** — http://www.entrerios.gov.ar/minpro/ (confirmado por búsqueda). Es probablemente la fuente individual más importante del proyecto dado el foco en desarrollo económico — priorizar su verificación y la de si tiene sección de prensa/comunicados propia o depende de la de comunicación general del gobierno.
- Redes: X/Twitter @gobiernoER, Facebook /GobiernoER (confirmado por búsqueda).
- RSS: no confirmado en ninguno de los portales de arriba — revisar manualmente.
- **Pendiente de identificar**: Secretaría/área específica de Trabajo, y de Economía/Hacienda — no confirmado en esta pasada, buscar por separado.

## Legislatura de Entre Ríos

- **Cámara de Diputados** — https://www.hcder.gov.ar/ (confirmado por búsqueda; tiene sección de prensa según la propia búsqueda).
- **Cámara de Senadores** — https://www.senadoer.gob.ar/ (confirmado por búsqueda). Contacto de prensa: prensa@senadoer.gob.ar (según resultado de búsqueda, no verificado directamente).
- Cobertura agregada de ambas cámaras: https://www.legislaturasconectadas.gob.ar/Legislatura/8/Camara-de-Diputados-Provincia-de-Entre-Rios y https://www.legislaturasconectadas.gob.ar/Legislatura/94/Honorable-Camara-de-Senadores-de-Entre-Rios (portal nacional que agrega prensa legislativa provincial — confirmado por búsqueda, útil como fuente secundaria).
- RSS: no confirmado.

## Municipalidad de Paraná

- **Sitio oficial y noticias** — https://www.parana.gob.ar/ , sección de noticias en https://www.parana.gob.ar/noticias (confirmado por búsqueda).
- **Boletín Oficial Digital** — https://boletinoficial.parana.gob.ar/ (confirmado por búsqueda) — relevante para ordenanzas/decretos con impacto económico.
- Redes: X/Twitter @MuniParana (confirmado por búsqueda).
- **Área de desarrollo económico/producción municipal**: no identificada en esta pasada — buscar por separado (suele depender de una Secretaría de Producción o de Desarrollo Económico municipal).
- RSS: no confirmado.

## Concejo Deliberante de Paraná

- **Sitio oficial** — https://hcdparana.gob.ar/ (confirmado por búsqueda).
- **Gobierno Abierto (actividad legislativa histórica de concejales)** — https://gobiernoabierto.hcdparana.gob.ar/index.php (confirmado por búsqueda) — potencialmente útil para verificar votos/autoría de proyectos.
- RSS: no confirmado.

## Organizaciones privadas/empresarias

- **Unión Industrial de Entre Ríos (UIER)** — https://uier.org.ar/ (confirmado por búsqueda, fundada en 2003).
- **Consejo Empresario de Entre Ríos (CEER)** — https://www.ceer.org/ (confirmado por búsqueda; publica notas de prensa directamente en el sitio, ej. reuniones con el gobernador).
- **Cámara de Comercio de Paraná/Entre Ríos**: no confirmada en esta pasada — buscar por separado.
- **Bolsa de Cereales de Entre Ríos, Sociedad Rural, otras cámaras sectoriales** (agro, construcción, comercio exterior): no confirmadas en esta pasada — pendiente de investigación específica, alta prioridad dado el foco en desarrollo económico y el peso del agro en la provincia.
- RSS: no confirmado en ninguna.

## Sindicatos

**No confirmado en esta pasada.** Pendiente: identificar los gremios con mayor actividad pública en Paraná/Entre Ríos — al menos estatales (ej. algún gremio estatal provincial), docentes (AGMER), comercio (empleados de comercio), construcción (UOCRA) e industria (según los sectores que releve UIER). Requiere una búsqueda dedicada, no se hizo en esta pasada por prioridad al resto de las categorías.

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

- **Sindicatos**: categoría entera sin trabajar — prioridad alta para la próxima pasada de `mapear-fuentes`.
- **Cámaras sectoriales específicas** (agro, comercio, construcción) dentro de "Organizaciones privadas/empresarias": sin confirmar, prioridad alta dado el foco en desarrollo económico.
- **RSS**: no se verificó ninguno en esta pasada — antes de armar cualquier automatización de ingesta, confirmar cuáles fuentes tienen feed real vs. cuáles requieren revisión manual o scraping.
- **Área de desarrollo económico municipal** (Paraná) y **Secretaría de Trabajo/Economía provincial**: no identificadas, buscar por separado.
- Confirmar si "Casa de Entre Ríos" es efectivamente el portal de prensa del gobierno provincial o una oficina de representación — la búsqueda inicial no lo dejó claro.
- Esta lista prioriza cantidad de cobertura sobre verificación exhaustiva de cada URL (RSS, vigencia de la sección de prensa) — antes de depender de ella para producción, correr una auditoría con `mapear-fuentes`.
