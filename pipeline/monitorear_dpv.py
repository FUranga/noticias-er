r"""
Ingesta automatizada de la Direccion Provincial de Vialidad de Entre Rios
(DPV): agrega noticias nuevas a la cablera (data/backlog.json) en estado
"pendiente".

No decide nada -- solo carga candidatos para que el editor los triage
despues en admin/index.html. Ver CLAUDE.md: la decision de que es noticia
es siempre humana.

Fuente: RSS estandar de WordPress (`https://dpver.gov.ar/feed/`), publico,
sin autenticacion, con texto completo via content:encoded -- confirmado
200 OK aunque el link no aparece expuesto en el HTML del sitio (mismo
patron que pipeline/monitorear_stj.py, ver docs/fuentes.md).

Por que sumar esta fuente (2026-09-15, pedido de Francisco): la DPV es
exactamente el tipo de organismo que conviene monitorear de forma
sistematica -- gasto real en obra vial, licitaciones y contrataciones
propias -- en vez de encontrar sus resoluciones sueltas y sin contexto
dentro del Boletin Oficial (ver docs/temas-a-seguir.md, entrada sobre
obra publica paralizada del 2026-09-15).

Uso:
    python monitorear_dpv.py
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from feed_utils import parsear_feed_con_reintentos  # noqa: E402
from monitorear_gobierno_er import cargar_backlog, cargar_ids_archivados, guardar_backlog  # noqa: E402
from monitorear_senado_er import limpiar_html, slug_de_link  # noqa: E402

FEED_URL = "https://dpver.gov.ar/feed/"
FUENTE_ID_PREFIJO = "dpver"
FUENTE_NOMBRE = "Dirección Provincial de Vialidad de Entre Ríos"


def obtener_noticias(feed_url: str = FEED_URL) -> list[dict]:
    parsed = parsear_feed_con_reintentos(feed_url)

    items = []
    for entry in parsed.entries:
        titulo = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
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
                "texto": limpiar_html(cuerpo_html),
            }
        )
    return items


def item_backlog_desde_rss(noticia: dict) -> dict:
    return {
        "id": f"{FUENTE_ID_PREFIJO}-{noticia['id']}",
        "fuente": FUENTE_NOMBRE,
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
    ids_existentes = {item.get("id") for item in backlog} | cargar_ids_archivados()

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
