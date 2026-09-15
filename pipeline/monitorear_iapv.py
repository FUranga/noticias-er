r"""
Ingesta automatizada del Instituto Autárquico de Planeamiento y Vivienda de
Entre Rios (IAPV): agrega noticias nuevas a la cablera (data/backlog.json)
en estado "pendiente".

No decide nada -- solo carga candidatos para que el editor los triage
despues en admin/index.html. Ver CLAUDE.md: la decision de que es noticia
es siempre humana.

Fuente: sitio a medida (no WordPress, sin RSS ni API -- confirmado
2026-09-15), pero con estructura HTML simple y predecible:
- Listado: https://iapv.gob.ar/seccion/noticias-listado (ultimas ~10
  noticias, cada una con titulo, fecha y link a la nota completa).
- Nota individual: https://iapv.gob.ar/seccion/noticias/{id}/{slug} --
  fecha en `.divCont_Fecha` (DD/MM/AAAA), cuerpo completo en
  `.divCont_ArticuloCuerpo`.

Extraccion con BeautifulSoup sobre HTML crudo (nunca WebFetch/resumen con
modelo secundario -- mismo criterio que el resto del proyecto para
contenido de terceros, ver docs/sitio-fundacion.md).

Uso:
    python monitorear_iapv.py
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from monitorear_gobierno_er import cargar_backlog, cargar_ids_archivados, guardar_backlog  # noqa: E402

BASE_URL = "https://iapv.gob.ar"
LISTADO_URL = f"{BASE_URL}/seccion/noticias-listado"
FUENTE_ID_PREFIJO = "iapv"
FUENTE_NOMBRE = "Instituto Autárquico de Planeamiento y Vivienda de Entre Ríos"

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AgenciaEntrerrianaBot/1.0)"}

PATRON_ID_LINK = re.compile(r"/seccion/noticias/(\d+)/([a-z0-9-]+)")


def fecha_iso(fecha_ddmmaaaa: str) -> str:
    try:
        dd, mm, aaaa = fecha_ddmmaaaa.strip().split("/")
        return f"{aaaa}-{mm.zfill(2)}-{dd.zfill(2)}"
    except (ValueError, AttributeError):
        return ""


def listar_noticias_recientes() -> list[dict]:
    resp = requests.get(LISTADO_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    vistos = set()
    items = []
    for h3 in soup.select("h3"):
        a = h3.find("a", href=PATRON_ID_LINK)
        if not a:
            continue
        match = PATRON_ID_LINK.search(a["href"])
        if not match:
            continue
        noticia_id = match.group(1)
        if noticia_id in vistos:
            continue
        vistos.add(noticia_id)

        titulo = a.get_text(strip=True)
        link = urljoin(BASE_URL, a["href"])
        items.append({"id": noticia_id, "titulo": titulo, "link": link})

    return items


def obtener_detalle(link: str) -> dict:
    resp = requests.get(link, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    fecha_el = soup.select_one(".divCont_Fecha")
    fecha = fecha_iso(fecha_el.get_text(strip=True)) if fecha_el else ""

    cuerpo_el = soup.select_one(".divCont_ArticuloCuerpo")
    texto = cuerpo_el.get_text("\n", strip=True) if cuerpo_el else ""

    return {"fecha": fecha, "texto": texto}


def item_backlog(noticia: dict) -> dict:
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
    print(f"Consultando {LISTADO_URL} ...")
    try:
        noticias = listar_noticias_recientes()
    except requests.RequestException as e:
        print(f"No se pudo consultar el listado: {e}")
        sys.exit(1)

    backlog = cargar_backlog()
    ids_existentes = {item.get("id") for item in backlog} | cargar_ids_archivados()

    nuevos = []
    for noticia in noticias:
        item_id = f"{FUENTE_ID_PREFIJO}-{noticia['id']}"
        if item_id in ids_existentes:
            continue
        try:
            detalle = obtener_detalle(noticia["link"])
        except requests.RequestException as e:
            print(f"  No se pudo bajar la nota {noticia['link']}: {e}")
            continue
        noticia.update(detalle)
        nuevos.append(item_backlog(noticia))

    if not nuevos:
        print("Sin novedades: el listado ya estaba cargado.")
        return

    backlog.extend(nuevos)
    guardar_backlog(backlog)

    print(f"Agregados {len(nuevos)} item(s) nuevo(s):")
    for item in nuevos:
        print(f"  - [{item['id']}] {item['titulo']}")
    print("\nQuedaron en estado 'pendiente' -- revisalos en admin/index.html.")


if __name__ == "__main__":
    main()
