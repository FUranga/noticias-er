# Newsletter — producto principal (por ahora)

Decisión de Francisco (2026-10-08): el producto principal del medio pasa a ser un **newsletter temático de política y economía de Entre Ríos con lectura del editor**, no la nota individual. "Por ahora": si el proyecto evoluciona, el producto también. Contexto y razones en `docs/vision-y-etapas.md` (sección "Foco actual (2026-10-08)").

## Por qué

El circuito comunicado → verificación → reescritura → publicación resultó demasiado caro por ítem para un equipo de Francisco + IA, y mayormente duplicaba lo que otros medios ya cubrían. El newsletter invierte la proporción: la mayoría del contenido es **curaduría atribuida y linkeada** (barata, y a la vez estrategia de vinculación con otros medios), y lo propio aparece donde de verdad aporta: conectar hechos dispersos, leer bien una fuente, señalar lo que falta saber.

## Referencia de formato

**Times Politics** (newsletter de política de The Times; ahí lo firma su editor, acá no — ver abajo) — no el "Daily Briefing" general del mismo diario, que se evaluó primero y se descartó como modelo principal por ser un resumen de titulares sin lectura propia.

Lo que se toma de la referencia:
- Saludo breve de apertura. **Sin firma personal** (decisión de Francisco, 2026-10-08): es el newsletter del medio, no de una persona — voz institucional en primera persona del plural ("lo estamos chequeando").
- **Panorama de apertura**: 1-2 párrafos que encuadran la semana/el día — el hilo que conecta lo que pasó.
- **En breve**: 2-4 líneas cortas con rótulo ("Concurso:", "Magistratura:") — lo que hay que saber pero no merece desarrollo.
- **En la Legislatura**: una línea con el estado de ambas cámaras (qué entró, qué salió, si hay receso). Es la primera versión visible del tracker legislativo de `docs/vision-y-etapas.md`.
- **3-5 temas numerados** con título propio, 100-250 palabras cada uno: hechos atribuidos + qué conecta con qué + qué falta saber.
- Interacción con el lector: una pregunta para responder por mail (y, si funciona, resultados en la edición siguiente).
- Cierre pidiendo feedback.

Lo que **no** se toma:
- Opinión y adjetivación valorativa ("magnificent speech", "it was raw and powerful"). Choca con `docs/estilo-editorial.md`.
- Columnas de opinión, trivia sin verificar, concurso de epígrafes (este último, quizás más adelante).
- Atribución a fuentes en off ("senior Tories are convinced"): no las tenemos todavía. Se compensa con documentos (Boletín Oficial, pedidos de informe, expedientes). Si aparecen fuentes propias, se usan con el estándar de `docs/estilo-editorial.md`.

## Reglas editoriales específicas

- **Análisis sí, opinión no.** Vale decir qué implica un hecho, qué conecta con qué y qué no se sabe (ej. "la nueva movilidad ata todas las jubilaciones provinciales a la paritaria docente" — sale de leer bien la reglamentación, no de un juicio de valor). No vale calificar ni tomar partido.
- **Atribución en cada dato de otro medio u organismo**, con link al original. Lo que viene de otro medio es "según X", no verificado por nosotros, salvo que lo hayamos chequeado — y en ese caso se dice.
- **Lo pendiente se dice como pendiente.** "Lo estamos chequeando" o "no se sabe todavía" es contenido válido; inventar o completar con suposiciones, no (regla general del repo).
- **La IA agrupa y redacta borradores; Francisco elige temas y escribe/aprueba la lectura.** Mismo principio que el resto del pipeline: ninguna skill decide sola qué entra.
- **Fuera de alcance** (deportes, espectáculos): no entra al cuerpo. Si alguna vez hay una sección de cierre con derivaciones a otros medios, es solo link, sin redacción propia. Subproductos temáticos (deporte, cultura) quedan para más adelante, si el principal se sostiene.

## Frecuencia

Arrancar con **dos ediciones por semana** (tentativo: lunes = qué viene; jueves = después de las sesiones legislativas). Pasar a diario solo si la rutina se sostiene. Ajustar con el uso real.

## Proceso (a construir — todavía no hay herramientas)

1. La cablera (`data/backlog.json`) sigue siendo el radar; no cambia la ingesta.
2. Agrupamiento: de los ítems del período, proponer 4-6 grupos temáticos con sus fuentes (trabajo de IA). Francisco elige 3-5.
3. Borrador de la edición con la estructura de arriba, marcando entre corchetes todo dato faltante o a verificar.
4. Edición y aprobación de Francisco.
5. Envío (plataforma sin decidir: Buttondown/Beehiiv/Substack/Ghost) y archivo de la edición en el sitio (contenido web para SEO/GEO sin depender de notas sueltas).

Antes de construir la skill (`armar-newsletter`) y los cambios al panel (marca "va al newsletter" + sección, como campo del ítem, no estado nuevo), **probar una o dos ediciones reales a mano**.

## Pendientes técnicos detectados en el prototipo

- Muchos ítems de medios llegan vía Google News: solo título y link redirigido (`news.google.com/rss/articles/...`). Para linkear hace falta resolver la URL real del medio y, idealmente, bajar la bajada.
- El volumen del Boletín Oficial ensucia la vista del período; el agrupamiento debería trabajar sobre lo que sobrevive el filtro de `docs/boletin-oficial-proceso.md`.

## Prototipo

Primer prototipo (con material real de la cablera del 6 al 8 de octubre de 2026): `newsletter/borradores/2026-10-08-prototipo.md`.
