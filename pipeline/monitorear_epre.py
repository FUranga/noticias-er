r"""
Ingesta automatizada del EPRE (Ente Provincial Regulador de la Energia de
Entre Rios): agrega noticias nuevas a la cablera (data/backlog.json) en
estado "pendiente".

No decide nada -- solo carga candidatos para que el editor los triage
despues en admin/index.html. Ver CLAUDE.md: la decision de que es noticia
es siempre humana.

Fuente: RSS estandar de WordPress (`https://epre.gov.ar/web/feed/`), publico,
sin autenticacion, con texto completo via content:encoded -- mismo mecanismo
que pipeline/monitorear_senado_er.py (confirmado 2026-09-07: mismo generador
WordPress, mismas namespaces RSS). El EPRE publica resoluciones (incluido el
cuadro tarifario mensual) y convocatorias a audiencia publica bajo las
categorias "Resoluciones", "Tarifa Electrica" y "Noticias" -- volumen bajo
(unas pocas entradas por mes), no hace falta ningun filtro mecanico como el
del Boletin Oficial (ver docs/boletin-oficial-proceso.md).

Cuidado -- distinto de Senado ER: el feed de EPRE NO se limita a los 10 items
por default de WordPress, devuelve el historico completo (500 items
confirmado 2026-09-07, resoluciones desde 2013). Por eso este script recorta
a los ultimos MAX_ITEMS antes de comparar contra el backlog -- si no,
la primera corrida (o cualquier corrida despues de un corte largo) volcaria
cientos de resoluciones viejas a "pendiente" de una sola vez, exactamente el
problema de volumen que se evito con el Boletin Oficial (ver
docs/boletin-oficial-proceso.md). Con el ritmo real del organismo (unas pocas
entradas por mes) y corriendo cada 15 min, MAX_ITEMS=20 tiene margen de sobra.

Uso:
    python monitorear_epre.py
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from monitorear_gobierno_er import cargar_backlog, cargar_ids_archivados, guardar_backlog  # noqa: E402
from monitorear_senado_er import obtener_noticias  # noqa: E402

FEED_URL = "https://epre.gov.ar/web/feed/"
FUENTE_ID_PREFIJO = "epre"
FUENTE_NOMBRE = "Ente Provincial Regulador de la Energía de Entre Ríos"
MAX_ITEMS = 20


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
        noticias = obtener_noticias(FEED_URL)[:MAX_ITEMS]
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
