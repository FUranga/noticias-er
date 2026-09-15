r"""
Ingesta automatizada del Consejo General de Educacion de Entre Rios (CGE):
agrega noticias nuevas a la cablera (data/backlog.json) en estado
"pendiente" o "descartado" (ver filtro abajo).

No decide nada -- solo carga candidatos para que el editor los triage
despues en admin/index.html. Ver CLAUDE.md: la decision de que es noticia
es siempre humana.

Fuente: RSS estandar de WordPress (`https://cge.entrerios.gov.ar/feed/`),
publico, sin autenticacion, con texto completo via content:encoded --
confirmado 200 OK (2026-09-15).

Filtro de ruido (a diferencia de pipeline/monitorear_stj.py): el feed del
CGE es muy activo pero dominado por gestion rutinaria de cargos docentes
(concursos, interinatos, suplencias) -- ver pipeline/filtro_contenido_cge.py
para el detalle de por que hace falta este filtro (mismo criterio que el
filtro de la fuente "empresa", nunca oculta del todo, solo auto-descarta
con motivo).

Cuidado, mismo caso que pipeline/monitorear_epre.py: el feed NO se limita a
los ultimos 10 items por default de WordPress -- devolvio 500 items en la
primera corrida (2026-09-15). Por eso se recorta a MAX_ITEMS antes de
comparar contra el backlog, para que un corte largo sin corridas no vuelque
cientos de items viejos de una sola vez.

Uso:
    python monitorear_cge.py
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from feed_utils import parsear_feed_con_reintentos  # noqa: E402
from filtro_contenido_cge import clasificar_no_editorial  # noqa: E402
from monitorear_gobierno_er import cargar_backlog, cargar_ids_archivados, guardar_backlog  # noqa: E402
from monitorear_senado_er import limpiar_html, slug_de_link  # noqa: E402

FEED_URL = "https://cge.entrerios.gov.ar/feed/"
FUENTE_ID_PREFIJO = "cge"
FUENTE_NOMBRE = "Consejo General de Educación de Entre Ríos"
MAX_ITEMS = 40


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
    motivo = clasificar_no_editorial(noticia["titulo"], noticia["texto"])
    return {
        "id": f"{FUENTE_ID_PREFIJO}-{noticia['id']}",
        "fuente": FUENTE_NOMBRE,
        "titulo": noticia["titulo"],
        "fecha": noticia["fecha"],
        "link": noticia["link"],
        "texto_original": noticia["texto"],
        "imagen_url": "",
        "estado": "descartado" if motivo else "pendiente",
        "agregado_el": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "procesado_el": None,
        "wp_edit_url": None,
        "motivo_descarte": motivo,
    }


def main() -> None:
    print(f"Consultando {FEED_URL} ...")
    try:
        noticias = obtener_noticias()[:MAX_ITEMS]
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

    pendientes = [item for item in nuevos if item["estado"] == "pendiente"]
    descartados = [item for item in nuevos if item["estado"] == "descartado"]

    print(f"Agregados {len(nuevos)} item(s) nuevo(s):")
    for item in nuevos:
        marca = " [auto-descartado: gestión de cargos]" if item["estado"] == "descartado" else ""
        print(f"  - [{item['id']}] {item['titulo']}{marca}")
    print(f"\n{len(pendientes)} quedaron en 'pendiente' -- revisalos en admin/index.html.")
    if descartados:
        print(f"{len(descartados)} se descartaron automáticamente (ver pipeline/filtro_contenido_cge.py).")


if __name__ == "__main__":
    main()
