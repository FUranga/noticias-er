# Aliados y financiamiento

Documento vivo — esto es terreno para pensar con el usuario, no un plan cerrado. Lo abrimos porque son dos preguntas que van a condicionar decisiones de producto desde el día uno (qué cubrir, qué no, cómo linkear).

## Filosofía: agencia y curaduría, no repetición

La lógica de todo el proyecto (ver [vision-y-etapas.md](vision-y-etapas.md)) es no duplicar cobertura que ya existe y funciona bien. Eso implica dos cosas prácticas:

1. **Linkear en vez de reescribir** lo que un medio local ya cubre bien en su nicho (policiales, deportes, espectáculos, sociedad) — nuestra nota de desarrollo económico puede citar y linkear una cobertura de otro medio como contexto, sin reescribirla.
2. **Ofrecer nuestro despacho a otros medios**, no solo consumir el de ellos. Si el valor que aportamos es curaduría + reescritura seria de comunicados institucionales, ese despacho puede ser útil para medios locales más chicos que hoy no tienen tiempo/equipo para procesar bien esos comunicados. Eso convierte a un competidor potencial en un aliado de distribución.

## Precedente directo: The Texas Tribune

Vale la pena mirarlo en detalle porque el usuario ya lo puso como referencia estética, pero el modelo de negocio es igual de relevante:
- Nonprofit, fundado por periodistas + filantropía inicial (parecido a nuestro punto de partida: una fundación).
- **Política de republicación gratuita**: cualquier medio de Texas puede republicar sus notas sin costo, con atribución. Esto multiplicó su alcance sin competir de frente con medios locales — al contrario, los alimenta.
- Ingresos diversificados: membresías de lectores, eventos (el "Texas Tribune Festival" es una fuente de ingresos y de marca en sí misma), sponsors corporativos con reglas éticas claras de separación entre redacción y sponsoreo, y subvenciones de fundaciones periodísticas.

Es razonable tomar esto como modelo de referencia para etapas 2 en adelante (alianzas + eventos + financiamiento), no solo para el diseño del sitio.

## Posibles aliados (a validar, no confirmados)

- **Medios locales existentes** (ver categoría "Medios locales" en [fuentes.md](fuentes.md)): posible esquema de sindicación — ellos republican nuestras notas de desarrollo económico/política institucional con atribución, nosotros linkeamos su cobertura de nicho (policiales, deportes, sociedad) en vez de cubrirla nosotros mismos.
  - **Idea de implementación, todavía no construida** (2026-09-04, cuando se llegue a la categoría "medios" en el orden de expansión de fuentes — ver `docs/fuentes.md` y la prioridad 5 del roadmap): la cablera (`admin/index.html`) probablemente necesite una solapa propia para ítems que vienen de otro medio, distinta de "gobierno"/"organizaciones" — porque el tratamiento editorial cambia: hay que buscar y citar la fuente original (no reescribir la cobertura ajena como si fuera propia, ver la sección "Medios y empresas como fuente" en `docs/estilo-editorial.md`), o directamente **linkear al medio en vez de escribir nada propio** cuando no hay valor agregado real. Esto se conecta directo con la estrategia de alianzas de arriba: cómo tratemos a un medio chico en la cablera (citarlo bien, linkearlo, no pisarle tráfico) es parte de construir la relación para una eventual sindicación, no solo una regla de estilo.
- **Universidades locales** (UNER, UADER): colaboración en data journalism, acceso a especialistas para dar contexto, pasantías para periodistas jóvenes en etapas futuras.
- **Otras fundaciones y redes de periodismo** (a nivel nacional/regional: SembraMedia, ICFJ, Google News Initiative, LATAM Fact-Checking Network, etc.): posibles fuentes de financiamiento, capacitación o intercambio de infraestructura — requiere investigación específica, no incluido en esta primera pasada.
- **Organismos de datos abiertos / transparencia**: si en la etapa de la sección de datos se necesita presión o asesoría para acceso a datos públicos, hay redes de ONGs de transparencia (ej. ACIJ, Directorio Legislativo a nivel nacional) que podrían sumarse como aliados técnicos, no como fuente de noticias.

## Posibles vías de financiamiento (a explorar, no decidido)

- **Financiamiento institucional inicial**: la Fundación para el Desarrollo Entrerriano como sostén de arranque — esto ya es una ventaja de partida frente a un medio nuevo típico.
- **Membresías de lectores** (modelo Texas Tribune / La Diaria Uruguay): pago voluntario o suscripción de lectores que valoran el periodismo serio, sin necesariamente poner todo el contenido detrás de paywall.
- **Sponsoreo editorial transparente** (modelo NPR/Texas Tribune "underwriting"): empresas o instituciones sponsorean secciones o el newsletter con reglas éticas explícitas de separación entre redacción y comercial — no publicidad intrusiva tradicional.
- **Contenido patrocinado claramente etiquetado**, si se decide en el futuro, siempre con líneas éticas explícitas y separación de la redacción.
- **Eventos y capacitaciones** (etapa 5 de la hoja de ruta): ingresos propios una vez que haya marca y audiencia.
- **Subvenciones de fundaciones periodísticas**: requiere mapeo específico de convocatorias vigentes cuando el proyecto tenga más tracción para aplicar.

## Próximos pasos sugeridos
- Decidir si se contacta a algún medio local chico para explorar una alianza piloto de republicación antes del lanzamiiento público.
- Evaluar con la Fundación qué tan abierta está la conversación de sponsors/membresías desde el arranque vs. dejarlo para la etapa 5.
- Mapear convocatorias de fondos de periodismo (nacional/regional) con fecha vigente cuando haya un prototipo mostrable.
