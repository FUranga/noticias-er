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

Parseo con `feedparser` (no `xml.etree`, ver incidente 2026-09-07): un feed
de WordPress alimentado por gacetillas de prensa pegadas desde Word/Google
Docs puede traer HTML mal formado dentro de `content:encoded` (una etiqueta
sin cerrar, una entidad suelta) que rompe un parser XML estricto -- fallo
real en produccion: `mismatched tag` en pleno cron de GitHub Actions.
`feedparser` esta hecho justamente para tolerar feeds del mundo real que no
son XML perfecto, y expone los mismos campos (`title`, `link`, `published`,
`author`, `content`) sin tener que lidiar con namespaces a mano.

Uso:
    python monitorear_senado_er.py
"""

import html
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import feedparser
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from monitorear_gobierno_er import cargar_backlog, guardar_backlog  # noqa: E402

FEED_URL = "https://www.senadoer.gob.ar/feed/"
FUENTE_ID_PREFIJO = "senadoer"
FUENTE_NOMBRE = "Cámara de Senadores de Entre Ríos"


def limpiar_html(texto_html: str | None) -> str:
    if not texto_html:
        return ""
    sin_tags = re.sub(r"<[^>]+>", "\n", texto_html)
    return html.unescape(re.sub(r"\n{3,}", "\n\n", sin_tags)).strip()


def slug_de_link(link: str) -> str:
    return link.rstrip("/").rsplit("/", 1)[-1]


def obtener_noticias(feed_url: str = FEED_URL) -> list[dict]:
    parsed = feedparser.parse(feed_url, agent="Mozilla/5.0")
    if parsed.bozo and not parsed.entries:
        # "bozo" solo marca que el feed no era XML perfecto -- feedparser ya
        # lo tolera (ver docstring del modulo). Solo es un error real si
        # ademas no se pudo sacar ninguna entrada.
        raise RuntimeError(f"Feed invalido y sin entradas: {parsed.get('bozo_exception')}")

    items = []
    for entry in parsed.entries:
        titulo = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
        creator = (entry.get("author") or "").strip()
        contenido = entry.get("content")
        cuerpo_html = contenido[0].get("value") if contenido else entry.get("summary") or ""

        try:
            fecha = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).strftime("%Y-%m-%d")
        except (TypeError, AttributeError):
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
    except (requests.RequestException, RuntimeError) as e:
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
