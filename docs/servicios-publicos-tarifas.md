# Servicios públicos y tarifas — beat de fondo

Documento de referencia para cubrir servicios públicos regulados (energía eléctrica, y a medida que se mapeen, agua/saneamiento, gas y transporte) con profundidad — marco legal, mecanismo de actualización, series históricas y organismos involucrados — para no volver a investigar lo mismo de cero en cada nota nueva. Mismo espíritu que `docs/fuentes-datos.md` (evitar repetir búsquedas) pero para el **funcionamiento de la política regulatoria**, no solo series numéricas.

Distinto de `docs/temas-a-seguir.md` (pistas sueltas sin desarrollar) y de `docs/fuentes.md` (qué organismo monitorear y con qué mecanismo) — acá va el conocimiento de fondo ya consolidado sobre cómo funciona cada servicio, más la lista explícita de lo que todavía falta investigar.

**Por qué existe (2026-09-07)**: al escribir la nota sobre la suba de la tarifa eléctrica social de octubre 2026 (`borradores/tarifa-electrica-social-octubre-2026.md`, publicada en WordPress) quedaron muchas preguntas de fondo sin resolver que exceden esa nota puntual — se abre este documento para acumularlas y para que la próxima nota de tarifas (eléctrica o de otro servicio) parta de más contexto, no de cero.

## Energía eléctrica

### Lo que ya sabemos (verificado sobre fuentes primarias)

- **Marco legal**: Ley Provincial N° 8.916 (Marco Regulatorio Eléctrico) y su modificatoria N° 10.153. El EPRE actúa con las facultades de los Artículos 48° y 56° de la Ley 8.916 (fijar normativa técnica, aprobar cuadros tarifarios).
- **El EPRE no tiene Directorio propio desde 1996** (Decreto N° 1127/96 MEOSP intervino el organismo) — hoy un Interventor con las facultades del Directorio ejerce todas las funciones (Decreto N° 1252/25 GOB, Dr. Marcos Rodríguez Allende al 2026-09). Ver `docs/temas-a-seguir.md` ("El EPRE no tiene Directorio propio desde 1996") para el ángulo institucional de esto — acá solo como dato de contexto operativo.
- **Distribución**: ENERSA es la distribuidora principal, pero el propio cuadro tarifario tiene una categoría separada ("Otros Distribuidores Provinciales") — hay cooperativas u otros distribuidores con tarifa propia dentro de la provincia. **Sin identificar todavía cuáles ni en qué localidades operan** (ver "Preguntas abiertas" abajo).
- **Zonas tarifarias**: el cuadro distingue "Zona Cálida" (Colón, Concordia, Diamante, Federal, Federación, Feliciano, La Paz, Nogoyá, Paraná, San Salvador, Tala, Uruguay y Villaguay) de "Resto" (Victoria, Gualeguay, Gualeguaychú, Islas del Ibicuy) — con cargos fijos y variables distintos.
- **Actualización mensual confirmada**: el EPRE aprueba un nuevo cuadro tarifario todos los meses por resolución propia, tomando como insumo los precios mayoristas que fija mensualmente la Secretaría de Energía de la Nación (POTREF, PEE, PES del Mercado Eléctrico Mayorista) y el Valor Agregado de Distribución (VAD) provincial, ajustado con tope ligado a la variación mensual del índice de salarios del INDEC.
- **Rol Nación vs. Provincia** (parcialmente mapeado):
  - **Nación** (Secretaría de Energía, Ministerio de Economía): fija los precios mayoristas de energía/potencia/transporte del MEM mes a mes, y fija el esquema de subsidios focalizados (Decreto PEN N° 943/25 — reemplazó el esquema anterior de segmentación de usuarios por nivel de ingreso) a través del Registro de Acceso a los Subsidios a la Energía (RASE).
  - **Provincia** (Secretaría de Energía de ER + EPRE): fija el Valor Agregado de Distribución (VAD, el componente que le corresponde a la distribuidora) y traduce los insumos nacionales en el cuadro tarifario final aplicable en la provincia, incluyendo el subsidio provincial adicional sobre el VAD para usuarios de menores ingresos (Resolución 564/25 S.E., prorrogada mes a mes).
- **Audiencias públicas**: el EPRE convoca audiencia pública antes de revisiones tarifarias de fondo (no el ajuste mensual de rutina), con Reglamento propio (Resolución EPRE N° 110/13) y Defensores de los Usuarios designados por colegios profesionales para cada audiencia — mecanismo de participación real verificado (última convocatoria conocida: audiencia del 5/8/2026 en Federación, sobre la Revisión Tarifaria Integral — RTI). Ver `docs/fuentes.md` (entrada EPRE) para el mecanismo de detección de futuras convocatorias.
- **Fuente de consumo de referencia**: un informe del Consejo Empresario de Entre Ríos (CEER) usa 250 kWh/mes como consumo residencial representativo para comparar tarifas entre provincias bajo el mismo esquema nacional — usado como consumo de referencia en la nota de octubre 2026 (ver `docs/estilo-editorial.md`, sección de cuadros tarifarios, para la regla editorial sobre cómo se atribuye esto).

### A verificar antes de repetir el dato (duda abierta, 2026-09-07)

La resolución de octubre 2026 describe, para el esquema nacional (Decreto 943/25), una **bonificación base del 50%** sobre el precio estacional del consumo base, "más una bonificación adicional extraordinaria" que varía mes a mes (25% en septiembre, 4,55% en octubre según la nota publicada). La nota publicada compara solo el componente variable (25% → 4,55%) sin mencionar el piso del 50%. **No se confirmó todavía si ese 50% de base es realmente un piso fijo que se mantiene todos los meses** (en cuyo caso la nota es precisa: describe el componente que efectivamente bajó) **o si en realidad es parte del mismo total que varió** (en cuyo caso faltaría contexto). Antes de repetir esta cifra en otra nota, confirmar leyendo el Decreto PEN N° 943/25 completo (no solo como se cita en la resolución del EPRE) o consultando directamente al EPRE.

## Preguntas abiertas (pedido de Francisco, 2026-09-07, a partir de la nota de octubre 2026)

Ninguna de estas se contesta inventando un número — quedan `para investigar` hasta confirmarlas con fuente primaria, mismo criterio que `docs/temas-a-seguir.md`.

- **¿Qué porcentaje de usuarios de ENERSA (u otros distribuidores) tiene tarifa social / está registrado en el RASE?** El 25%/4,55% citados son porcentajes de *subsidio*, no de *población beneficiaria* — son datos distintos y no hay que confundirlos.
- **Evolución histórica completa del esquema de subsidios y del cuadro tarifario** — no solo mes a mes desde que empezamos a mirarlo (agosto/septiembre 2026), sino desde cuándo existe el esquema de segmentación/RASE, y cómo cambió con las distintas gestiones nacionales.
- **¿Se pueden apelar los aumentos?** Existe el mecanismo de audiencia pública *previa* a una revisión de fondo (ver arriba) — pero no se investigó si un usuario individual (o una asociación de consumidores) tiene una vía de impugnación o recurso administrativo/judicial contra una resolución de cuadro tarifario ya aprobada.
- **¿El esquema aplica a toda la provincia por igual?** Ya sabemos que hay zonas tarifarias distintas (Zona Cálida vs. Resto) y una categoría de "Otros Distribuidores Provinciales" (cooperativas) con tarifa propia — falta identificar cuáles son esos otros distribuidores, en qué localidades operan, y si el esquema nacional de subsidios (RASE) les aplica igual que a los clientes de ENERSA.
- **Identificar a "Otros Distribuidores Provinciales"** — nombre de cada cooperativa/distribuidor, zona de cobertura, y si tienen su propia resolución de cuadro tarifario o dependen de la del EPRE.

## Agua y saneamiento

**Sin mapear todavía.** Pendiente identificar: quién presta el servicio en Paraná y en el resto de la provincia (¿empresa provincial, municipios, cooperativas?), si existe un ente regulador separado del EPRE, y si hay un cuadro tarifario público con la misma periodicidad que el eléctrico.

## Gas

**Sin mapear todavía.** Pendiente identificar si hay una licenciataria de distribución con jurisdicción en Entre Ríos regulada por ENARGAS (nacional) y si la provincia tiene algún rol regulatorio propio (ej. redes de gas natural en zonas rurales, garrafa social).

## Transporte

**Mencionado por Francisco como posible tercer tema, sin mapear todavía.** Pendiente identificar la autoridad de aplicación provincial del transporte interurbano de pasajeros (boleto, subsidios, concesión de líneas) y si hay un mecanismo de actualización de tarifas análogo al eléctrico.

## Cómo se usa

Antes de escribir una nota sobre tarifas o regulación de un servicio público, revisar acá primero — si el mecanismo ya está mapeado, ahorra la investigación de fondo y deja más tiempo para el hecho puntual. Si aparece un dato nuevo que responde una de las preguntas abiertas, actualizar esta sección en vez de dejarlo solo en el borrador de la nota. El mapeo de agua/gas/transporte a nivel provincial se está corriendo aparte (ver commit del mapeo de fuentes de servicios públicos); a nivel municipal, `docs/fuentes.md` solo los identifica, no arma mecanismo de ingesta propio (menor prioridad hasta que haya evidencia de volumen/valor que lo justifique).
