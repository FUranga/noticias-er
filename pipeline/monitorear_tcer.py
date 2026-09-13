r"""
Ingesta automatizada del Tribunal de Cuentas de Entre Rios (TCER): agrega
a la cablera (data/backlog.json) en estado "pendiente" los documentos
nuevos que aparecen en https://tcer.gob.ar/novedades.html -- Memorias
Anuales, Convenios institucionales, e Informes de Auditoria de la Cuenta
General del Ejercicio.

Correccion 2026-09-13 de un diagnostico anterior (ver docs/fuentes.md,
seccion "Organos de control"): se creia que el sitio bloqueaba cualquier
cliente automatizado con 403 (WebFetch daba ese error). Probado con
`requests` simple: **alcanza con mandar un User-Agent de navegador real**
-- no es un desafio de Cloudflare interactivo, solo un filtro de
User-Agent, igual de simple que el resto de los sitios de este proyecto.
No hace falta Playwright ni navegador.

No decide nada -- solo carga candidatos para que el editor los mire
despues. Ver CLAUDE.md: la decision de que es noticia es siempre humana.
Esto es justo el "quick win" que ya senalaba docs/fuentes.md: informes
tecnicos que van a la Legislatura y quedan en la web del organismo sin
gacetilla que los traduzca, casi nunca con cobertura periodistica pese a
ser de alto valor.

Que SI cubre esto: Memorias Anuales, Convenios, e Informes de Auditoria
de la Cuenta General del Ejercicio (el control general y periodico sobre
las cuentas del Estado provincial) -- todos estan listados de forma
estatica en `novedades.html`, con link directo a un PDF.

Que NO cubre esto (limite conocido, PARCIALMENTE resuelto 2026-09-13):
las auditorias ESPECIALES puntuales (ej. la de comedores comunitarios de
Paraná, 2026-09-11 -- ver docs/temas-a-seguir.md) no aparecen en
novedades.html. Si terminan en una Resolucion del TCER, esas SI son
buscables en `https://tcer.gob.ar/scripts/normativa/buscar` (mismo sitio,
pagina normativa.html, sin RSS ni feed cronologico, pero con una API de
busqueda por tipo/anio/palabra clave encontrada inspeccionando la red del
navegador) -- confirmado con un precedente real: una Resolucion de 2021
sobre subsidios a comedores comunitarios de Concordia aparece con la
palabra clave "comedores". PERO ese endpoint sin filtro devuelve **255
resultados solo para 2026** -- la inmensa mayoria son resoluciones
administrativas rutinarias (aprobando/observando una rendicion de
cuentas puntual), el mismo tipo de ruido que ya se filtro para el
Boletin Oficial (ver docs/boletin-oficial-proceso.md). Ingerir todo ese
stream sin filtro re-crearia ese problema a proposito evitado -- no se
hizo. En su lugar, `buscar_comedores_comunitarios()` mas abajo repite
puntualmente la busqueda por la palabra clave del caso que se esta
siguiendo, sin traer el resto del stream. Si en algun momento se decide
seguir la normativa del TCER en general, hace falta antes disenar un
filtro dedicado (mismo espiritu que el del Boletin), no ingerir todo.

Mecanismo: `novedades.html` no tiene una fecha de publicacion propia por
documento (es una pagina de categorias, no un feed cronologico) -- se usa
el header HTTP `Last-Modified` del PDF mismo (real, no inventado) como
fecha del item.

Uso:
    python monitorear_tcer.py
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from monitorear_gobierno_er import cargar_backlog, cargar_ids_archivados, guardar_backlog  # noqa: E402
from monitorear_senado_er import slug_de_link  # noqa: E402

NOVEDADES_URL = "https://tcer.gob.ar/novedades.html"
FUENTE_NOMBRE = "Tribunal de Cuentas de Entre Ríos"
ID_PREFIJO = "tcer"

# User-Agent de navegador real -- ver nota del docstring, es lo unico que
# hacia falta para dejar de recibir 403.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    )
}


def obtener_documentos() -> list[dict]:
    resp = requests.get(NOVEDADES_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    documentos = []
    for a in soup.find_all("a", attrs={"data-bs-target": "#modalVerNovedades"}):
        href = a.get("href")
        titulo = a.get("title") or a.get_text(strip=True)
        if href and titulo:
            documentos.append({"titulo": titulo.strip(), "href": href.strip()})
    return documentos


def categorizar(titulo: str) -> tuple[str, str]:
    """Devuelve (titulo_para_cablera, texto_original) segun el tipo de documento."""
    if titulo.startswith("Memoria Anual"):
        anio = titulo.replace("Memoria Anual", "").strip()
        return (
            f"El Tribunal de Cuentas de Entre Ríos publicó su Memoria Anual {anio}",
            (
                f"Memoria Anual {anio} del Tribunal de Cuentas de Entre Ríos (TCER), remitida "
                "anualmente a la Legislatura según el Artículo 213 de la Constitución Provincial."
            ),
        )
    if "Cuenta General del Ejercicio" in titulo:
        anio = titulo.replace("Cuenta General del Ejercicio", "").strip()
        return (
            f"El Tribunal de Cuentas de Entre Ríos publicó el informe de auditoría de la Cuenta General del Ejercicio {anio}",
            (
                f"Informe de auditoría de la Cuenta General del Ejercicio {anio}, remitido por el "
                "Tribunal de Cuentas de Entre Ríos (TCER) a la Legislatura provincial."
            ),
        )
    # "Convenio" explicito, o el patron "AAAA: <institucion>" que usan los
    # convenios sin la palabra en el titulo (ej. "2021: Universidad
    # Tecnológica Nacional (Facultad Regional Paraná - UTN)").
    if "Convenio" in titulo or re.match(r"^\d{4}:\s", titulo):
        return (
            f"El Tribunal de Cuentas de Entre Ríos publicó un convenio: {titulo}",
            f"Convenio institucional publicado por el Tribunal de Cuentas de Entre Ríos (TCER): {titulo}.",
        )
    return (f"Documento nuevo del Tribunal de Cuentas de Entre Ríos: {titulo}", titulo)


def obtener_fecha_pdf(url: str) -> str:
    """Fecha real (Last-Modified del PDF) o la fecha de hoy si el header no viene."""
    try:
        r = requests.head(url, headers=HEADERS, timeout=20, allow_redirects=True)
        lm = r.headers.get("Last-Modified") or r.headers.get("last-modified")
        if lm:
            dt = datetime.strptime(lm, "%a, %d %b %Y %H:%M:%S %Z")
            return dt.strftime("%Y-%m-%d")
    except (requests.RequestException, ValueError):
        pass
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def item_backlog_desde_documento(doc: dict) -> dict:
    titulo_cablera, texto = categorizar(doc["titulo"])
    fecha = obtener_fecha_pdf(doc["href"])
    slug = slug_de_link(doc["href"]) or re.sub(r"[^a-z0-9]+", "-", doc["titulo"].lower()).strip("-")
    return {
        "id": f"{ID_PREFIJO}-{slug}",
        "fuente": FUENTE_NOMBRE,
        "titulo": titulo_cablera,
        "fecha": fecha,
        "link": doc["href"],
        "texto_original": texto,
        "imagen_url": "",
        "estado": "pendiente",
        "agregado_el": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "procesado_el": None,
        "wp_edit_url": None,
        "motivo_descarte": None,
    }


NORMATIVA_BUSCAR_URL = "https://tcer.gob.ar/scripts/normativa/buscar"

# Busquedas puntuales activas -- cada una es un caso concreto que se esta
# siguiendo (ver docs/temas-a-seguir.md), NO un intento de cubrir toda la
# normativa del TCER (ver nota del docstring sobre el ruido de los 255
# resultados/anio sin filtro). Agregar una entrada aca cuando aparezca un
# caso puntual nuevo que valga la pena vigilar asi; sacarla cuando el caso
# se resuelva o se descarte.
BUSQUEDAS_PUNTUALES = {
    "comedores comunitarios": "Auditoría de comedores comunitarios (ver docs/temas-a-seguir.md, 2026-09-13)",
}


def buscar_normativa(keyword: str) -> list[dict]:
    """Resultados de /scripts/normativa/buscar para una palabra clave puntual.

    Endpoint encontrado inspeccionando la pestaña de red del navegador al
    usar el buscador de normativa.html (no documentado, no tiene RSS/API
    formal) -- devuelve HTML con una tabla, no JSON.
    """
    resp = requests.get(
        NORMATIVA_BUSCAR_URL,
        params={"normativaTipo": "", "normativaAnio": "", "normativaKeyword": keyword},
        headers=HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    resultados = []
    for row in soup.select("tbody tr"):
        celdas = row.find_all("td")
        if len(celdas) < 4:
            continue
        tipo = celdas[0].get_text(strip=True)
        numero = celdas[1].get_text(strip=True)
        anio = celdas[2].get_text(strip=True)
        link_tag = celdas[3].find("a", href=True)
        if not link_tag:
            continue
        href = link_tag["href"]
        # El sitio tiene un bug conocido (2026-09-13) que a veces deja
        # "Tipo"/"Numero"/"Año" en 0 y filtra un warning de PHP dentro del
        # data-title -- se ignoran esos resultados rotos en vez de cargar
        # basura a la cablera (ver PDFs de ejemplo, dieron 404/HTML en vez
        # de PDF real).
        if tipo in ("0", "") or numero == "0":
            continue
        resultados.append({
            "titulo": f"{tipo} N° {numero}/{anio}".strip(),
            "href": href,
        })
    return resultados


def main() -> None:
    print(f"Consultando {NOVEDADES_URL} ...")
    try:
        documentos = obtener_documentos()
    except requests.RequestException as e:
        print(f"No se pudo consultar el sitio: {e}")
        sys.exit(1)

    for keyword, motivo in BUSQUEDAS_PUNTUALES.items():
        print(f"Buscando normativa por '{keyword}' ({motivo}) ...")
        try:
            for r in buscar_normativa(keyword):
                r["titulo"] = f"{r['titulo']} — {motivo}"
                documentos.append(r)
        except requests.RequestException as e:
            print(f"  No se pudo buscar '{keyword}': {e}")

    if not documentos:
        print("No se encontro ningun documento en la pagina -- revisar si cambio la estructura del sitio.")
        return

    backlog = cargar_backlog()
    ids_existentes = {item.get("id") for item in backlog} | cargar_ids_archivados()

    nuevos = []
    for doc in documentos:
        item = item_backlog_desde_documento(doc)
        if item["id"] in ids_existentes:
            continue
        ids_existentes.add(item["id"])
        nuevos.append(item)

    if not nuevos:
        print("Sin novedades: todos los documentos ya estaban cargados.")
        return

    backlog.extend(nuevos)
    guardar_backlog(backlog)

    print(f"Agregados {len(nuevos)} item(s) nuevo(s):")
    for item in nuevos:
        print(f"  - [{item['id']}] {item['titulo']} ({item['fecha']})")
    print("\nQuedaron en estado 'pendiente' -- revisalos en admin/index.html.")


if __name__ == "__main__":
    main()
