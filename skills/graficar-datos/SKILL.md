---
name: graficar-datos
description: Arma un chart de datos (evolución en el tiempo, variación por categoría) para acompañar una nota, en la estética visual del proyecto hermano `mapa-empleo` (Inter, rojo/verde por dirección del cambio, sin grillas, número grande destacado), con título y bajada propios y una capa de hover interactiva. Publica una versión interactiva como Artifact para revisión y una versión estática (imagen) para insertar en el borrador de WordPress. Usar cuando el usuario pide "hacé un gráfico/chart de...", "visualizá estos datos", o pide actualizar un chart ya hecho por este medio.
---

# Graficar datos para una nota

Contexto: los charts de este medio acompañan notas económicas/institucionales basadas en datos reales (ver `docs/fuentes-datos.md`), muchas veces cruzando el registro oficial que cita una fuente contra un dato más directo (ver el caso real de la nota sobre Dal Molín/Cresto e industria manufacturera, 2026-09-11: el Registro de Establecimientos Industriales decía +19 inscripciones, pero el empleo formal del sector había caído 914 puestos). El chart tiene que sostener ese tipo de hallazgo con la misma rigurosidad que el texto — nunca es decoración.

**Esta skill no decide qué graficar ni qué dice la nota** — eso es trabajo editorial previo (`redactar-noticia`, o la conversación con Francisco). Acá el insumo (qué serie, qué cifras, qué corte temporal) ya está decidido; esta skill se ocupa de construir el chart y de insertarlo donde corresponde.

## Antes de graficar

1. **No inventar el dato — bajar la fuente primero.** Si el dato sale de `mapa-empleo` (`C:\Users\Francisco.Uranga\OneDrive - William Reed Ltd\Documents\proyectos claude\mapa-empleo\data.json` / `empresas.json`), leé el archivo directo con Python antes de escribir cualquier número en el chart — nunca repitas de memoria una cifra de una conversación anterior sin volver a chequearla.
2. **`mapa-empleo` se actualiza solo, mes a mes** (un GitHub Action corre un chequeo diario contra SIPA/OEDE/SRT — ver su propio `README.md`). Antes de reusar una cifra ya graficada en una nota vieja, revisá `meta.actualizado` / `meta.ultimo` en el JSON correspondiente — si avanzó desde la última vez, el chart (y el texto de la nota, si ya está publicada) necesitan actualizarse. Ver `docs/fuentes-datos.md` para qué serie vive en qué archivo y con qué rezago (el trimestral de OEDE por sector/provincia va bastante más atrasado que el mensual de SIPA).
3. **Documentar la fuente verificada en `docs/fuentes-datos.md`** si es la primera vez que se usa ese dato puntual (ver estructura ya existente ahí) — para no repetir la búsqueda la próxima vez.

## El sistema visual (fijo, no reinventar cada vez)

Tomado directo de `mapa-empleo/index.html` (mismo autor/proyecto hermano, para que un chart de acá se sienta de la misma familia si algún día conviven):

```css
--bg:#ffffff; --panel:#ffffff; --ink:#1d1d1f; --muted:#86868b; --hair:#e6e6e8;
--loss:#d0342c; --loss-soft:#fbe7e5; --gain:#1f6f5c; --accent:#0071e3;
font-family:"Inter",-apple-system,BlinkMacSystemFont,"SF Pro Text",system-ui,sans-serif;
```

- **Rojo (`--loss`) = cae, verde (`--gain`) = sube** — nunca al revés, y nunca un tercer color para una tercera categoría (si hace falta un "sin cambio", usar `--muted`, no inventar un color nuevo).
- **Sin grillas ni eje Y con ticks** — el chart tiene labels de inicio/fin del eje X nomás, y el valor de cada punto relevante como texto directo al lado del punto (no una escala que el lector tenga que leer).
- **Línea de 2.5px, círculos huecos (`fill:#fff`, `stroke` del color de la serie) solo en los extremos** — no un punto por cada dato intermedio, eso es ruido visual a esta escala.
- **Área debajo de la línea, con el mismo color al 10-15% de opacidad** (`--loss-soft`) — ayuda a leer la tendencia sin agregar líneas.
- **Barras divergentes desde un cero central** (no desde el borde izquierdo) para variación por categoría — ver plantilla de barras más abajo.

## Estructura de la tarjeta (card)

Todo chart de esta skill es una tarjeta autocontenida de 960px de ancho, con este orden fijo:

1. **Eyebrow** (13px, `--muted`, mayúsculas) — el recorte geográfico/temático, ej. `ENTRE RÍOS · INDUSTRIA MANUFACTURERA`.
2. **Título** (26px, peso 800) — el hallazgo en una oración, no una descripción genérica del eje ("Puestos de trabajo registrados" es débil; "El empleo industrial retrocede en Entre Ríos" sostiene algo). Mismo criterio de título que una nota (`docs/estilo-editorial.md`): sujeto + qué pasa, sin adjetivos de valor.
3. **Bajada/dek** (15px, `--muted`, hasta ~640px de ancho) — una oración con la fuente exacta y el corte temporal, para que la tarjeta se entienda sola si se comparte suelta.
4. **Número grande** (opcional, solo si hay un único número que resume el chart — no lo fuerces en un chart de barras con varias categorías) — 44px, color según dirección.
5. **El chart**, con hover.

Plantillas ya armadas en `skills/graficar-datos/plantillas/`:
- `linea-con-area.html` — evolución en el tiempo (una serie, con hover).
- `barras-divergentes.html` — variación por categoría (barras desde un cero central, con hover).

Partir de esos archivos (copiarlos, no reescribirlos de cero) y reemplazar solo lo marcado en sus comentarios: eyebrow, título, bajada, y el array de datos.

## Interactividad (siempre, no opcional)

Todo chart lleva una capa de hover, aunque termine insertado como imagen estática en WordPress:
- **Línea**: un `<rect>` transparente capturando todo el ancho del SVG, que en `mousemove` busca el punto más cercano en X, mueve un punto de foco y muestra un tooltip (fondo `--ink`, texto blanco, `border-radius:7px`) con la fecha/período y el valor exacto.
- **Barras**: cada fila reacciona a `mouseenter`/`mouseleave` con un fondo sutil (`--neutral`), y un tooltip fijo (`position:fixed`, sigue al cursor) con el detalle que no entra en la barra (ej. el valor absoluto además del %).

## Proceso de publicación

1. Escribir el HTML de la tarjeta (Google Fonts para Inter, JS inline armando el SVG/las filas desde un array de datos con el dato ya verificado).
2. Publicar con `Artifact` (favicon 🏭 para temas de industria/economía, o el que corresponda al tema) — esta es la versión **interactiva**, queda como link para que Francisco la revise y, eventualmente, para compartir suelta si hace falta.
3. **Mirar el render una vez** (`claude-in-chrome`: navegar al link del Artifact, screenshot) antes de darlo por bueno — especialmente los decimales con coma (`.toFixed(1).replace(".", ",")`, JS usa punto por default) y que el tooltip no se corte contra el borde de la tarjeta.
4. Recortar la tarjeta con `computer` `zoom` + `save_to_disk:true` (región ajustada al borde de la card, sin la barra de navegación del visor de artifacts por arriba) — esto da el PNG para insertar en la nota.
5. Subir el PNG a la biblioteca de medios de WordPress (mismo mecanismo que `pipeline/publicar_borrador.py` usa para la imagen destacada, pero a mano vía `requests.post(.../wp-json/wp/v2/media)`) y armar el `caption` con el crédito: `Elaboración propia sobre datos de [fuente] / [organismo]`.
6. Insertar en el cuerpo del post como `<figure><img src="..." style="max-width:100%;height:auto;" /><figcaption>...</figcaption></figure>`, en el punto del texto donde se menciona el dato que grafica — nunca todos los charts amontonados al final.
7. Si el post ya estaba publicado/en borrador y el editor lo venía editando a mano, **releer el `content` actual antes de insertar** (buscar el párrafo ancla por texto) — no asumas que el texto sigue igual a como lo dejaste vos.

## Si falla el screenshot

`claude-in-chrome` puede fallar para el screenshot/crop (pasó una vez, 2026-09-11 — timeout de la extensión en toda pestaña, no solo en el Artifact, ni siquiera con una pestaña en blanco). No hay fallback automático: avisar a Francisco, darle el link del Artifact para que confirme el diseño mirándolo él mismo, y reintentar el crop más tarde en vez de forzarlo o improvisar un método alternativo de captura.
