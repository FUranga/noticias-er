# Pipeline de publicación

Script chico que toma una noticia ya redactada (la salida de la skill `redactar-noticia`) y la sube a WordPress como borrador (`draft`), lista para que el editor la revise y publique desde el editor nativo de WordPress. Ver `docs/arquitectura-tecnica.md` para el contexto completo del pipeline de agencia.

## 1. Generar la Application Password en WordPress (una sola vez)

1. Entrá a tu WordPress como admin → **Usuarios → Tu perfil**.
2. Bajá hasta la sección **Application Passwords**.
3. Ponele un nombre (ej. `pipeline-agencia`) y generá.
4. Copiá la clave que te muestra (formato `xxxx xxxx xxxx xxxx xxxx xxxx`) — solo se muestra una vez.

Esta clave NO es tu contraseña normal — es una credencial separada, solo para esta integración, que podés revocar en cualquier momento sin afectar tu login.

## 2. Configurar el script (una sola vez)

```
cd pipeline
copy .env.example .env      # (en PowerShell: Copy-Item .env.example .env)
```

Editá `.env` y completá:
- `WP_URL`: la URL de tu WordPress (sin barra al final).
- `WP_USER`: tu usuario de WordPress.
- `WP_APP_PASSWORD`: la clave que generaste en el paso 1.

Instalá las dependencias (una sola vez, requiere Python):
```
pip install -r requirements.txt
```

## 3. Uso normal

1. Pegás un comunicado en la skill `redactar-noticia` (Claude Code) y te devuelve el borrador en este formato:
   ```
   Título: ...

   Bajada: ...

   [Cuerpo en párrafos cortos]

   Fuente: ...
   ```
2. Guardás esa salida en un archivo de texto (ej. `nota.txt`).
3. Corrés:
   ```
   python publicar_borrador.py nota.txt
   ```
4. El script te devuelve el link directo para revisar el borrador en el editor de WordPress. Ahí editás y publicás cuando estés conforme — el script nunca publica solo, siempre crea el post en estado `draft`.

**Antes de correr el script, listar los borradores existentes** (`GET /wp-json/wp/v2/posts?status=draft` con las credenciales de `.env`) si hay chance de que la nota ya se haya subido antes (por ejemplo, si el editor escribió un primer borrador a mano directo en WordPress). `publicar_borrador.py` **siempre crea un post nuevo** — no tiene forma de actualizar uno existente por id. Caso real (2026-09-07): se corrió el script sin chequear y se creó un post duplicado de uno que el editor ya había escrito a mano en WordPress; hubo que mandar el duplicado a la papelera (`DELETE /wp-json/wp/v2/posts/<id>`, sin `force=true` para que sea reversible) y aplicar los cambios sobre el post original (`POST /wp-json/wp/v2/posts/<id>` con `title`/`excerpt`/`content`, sin tocar `status`).

Si estás iterando sobre un borrador ya subido (varias rondas de edición), **releé el post antes de cada actualización** (`GET .../posts/<id>?context=edit`) — el editor puede haber seguido editando a mano en WordPress mientras tanto (incluso puede haber cambiado el `status` a `publish` sin avisar), y una actualización a ciegas pisa esos cambios.

## Notas

- `.env` nunca se commitea (está en `.gitignore`). Si la Application Password se filtra, revocala desde WordPress (Usuarios → Tu perfil → Application Passwords → Revoke) y generá una nueva.
- Este script es intencionalmente simple (un archivo de texto por nota, ejecución manual) — automatizar la ingesta de comunicados (RSS, scraping) es un paso posterior, no parte de esta primera versión.

## Ingesta automatizada (piloto): Gobierno de Entre Ríos

`monitorear_gobierno_er.py` agrega las noticias nuevas del Gobierno de Entre Ríos directo a `data/backlog.json` en estado `pendiente`, **siempre con texto completo real** — no decide ni publica nada, solo evita cargar a mano lo que ya está en el sitio oficial. Ver `docs/fuentes.md` (sección "Gobierno provincial") para el detalle completo de la investigación.

**Solo carga ítems con texto completo** — nunca un título suelto sin cuerpo (no se inventan datos, ver `CLAUDE.md`). La fuente es una API pública (`/api/public/home/noticias`), liviana (sin navegador), que solo trae las **últimas 6** noticias (sin paginación posible, confirmado). Una vez que una noticia sale de esa ventana, no hay forma de conseguir su texto completo — la página de detalle de cada nota (`/noticias/<id>`) está rota en el sitio de origen, no carga contenido para nadie (confirmado con la consola del navegador limpia, sin errores).

**La mitigación es de frecuencia, no de herramienta**: correr este script seguido (pensado para cada 15 min, automatizado en `.github/workflows/monitorear_gobierno_er.yml` — corre en GitHub Actions, no depende de que tu compu esté prendida ni de que estés logueado) para que casi ninguna nota se escape de la ventana antes de verla. Con el ritmo de publicación observado (~1 nota cada 45 min) alcanza de sobra, aunque no hay garantía matemática de cero pérdidas en un día de mucha actividad.

**Fotos**: no se pre-bajan en esta corrida (se evaluó con Playwright/scraping y se decidió que no vale la pena para las 6 "por las dudas"). Cuando el editor elige una nota para publicar, la skill `procesar-cablera` la busca en vivo con el navegador en ese momento — ver `skills/procesar-cablera/SKILL.md`.

No requiere `.env` (API pública, sin credenciales) ni Playwright. Uso local (además de correr solo en GitHub Actions):
```
python monitorear_gobierno_er.py
```
Es seguro correrlo varias veces — no duplica ítems ya cargados.

## Ingesta automatizada: Senado de Entre Ríos

`monitorear_senado_er.py` — mismo patrón que el de Gobierno de ER (solo texto completo, sin fotos pre-bajadas, GitHub Actions cada 15 min en `.github/workflows/monitorear_senado_er.yml`), pero mucho más simple de construir: el sitio es WordPress real con **RSS estándar completo** (`senadoer.gob.ar/feed/`, con `content:encoded`) y **API REST habilitada** — no hizo falta investigar nada especial, ni Wayback Machine ni navegador. Ver `docs/fuentes.md` (sección "Legislatura de Entre Ríos").

```
python monitorear_senado_er.py
```

Uso: Municipio y Concejo Deliberante quedaron pausados por ahora (Municipio bloqueado por un desafío de Cloudflare que no intentamos sortear; Concejo sin investigar todavía) — Diputados sin verificar (dio timeout). Cuando se retomen, probar primero si también son WordPress con `/feed/` antes de asumir que hace falta algo más elaborado.

## Ingesta automatizada: Boletín Oficial de Entre Ríos

`monitorear_boletin_er.py` — bastante más elaborado que los dos anteriores: cada edición tiene ~100 páginas y decenas de normas, así que además de detectar novedades aplica un **filtro mecánico de volumen** antes de cargar a la cablera (nunca editorial — ver `docs/boletin-oficial-proceso.md` para el diseño completo, qué se filtra y por qué, y qué prioridad se asigna a lo que sobrevive).

```
python monitorear_boletin_er.py
```

Requiere `pypdf` (ya en `requirements.txt`) además de `requests`. **Primera corrida**: arranca desde la edición más reciente del índice, nunca desde el histórico completo (el índice tiene ediciones desde 2020). Automatizado en `.github/workflows/monitorear_boletin_er.yml`, corre dos veces por día hábil (09:00 y 15:30 ART) — a diferencia de los otros dos monitores, acá no hace falta cada 15 min: cada corrida levanta un job completo aunque no haya novedad, y no hay urgencia de detectar una norma nueva por minutos como sí la hay con un comunicado de prensa. Ver `docs/boletin-oficial-proceso.md`, "Horario de corrida".

Todo lo filtrado (y un resumen de lo que no se parsea en detalle todavía) queda en `data/log_filtro_boletin.jsonl` — nunca se pierde en silencio, ver el doc de proceso para la idea de revisarlo periódicamente buscando patrones.
