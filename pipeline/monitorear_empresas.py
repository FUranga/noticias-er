r"""
Ingesta automatizada de comunicados propios de camaras empresarias y
empresas entrerrianas: agrega novedades nuevas a la cablera
(data/backlog.json) en estado "pendiente", bajo la macro-pestana
"Empresas" de admin/index.html (filtra por el prefijo "empresa-" del id).

Distinto del agregador "Medios" (pipeline/monitorear_medios.py): estas NO
son coberturas de otro medio sobre un hecho -- son comunicados propios de
la fuente (una camara o una empresa hablando de si misma), mismo tipo de
material que un comunicado de gobierno. Por eso no se filtra por
topico+lugar (ver docs/fuentes.md, seccion "Organizaciones
privadas/empresarias" -- casi todo lo que publican es relevante por
definicion, es su propio comunicado) y usan los mismos 4 estados que el
resto de la cablera (pendiente/a_publicar/a_investigar/descartado), no los
estados especiales de "Medios" (referido, etc.).

No decide nada -- solo carga candidatos para que el editor los triage
despues. Ver CLAUDE.md: la decision de que es noticia es siempre humana, y
un comunicado de una camara/empresa tiene el mismo sesgo estructural que
uno de gobierno (esta escrito para hacer quedar bien a quien lo emite) --
aplica la misma regla de atribucion de docs/estilo-editorial.md.

Dos fuentes de datos:
- data/fuentes_camaras.json: las 6 camaras empresarias con RSS confirmado
  (UIER, CEER, Centro Comercial de Parana, FEDER, Bolsa de Cereales ER,
  CAMARCO ER).
- data/organismos_empresas.json: filtra las que tienen "rss" no nulo
  (67 al 2026-09-08) -- ver docs/fuentes.md para el detalle de como se
  armo esa lista y su verificacion de RSS.

Uso:
    python monitorear_empresas.py
"""

import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from feed_utils import parsear_feed_con_reintentos  # noqa: E402
from filtro_contenido_empresas import clasificar_no_editorial  # noqa: E402
from monitorear_gobierno_er import cargar_backlog, guardar_backlog, limpiar_html  # noqa: E402
from monitorear_senado_er import slug_de_link  # noqa: E402

CAMARAS_PATH = Path(__file__).resolve().parent.parent / "data" / "fuentes_camaras.json"
EMPRESAS_PATH = Path(__file__).resolve().parent.parent / "data" / "organismos_empresas.json"

ID_PREFIJO = "empresa"


def slugificar(nombre: str) -> str:
    sin_acentos = unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", sin_acentos.lower()).strip("-")


def cargar_fuentes() -> list[dict]:
    with open(CAMARAS_PATH, encoding="utf-8") as f:
        camaras = json.load(f)
    fuentes = [{"id": c["id"], "nombre": c["nombre"], "rss": c["rss"], "es_camara": True} for c in camaras]

    with open(EMPRESAS_PATH, encoding="utf-8") as f:
        empresas = json.load(f)
    for e in empresas:
        if e.get("rss"):
            fuentes.append(
                {"id": slugificar(e["nombre"]), "nombre": e["nombre"], "rss": e["rss"], "es_camara": False}
            )

    return fuentes


def obtener_items(fuente: dict) -> list[dict]:
    parsed = parsear_feed_con_reintentos(fuente["rss"])

    items = []
    for entry in parsed.entries:
        titulo = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
        if not titulo or not link:
            continue
        contenido = entry.get("content")
        cuerpo_html = contenido[0].get("value") if contenido else entry.get("summary") or ""

        try:
            fecha = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).strftime("%Y-%m-%d")
        except (TypeError, AttributeError):
            fecha = ""

        items.append(
            {
                "id": f"{ID_PREFIJO}-{fuente['id']}-{slug_de_link(link)}",
                "fuente": fuente["nombre"],
                "titulo": titulo,
                "fecha": fecha,
                "link": link,
                "texto": limpiar_html(cuerpo_html),
                "es_camara": fuente["es_camara"],
            }
        )
    return items


def item_backlog(item: dict) -> dict:
    motivo = clasificar_no_editorial(item["titulo"], item["texto"], item["link"], es_camara=item["es_camara"])
    return {
        "id": item["id"],
        "fuente": item["fuente"],
        "titulo": item["titulo"],
        "fecha": item["fecha"],
        "link": item["link"],
        "texto_original": item["texto"],
        "imagen_url": "",
        "estado": "descartado" if motivo else "pendiente",
        "agregado_el": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "procesado_el": None,
        "wp_edit_url": None,
        "motivo_descarte": motivo,
    }


def main() -> None:
    fuentes = cargar_fuentes()
    backlog = cargar_backlog()
    ids_existentes = {item.get("id") for item in backlog}
    nuevos = []
    fallidas = []

    for fuente in fuentes:
        print(f"Consultando {fuente['nombre']} ({fuente['rss']}) ...")
        try:
            items = obtener_items(fuente)
        except Exception as e:  # noqa: BLE001 -- una fuente caida/rara no debe tirar abajo todo el lote
            print(f"  No se pudo consultar: {e}")
            fallidas.append(fuente["nombre"])
            continue

        for item in items:
            if item["id"] in ids_existentes:
                continue
            ids_existentes.add(item["id"])
            nuevos.append(item_backlog(item))

    if nuevos:
        backlog.extend(nuevos)
        guardar_backlog(backlog)

    if not nuevos and not fallidas:
        print("\nSin novedades: todo lo consultado ya estaba cargado.")
        return

    if nuevos:
        pendientes = [item for item in nuevos if item["estado"] == "pendiente"]
        descartados = [item for item in nuevos if item["estado"] == "descartado"]
        print(f"\nAgregados {len(nuevos)} item(s) nuevo(s) (macro-pestaña 'Empresas'):")
        for item in nuevos:
            marca = " [auto-descartado]" if item["estado"] == "descartado" else ""
            print(f"  - [{item['id']}] {item['fuente']}: {item['titulo']}{marca}")
        print(f"\n{len(pendientes)} quedaron en 'pendiente' -- revisalos en admin/index.html.")
        if descartados:
            print(
                f"{len(descartados)} se descartaron automaticamente (filtro de contenido no editorial "
                "-- ver pipeline/filtro_contenido_empresas.py): recetas, avisos laborales o fichas de "
                "producto/servicio sin hecho noticioso."
            )

    if fallidas:
        print(f"\nFuentes que fallaron esta corrida ({len(fallidas)}): {', '.join(fallidas)}")


if __name__ == "__main__":
    main()
