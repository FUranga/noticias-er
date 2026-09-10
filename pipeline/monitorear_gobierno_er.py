r"""
Ingesta automatizada del Gobierno de Entre Rios: agrega noticias nuevas a la
cablera (data/backlog.json) en estado "pendiente".

No decide nada -- solo carga candidatos para que el editor los triage despues
en admin/index.html, igual que si los hubiera pegado a mano. Ver CLAUDE.md:
la decision de que es noticia es siempre humana, y nunca se inventan datos --
por eso este script SOLO carga items con texto completo real (nunca un
titulo suelto sin cuerpo).

Fuente: API publica `/api/public/home/noticias` -- sin autenticacion, sin
navegador, devuelve titulo/copete/texto completo/fecha/organismo de las
ULTIMAS 6 noticias. Ver docs/fuentes.md (seccion "Gobierno provincial") para
el detalle completo de como se encontro y sus limites:

  - Es GET-only, sin paginacion (probado con mas de 10 nombres de parametro
    distintos): siempre devuelve exactamente las ultimas 6, estrictamente por
    fecha de publicacion (no una seleccion curada).
  - No hay forma de conseguir el texto completo de una nota una vez que sale
    de esa ventana de 6 -- la pagina de detalle (`/noticias/<id>`) esta rota
    en el sitio de origen, no carga contenido para nadie (confirmado con la
    consola del navegador limpia, sin errores). El campo `link` de cada item
    apunta ahi de todas formas, como identificador -- no esperar que abra
    contenido si la nota ya no esta entre las ultimas 6.

Por eso la mitigacion es de frecuencia, no de herramienta: correr este
script seguido (pensado para cada 15 min via GitHub Actions -- ver
.github/workflows/monitorear_gobierno_er.yml) para que casi ninguna noticia
nueva se escape de la ventana de 6 antes de que este script la vea. Con el
ritmo de publicacion observado (~1 nota cada 45 min) alcanza holgadamente.

Fotos: no se capturan automaticamente en esta corrida (ver docs/fuentes.md
y el historial de decisiones -- se probo con Playwright/scraping y se decidio
que no vale la pena pre-bajar fotos de las 6 "por las dudas"). Cuando el
editor elige una nota para publicar, la foto se busca en vivo con el
navegador en ese momento -- ver `skills/procesar-cablera/SKILL.md`.

Uso:
    python monitorear_gobierno_er.py

Sin dependencias pesadas: solo `requests` (ver requirements.txt). No requiere
credenciales (API publica).
"""

import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

API_URL = "https://portal.entrerios.gov.ar/api/public/home/noticias"
ARTICULO_URL_TPL = "https://portal.entrerios.gov.ar/noticias/{id}"
FUENTE_ID_PREFIJO = "goberer"

BACKLOG_PATH = Path(__file__).resolve().parent.parent / "data" / "backlog.json"
ARCHIVO_PATHS = [
    Path(__file__).resolve().parent.parent / "data" / "archivo" / "backlog-descartados.json",
    Path(__file__).resolve().parent.parent / "data" / "archivo" / "backlog-publicados.json",
]


def limpiar_html(texto_html: str | None) -> str:
    """Saca tags HTML y decodifica entidades -- deja texto plano legible."""
    if not texto_html:
        return ""
    sin_tags = re.sub(r"<[^>]+>", "\n", texto_html)
    return html.unescape(re.sub(r"\n{3,}", "\n\n", sin_tags)).strip()


def obtener_noticias_api() -> list[dict]:
    resp = requests.get(API_URL, headers={"Accept": "application/json"}, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"La API respondio pero sin 'success': {data}")
    return data.get("data", [])


def cargar_backlog() -> list[dict]:
    if not BACKLOG_PATH.exists():
        return []
    with open(BACKLOG_PATH, encoding="utf-8") as f:
        return json.load(f)


def guardar_backlog(items: list[dict]) -> None:
    with open(BACKLOG_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
        f.write("\n")


def cargar_ids_archivados() -> set[str]:
    """IDs que ya salieron de backlog.json via `archivar_cablera.py` (estado
    descartado/referido, o publicado con wp_edit_url).

    Todos los `monitorear_*.py` tienen que sumar esto a su chequeo de "ya
    existe" antes de agregar un item -- si solo miran `cargar_backlog()`,
    un item ya archivado (que ya no esta en backlog.json) parece nuevo de
    vuelta la proxima corrida, y el scraper lo re-agrega como "pendiente"
    aunque el editor ya lo haya descartado. Confirmado 2026-09-10: 139 de
    324 items archivados habian resurgido asi en la cablera activa.
    """
    ids: set[str] = set()
    for path in ARCHIVO_PATHS:
        if not path.exists():
            continue
        with open(path, encoding="utf-8") as f:
            ids.update(item.get("id") for item in json.load(f))
    return ids


def item_backlog_desde_api(noticia: dict) -> dict:
    organismo = (noticia.get("organismo") or "").strip()
    fuente = f"Gobierno de Entre Rios - {organismo}" if organismo else "Gobierno de Entre Rios"

    copete = limpiar_html(noticia.get("copete"))
    texto = limpiar_html(noticia.get("texto"))
    texto_original = "\n\n".join(p for p in (copete, texto) if p)

    fecha_pub = noticia.get("fecha_publicacion") or ""
    fecha = fecha_pub.split(" ")[0] if fecha_pub else ""

    return {
        "id": f"{FUENTE_ID_PREFIJO}-{noticia['id']}",
        "fuente": fuente,
        "titulo": noticia.get("titulo", "").strip(),
        "fecha": fecha,
        "link": ARTICULO_URL_TPL.format(id=noticia["id"]),
        "texto_original": texto_original,
        "imagen_url": "",
        "estado": "pendiente",
        "agregado_el": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "procesado_el": None,
        "wp_edit_url": None,
        "motivo_descarte": None,
    }


def main() -> None:
    print(f"Consultando {API_URL} ...")
    try:
        noticias = obtener_noticias_api()
    except requests.RequestException as e:
        print(f"No se pudo consultar la API: {e}")
        sys.exit(1)

    backlog = cargar_backlog()
    ids_existentes = {item.get("id") for item in backlog} | cargar_ids_archivados()

    nuevos = []
    for noticia in noticias:
        item = item_backlog_desde_api(noticia)
        if item["id"] in ids_existentes:
            continue
        nuevos.append(item)

    if not nuevos:
        print("Sin novedades: las ultimas 6 ya estaban cargadas.")
        return

    backlog.extend(nuevos)
    guardar_backlog(backlog)

    print(f"Agregados {len(nuevos)} item(s) nuevo(s) a {BACKLOG_PATH}:")
    for item in nuevos:
        print(f"  - [{item['id']}] {item['titulo']}")
    print("\nQuedaron en estado 'pendiente' -- revisalos en admin/index.html.")


if __name__ == "__main__":
    main()
