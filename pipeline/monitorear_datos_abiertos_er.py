r"""
Ingesta automatizada del Portal de Datos Abiertos de Entre Rios: agrega
datasets nuevos o actualizados a la cablera (data/backlog.json) en estado
"pendiente".

No decide nada -- solo carga candidatos para que el editor los triage
despues en admin/index.html. Ver CLAUDE.md: la decision de que es noticia
es siempre humana.

Distinto de los demas monitores: acá no hay "noticia" en el sentido
tradicional, sino un dataset publicado o actualizado -- la novedad es que
el Estado hizo publico (o cambio) un conjunto de datos, no un anuncio en
prosa. El titulo del item queda como "Dataset publicado/actualizado:
<titulo>" para que quede claro en la cablera que es material de otra
naturaleza (ver nota de CLAUDE.md sobre que lo judicial/regulatorio
necesita tratamiento distinto -- esto aplica el mismo criterio a datasets).

Fuente: API CKAN estandar, publica, sin autenticacion (confirmada
2026-09-06, ver docs/fuentes.md seccion "Organos de control..."):
    https://datos.entrerios.gov.ar/api/3/action/package_search
ordenada por `metadata_modified desc` -- devuelve tanto datasets nuevos
como actualizaciones de datasets existentes (no se distingue explicitamente
entre "nuevo" y "actualizado" en esta primera version; ambos casos entran
igual, el editor los distingue leyendo fechas si hace falta).

Uso:
    python monitorear_datos_abiertos_er.py
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from monitorear_gobierno_er import cargar_backlog, cargar_ids_archivados, guardar_backlog  # noqa: E402

API_URL = "https://datos.entrerios.gov.ar/api/3/action/package_search"
FUENTE_NOMBRE = "Portal de Datos Abiertos de Entre Ríos"
ID_PREFIJO = "datosabiertoser"

# Cuantos de los mas recientemente modificados revisar en cada corrida.
# El portal tiene ~180 datasets en total; no hace falta traerlos todos
# cada vez, alcanza con mirar los N mas recientes y dejar que la
# deduplicacion por id haga el resto.
CANTIDAD_A_REVISAR = 20


def obtener_datasets() -> list[dict]:
    resp = requests.get(
        API_URL,
        params={"sort": "metadata_modified desc", "rows": CANTIDAD_A_REVISAR},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"La API de CKAN respondio success=false: {data}")
    return data["result"]["results"]


def item_backlog_desde_dataset(dataset: dict) -> dict:
    slug = dataset.get("name") or dataset["id"]
    modificado = (dataset.get("metadata_modified") or "")[:10]
    creado = (dataset.get("metadata_created") or "")[:10]
    es_nuevo = modificado == creado

    organizacion = (dataset.get("organization") or {}).get("title", "")
    titulo_base = dataset.get("title") or slug
    prefijo_titulo = "Dataset publicado" if es_nuevo else "Dataset actualizado"

    partes_texto = []
    if dataset.get("notas") or dataset.get("notes"):
        partes_texto.append(dataset.get("notas") or dataset.get("notes"))
    if organizacion:
        partes_texto.append(f"Organización responsable: {organizacion}.")
    cantidad_recursos = len(dataset.get("resources") or [])
    if cantidad_recursos:
        partes_texto.append(f"Incluye {cantidad_recursos} recurso(s) descargable(s).")

    return {
        "id": f"{ID_PREFIJO}-{slug}-{modificado}",
        "fuente": FUENTE_NOMBRE,
        "titulo": f"{prefijo_titulo}: {titulo_base}",
        "fecha": modificado or creado,
        "link": f"https://datos.entrerios.gov.ar/dataset/{slug}",
        "texto_original": "\n\n".join(partes_texto),
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
        datasets = obtener_datasets()
    except (requests.RequestException, RuntimeError) as e:
        print(f"No se pudo consultar la API: {e}")
        sys.exit(1)

    backlog = cargar_backlog()
    ids_existentes = {item.get("id") for item in backlog} | cargar_ids_archivados()

    nuevos = []
    for dataset in datasets:
        item = item_backlog_desde_dataset(dataset)
        if item["id"] in ids_existentes:
            continue
        nuevos.append(item)

    if not nuevos:
        print("Sin novedades: los datasets mas recientes ya estaban cargados.")
        return

    backlog.extend(nuevos)
    guardar_backlog(backlog)

    print(f"Agregados {len(nuevos)} item(s) nuevo(s):")
    for item in nuevos:
        print(f"  - [{item['id']}] {item['titulo']}")
    print("\nQuedaron en estado 'pendiente' -- revisalos en admin/index.html.")


if __name__ == "__main__":
    main()
