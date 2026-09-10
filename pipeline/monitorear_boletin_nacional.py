r"""
Ingesta automatizada del Boletin Oficial de la Republica Argentina (BORA),
filtrada a lo que menciona a Entre Rios o a organismos nacionales/binacionales
con impacto directo en la provincia (hoy: "Salto Grande", que cubre tanto a
la Comision Tecnica Mixta de Salto Grande como al complejo hidroelectrico en
general). Agrega candidatos a la cablera (data/backlog.json) en estado
"pendiente" -- ver CLAUDE.md: la decision de que es noticia es siempre humana.

Distinto del filtro del Boletin de Entre Rios (pipeline/monitorear_boletin_er.py,
ver docs/boletin-oficial-proceso.md): ese es un filtro de EXCLUSION (deja pasar
casi todo, saca lo estructuralmente administrativo). Este es un filtro de
INCLUSION: el Boletin nacional es demasiado grande para cargarlo entero (la
Seccion 1 sola tiene ediciones de cientos de normas por dia, la enorme mayoria
sin ninguna relacion con Entre Rios) -- solo entra lo que menciona
explicitamente alguna de las KEYWORDS.

Mecanismo (reversado 2026-09-07 con el navegador, no documentado publicamente):
el buscador de https://www.boletinoficial.gob.ar/busquedaAvanzada/all no expone
parametros GET ni un feed -- el formulario dispara un POST a
`/busquedaAvanzada/realizarBusqueda` con un body `application/x-www-form-urlencoded`
de un solo campo, `params`, que es un JSON serializado (ver `_body_busqueda`
abajo para el shape completo). La respuesta es JSON con `content.html`: un
fragmento HTML ya renderizado con los resultados (no una lista de objetos
estructurados) -- hay que parsearlo con BeautifulSoup, no leerlo como datos
limpios. Cada resultado es un <div class="linea-aviso">; el link a la norma
completa esta en el <a href="/detalleAviso/<seccion>/<id>/<AAAAMMDD>"> que lo
envuelve (no adentro del propio linea-aviso).

Importante -- la busqueda del sitio hace AND de palabras sueltas, no de frase
exacta (probado: `texto: "Entre Ríos"` con comillas no acota a la frase, sigue
siendo "entre" Y "rios" en cualquier parte de la norma). Sin acotar por fecha
esto devuelve decenas de miles de resultados sobre 133 anios de archivo -- por
eso este script SIEMPRE manda fechaDesde/fechaHasta (ventana de LOOKBACK_DIAS)
y nunca corre la busqueda "abierta". Con la ventana acotada el volumen real es
bajo (~2-3 avisos/dia mencionando "Entre Rios" en Seccion 1+3, verificado
2026-09-07 sobre 5 semanas de archivo) -- manejable para revisar a mano.

El texto que trae el fragmento de busqueda es un RESUMEN/extracto (no el texto
completo de la norma) -- a diferencia de Senado ER o EPRE, `texto_original` acá
va a quedar corto. Es exactamente el mismo caso que "el texto parece incompleto"
que ya contempla `skills/procesar-cablera/SKILL.md` (usar WebFetch sobre `link`
para completar antes de redactar) -- no hace falta logica especial.

Uso:
    python monitorear_boletin_nacional.py
"""

import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from monitorear_gobierno_er import cargar_backlog, cargar_ids_archivados, guardar_backlog  # noqa: E402

BUSQUEDA_URL = "https://www.boletinoficial.gob.ar/busquedaAvanzada/realizarBusqueda"
FUENTE_NOMBRE = "Boletín Oficial de la República Argentina"
FUENTE_ID_PREFIJO = "boletinnac"

# Cada keyword se busca por separado (la busqueda del sitio es AND de palabras
# sueltas dentro de una misma consulta, no OR entre conceptos distintos).
KEYWORDS = ["Entre Ríos", "Salto Grande"]

# Seccion 1 = Legislacion y Avisos Oficiales (leyes/decretos/resoluciones),
# Seccion 3 = Contrataciones (licitaciones). Se excluye la Seccion 2
# (Sociedades y Avisos Judiciales) -- mismo criterio que el Boletin de ER:
# edictos judiciales y avisos societarios individuales practicamente nunca
# son noticia, y son la categoria de mayor volumen/ruido.
SECCIONES = [1, 3]
SECCION_SLUG = {1: "primera", 2: "segunda", 3: "tercera"}

LOOKBACK_DIAS = 4  # margen para no perder nada si una corrida se salteo un dia


def _body_busqueda(texto: str, fecha_desde: str, fecha_hasta: str, seccion: list[int]) -> dict:
    return {
        "busquedaRubro": False,
        "hayMasResultadosBusqueda": True,
        "ejecutandoLlamadaAsincronicaBusqueda": False,
        "ultimaSeccion": "",
        "filtroPorRubrosSeccion": False,
        "filtroPorRubroBusqueda": False,
        "filtroPorSeccionBusqueda": True,
        "busquedaOriginal": True,
        "ordenamientoSegunda": False,
        "seccionesOriginales": seccion,
        "ultimoItemExterno": None,
        "ultimoItemInterno": None,
        "texto": texto,
        "rubros": [],
        "nroNorma": "",
        "anioNorma": "",
        "denominacion": "",
        "tipoContratacion": "",
        "anioContratacion": "",
        "nroContratacion": "",
        "fechaDesde": fecha_desde,
        "fechaHasta": fecha_hasta,
        "todasLasPalabras": True,
        "comienzaDenominacion": False,
        "seccion": seccion,
        "tipoBusqueda": "Avanzada",
        "numeroPagina": 1,
        "ultimoRubro": "",
    }


def buscar(texto: str, fecha_desde: str, fecha_hasta: str, seccion: list[int]) -> str:
    resp = requests.post(
        BUSQUEDA_URL,
        data={"params": json.dumps(_body_busqueda(texto, fecha_desde, fecha_hasta, seccion))},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("error"):
        raise RuntimeError(f"El buscador respondio con error: {data.get('mensajes')}")
    return data["content"]["html"]


def parsear_resultados(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for bloque in soup.select(".linea-aviso"):
        enlace = bloque.find_parent("a", href=re.compile(r"/detalleAviso/"))
        if not enlace:
            continue
        m = re.search(r"/detalleAviso/(\w+)/(\d+)/(\d{8})", enlace["href"])
        if not m:
            continue
        seccion_slug, aviso_id, fecha_raw = m.groups()
        fecha = f"{fecha_raw[0:4]}-{fecha_raw[4:6]}-{fecha_raw[6:8]}"
        texto = re.sub(r"\s+", " ", bloque.get_text(" ", strip=True)).strip()
        items.append(
            {
                "id": aviso_id,
                "fecha": fecha,
                "link": f"https://www.boletinoficial.gob.ar/detalleAviso/{seccion_slug}/{aviso_id}/{fecha_raw}",
                "texto": texto,
            }
        )
    return items


def item_backlog(aviso: dict) -> dict:
    # El texto trae "ORGANISMO Resolución N/AÑO Fecha de Publicacion: ... <extracto>"
    # -- se usa como titulo el primer tramo (antes de la fecha), y el resto queda
    # en texto_original como contexto/extracto (no es el texto completo, ver
    # docstring del modulo).
    texto = aviso["texto"]
    partes = re.split(r"Fecha de Publicacion:\s*\d{2}/\d{2}/\d{4}", texto, maxsplit=1)
    titulo = partes[0].strip()[:200] or texto[:200]
    return {
        "id": f"{FUENTE_ID_PREFIJO}-{aviso['id']}",
        "fuente": FUENTE_NOMBRE,
        "titulo": titulo,
        "fecha": aviso["fecha"],
        "link": aviso["link"],
        "texto_original": texto,
        "imagen_url": "",
        "estado": "pendiente",
        "agregado_el": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "procesado_el": None,
        "wp_edit_url": None,
        "motivo_descarte": None,
    }


def main() -> None:
    hoy = datetime.now(timezone.utc).date()
    fecha_desde = (hoy - timedelta(days=LOOKBACK_DIAS)).strftime("%d/%m/%Y")
    fecha_hasta = hoy.strftime("%d/%m/%Y")

    encontrados: dict[str, dict] = {}
    for keyword in KEYWORDS:
        for seccion in SECCIONES:
            print(f"Consultando BORA: \"{keyword}\" en Sección {seccion} ({fecha_desde} a {fecha_hasta}) ...")
            try:
                html = buscar(keyword, fecha_desde, fecha_hasta, [seccion])
            except (requests.RequestException, RuntimeError, KeyError) as e:
                print(f"  Fallo la consulta ({keyword}, sección {seccion}): {e}")
                continue
            for aviso in parsear_resultados(html):
                encontrados[aviso["id"]] = aviso

    backlog = cargar_backlog()
    ids_existentes = {item.get("id") for item in backlog} | cargar_ids_archivados()

    nuevos = []
    for aviso in encontrados.values():
        item = item_backlog(aviso)
        if item["id"] in ids_existentes:
            continue
        nuevos.append(item)

    if not nuevos:
        print("Sin novedades en la ventana consultada.")
        return

    backlog.extend(nuevos)
    guardar_backlog(backlog)

    print(f"Agregados {len(nuevos)} item(s) nuevo(s):")
    for item in nuevos:
        print(f"  - [{item['id']}] {item['titulo']}")
    print("\nQuedaron en estado 'pendiente' -- revisalos en admin/index.html.")


if __name__ == "__main__":
    main()
