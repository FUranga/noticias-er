r"""
Ingesta automatizada del Senado de Entre Rios: agrega noticias nuevas a la
cablera (data/backlog.json) en estado "pendiente".

No decide nada -- solo carga candidatos para que el editor los triage
despues en admin/index.html. Ver CLAUDE.md: la decision de que es noticia
es siempre humana.

Fuente: RSS estandar de WordPress (`https://www.senadoer.gob.ar/feed/`),
publico, sin autenticacion, con texto completo via content:encoded. Mucho
mas simple que el caso del Gobierno de Entre Rios (ver
pipeline/monitorear_gobierno_er.py) -- no hace falta Wayback Machine ni
ninguna investigacion especial, es un feed real y completo.

Limite conocido: WordPress devuelve los ultimos 10 items por default en
/feed/. Correr seguido (cada 30-60 min es de sobra dado el ritmo de
publicacion de este organismo) para no perderse ninguno.

Uso:
    python monitorear_senado_er.py
"""

import html
import re
import sys
from datetime import timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from xml.etree import ElementTree

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from monitorear_gobierno_er import cargar_backlog, guardar_backlog  # noqa: E402

FEED_URL = "https://www.senadoer.gob.ar/feed/"
FUENTE_ID_PREFIJO = "senadoer"
FUENTE_NOMBRE = "Cámara de Senadores de Entre Ríos"

NS = {"content": "http://purl.org/rss/1.0/modules/content/", "dc": "http://purl.org/dc/elements/1.1/"}


def limpiar_html(texto_html: str | None) -> str:
    if not texto_html:
        return ""
    sin_tags = re.sub(r"<[^>]+>", "\n", texto_html)
    return html.unescape(re.sub(r"\n{3,}", "\n\n", sin_tags)).strip()


def slug_de_link(link: str) -> str:
    return link.rstrip("/").rsplit("/", 1)[-1]


def obtener_noticias() -> list[dict]:
    resp = requests.get(FEED_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    resp.raise_for_status()
    root = ElementTree.fromstring(resp.content)

    items = []
    for item in root.findall(".//item"):
        titulo = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date_raw = item.findtext("pubDate") or ""
        creator = (item.findtext("dc:creator", namespaces=NS) or "").strip()
        cuerpo_html = item.findtext("content:encoded", namespaces=NS) or ""

        try:
            fecha = parsedate_to_datetime(pub_date_raw).astimezone(timezone.utc).strftime("%Y-%m-%d")
        except (TypeError, ValueError):
            fecha = ""

        items.append(
            {
                "id": slug_de_link(link),
                "titulo": titulo,
                "link": link,
                "fecha": fecha,
                "creator": creator,
                "texto": limpiar_html(cuerpo_html),
            }
        )
    return items


def item_backlog_desde_rss(noticia: dict) -> dict:
    from datetime import datetime

    fuente = FUENTE_NOMBRE
    if noticia["creator"] and noticia["creator"].lower() not in ("prensa vicegobernación", "admin"):
        fuente = f"{FUENTE_NOMBRE} ({noticia['creator']})"

    return {
        "id": f"{FUENTE_ID_PREFIJO}-{noticia['id']}",
        "fuente": fuente,
        "titulo": noticia["titulo"],
        "fecha": noticia["fecha"],
        "link": noticia["link"],
        "texto_original": noticia["texto"],
        "imagen_url": "",
        "estado": "pendiente",
        "agregado_el": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "procesado_el": None,
        "wp_edit_url": None,
        "motivo_descarte": None,
    }


def main() -> None:
    print(f"Consultando {FEED_URL} ...")
    try:
        noticias = obtener_noticias()
    except (requests.RequestException, ElementTree.ParseError) as e:
        print(f"No se pudo consultar el feed: {e}")
        sys.exit(1)

    backlog = cargar_backlog()
    ids_existentes = {item.get("id") for item in backlog}

    nuevos = []
    for noticia in noticias:
        item = item_backlog_desde_rss(noticia)
        if item["id"] in ids_existentes:
            continue
        nuevos.append(item)

    if not nuevos:
        print("Sin novedades: el feed ya estaba cargado.")
        return

    backlog.extend(nuevos)
    guardar_backlog(backlog)

    print(f"Agregados {len(nuevos)} item(s) nuevo(s):")
    for item in nuevos:
        print(f"  - [{item['id']}] {item['titulo']}")
    print("\nQuedaron en estado 'pendiente' -- revisalos en admin/index.html.")


if __name__ == "__main__":
    main()
