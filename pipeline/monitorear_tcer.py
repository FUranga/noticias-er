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

Que NO cubre esto (limite conocido, no resuelto): las auditorias
ESPECIALES puntuales (ej. la de comedores comunitarios de Paraná,
2026-09-11 -- ver docs/temas-a-seguir.md) no aparecen en esta pagina bajo
ninguna de las tres categorias de arriba. Si el TCER las publica en algun
otro lugar del sitio, no se encontro en esta pasada -- seguimos
dependiendo de que algun medio la cubra para enterarnos, igual que antes.

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


def main() -> None:
    print(f"Consultando {NOVEDADES_URL} ...")
    try:
        documentos = obtener_documentos()
    except requests.RequestException as e:
        print(f"No se pudo consultar el sitio: {e}")
        sys.exit(1)

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
