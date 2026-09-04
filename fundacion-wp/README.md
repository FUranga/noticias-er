# fundacion-wp/

Scripts de mantenimiento para el sitio institucional de la Fundación (`desarrolloentrerriano.org`,
WordPress + theme Kadence). Esto es *distinto* del `pipeline/` de la raíz del repo, que es del
WordPress del medio (`Agencia Entrerriana`) — son dos WordPress separados, dos `.env` separados.

Contexto completo del sitio (estructura, decisiones de contenido, gotchas) en
[`../docs/sitio-fundacion.md`](../docs/sitio-fundacion.md). Pendientes en
[`../docs/checklist-sitio-fundacion.md`](../docs/checklist-sitio-fundacion.md).

## Setup

```
cd fundacion-wp
pip install -r requirements.txt
cp .env.example .env   # completar con la Application Password real
```

`_wp.py` es el módulo compartido que lee `.env` y expone `WP_URL`/`AUTH` — todos los scripts lo importan.

## Scripts

- **`armar_home.py`** — fuente de verdad del HTML de la portada (hero + bloque "Novedades"). Correrlo
  sobreescribe la página "Inicio" (id 55) con exactamente este contenido. Es el script que se edita
  cuando hay que cambiar algo de la home (foto, texto, colores).
- **`armar_menu.py`** — setup inicial de páginas ("Novedades", "Informes") y menú principal. Ya corrido
  una vez; volver a correrlo crea páginas/menú duplicados (no chequea si ya existen). Se preserva como
  referencia de la estructura del menú, no para re-ejecutar tal cual.
- **`categorizar.py`** — asigna categoría (Opinión/Evento/Informe/Entrevista/Institucional) a cada post
  por heurística de título/autor/contenido. Idempotente. Útil si se importa contenido nuevo en lote.
- **`corregir_fechas.py`** — restaura la fecha original de los posts después de un bulk-edit-a-publish
  desde el listado de wp-admin (bug conocido del propio WordPress: resetea `date` a "ahora" si no se
  preserva explícitamente). Matchea por título contra un diccionario hardcodeado + el JSON de históricos.
- **`rehost_imagenes.py`** — escanea todos los posts por `<img src>` externos (hotlinking a
  visiondesarrollista.org / analisisdigital.com.ar) y los re-aloja en la biblioteca de medios propia.
  Idempotente — si no quedan imágenes externas, no hace nada.

## Lo que NO está scripteado (hecho a mano o vía Customizer)

- **Logo, favicon, idioma del sitio (`es_ES`), Enlaces Sociales, Additional CSS** — se configuran desde
  el Customizer de WordPress (`wp-admin/customize.php`) o Ajustes generales. El único caso en que se usó
  la API REST directamente para esto fue `site_logo` (el click en el Customizer no lo guardaba de forma
  confiable) y, en la sesión del 2026-09-03, los enlaces sociales y el texto del footer — ver
  `docs/sitio-fundacion.md` sección "Customizer vía API" para el patrón de JS usado (`wp.customize(...)`).
- **El CSS que saca la franja gris de título y las sombras de las tarjetas** vive en el campo "Additional
  CSS" del Customizer (Apariencia → Personalizar → CSS adicional), no en un archivo de este repo — ver
  el snippet completo en `docs/sitio-fundacion.md`.
- **Import histórico** (54 notas viejas de FUNDER + 20 de Visión Desarrollista + 1 de Análisis Digital):
  se hizo con scripts de un solo uso (`importar_historicos.py`, `importar_vision.py`, etc.) que no se
  preservaron en el repo porque ya cumplieron su función y no son re-ejecutables sin duplicar contenido.
  Las decisiones de qué se importó y qué se excluyó (y por qué) están documentadas en
  `docs/contenido-historico-fundacion.md` y `docs/sitio-fundacion.md`.
