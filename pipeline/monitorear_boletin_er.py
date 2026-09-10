r"""
Ingesta automatizada del Boletin Oficial de Entre Rios: agrega a la cablera
(data/backlog.json) las normas de cada edicion nueva que sobreviven un
filtro mecanico de volumen. Ver docs/boletin-oficial-proceso.md para el
diseno completo (por que hace falta un filtro, que se filtra y por que,
que sigue faltando) y docs/fuentes.md (seccion "Organos de control...")
para como se encontraron las URLs de origen.

Por que este script es distinto de monitorear_gobierno_er.py y
monitorear_senado_er.py (que cargan TODO sin filtrar): una edicion tiene
~100 paginas y decenas de items, y la gran mayoria son registros
administrativos estructuralmente casi nunca noticiables (rechazos de
recursos individuales, avisos legales personales). Cargar todo ahogaria
la cablera. El filtro es mecanico (por patron de titulo/categoria), NUNCA
editorial -- no decide que ES noticia, solo que tipo de registro no llega
a tener la oportunidad de serlo. Nada se pierde en silencio: todo lo
filtrado (y un resumen de lo que ni se intento parsear en detalle) queda
en data/log_filtro_boletin.jsonl.

Alcance de esta version (2026-09, ver docs/boletin-oficial-proceso.md,
"Fuera de alcance"): parsea en detalle toda la Seccion Administrativa
(Leyes, Decretos, Resoluciones) y, de la Seccion Comercial, solo
Licitaciones. El resto de la Seccion Comercial (edictos judiciales,
personas juridicas, y las demas subcategorias de organismos publicos)
se descarta en bloque por categoria, sin parseo item por item.

Cada item que sobrevive se carga con "estado": "pendiente", igual que
las demas fuentes -- no decide ni publica nada, el editor lo triagea
despues (ver CLAUDE.md).

Uso:
    python monitorear_boletin_er.py

Requiere `pypdf` ademas de `requests` (ver requirements.txt).
"""

import io
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).resolve().parent))
from monitorear_gobierno_er import cargar_backlog, cargar_ids_archivados, guardar_backlog  # noqa: E402

INDICE_URL = "https://testing54.entrerios.gov.ar/boletin/factura/inicio/get_buscador"
PDF_URL_TPL = "https://www.entrerios.gov.ar/boletin/calendario/Boletin/{anio}/{mes}/{dd_mm_aa}.pdf"
FUENTE_ID_PREFIJO = "boletiner"
FUENTE_NOMBRE = "Boletín Oficial de Entre Ríos"

LOG_PATH = Path(__file__).resolve().parent.parent / "data" / "log_filtro_boletin.jsonl"

MESES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}

CATEGORIAS_ADMIN = {"LEYES", "DECRETOS", "RESOLUCIONES", "ACORDADAS", "DISPOSICIONES"}
CODIGO_RE = re.compile(
    r"^(LEY N[°ºª]\s*\d+"
    r"|DTO[- ]\d{4}[-\s].+"
    r"|DECRETO N[°ºª]?\s*\d+.*"
    r"|RESOLUCI[OÓ]N N[°ºª]?\s*\S+.*"
    r"|ACORDADA N[°ºª]?\s*\S+.*"
    r"|DISPOSICI[OÓ]N N[°ºª]?\s*\S+.*)$"
)

# Filtro mecanico de decretos: solo lo que estructuralmente confirma una
# decision ya tomada contra una persona, sin revelar un hecho nuevo. Ver
# docs/boletin-oficial-proceso.md para el resto de los patrones evaluados
# y por que NO se filtran (reconocimiento de pago, recupero de haberes,
# renuncias, pases a retiro -- los montos/cargos varian, quedan todos).
# Sobre titulo sin espacios (ver _sin_espacios): mismo motivo que las
# palabras de prioridad de mas abajo.
RECHAZO_INDIVIDUAL_RE = re.compile(r"^RECHAZO(RECURSO|RECLAMO|SOLICITUD)INTERPUESTO")

# Patrones de titulo que siempre se marcan prioridad "alta" (Francisco,
# 2026-09-06): contratacion via excepcion, convenios entre organismos.
# Comparacion sobre el titulo SIN espacios: el texto extraido del PDF a
# veces mete un espacio suelto en medio de una palabra por kerning (ej.
# "CONVE NIO" en vez de "CONVENIO", visto en la edicion 28410) y una regex
# sobre el titulo tal cual se lo pierde.
DECRETO_ALTA_PRIORIDAD_PALABRAS = ("EXCEPCION", "EXCEPCIÓN", "CONVENIO")
LEY_PROTOCOLAR_PALABRAS = ("CIUDADANOILUSTRE", "BENEPLACITO", "BENEPLÁCITO", "ADHESION", "ADHESIÓN", "CONMEMORA", "HOMENAJE")


def _sin_espacios(s: str) -> str:
    return re.sub(r"\s+", "", s).upper()


def _contiene_alguna(titulo: str, palabras: tuple[str, ...]) -> bool:
    compacto = _sin_espacios(titulo)
    return any(p in compacto for p in palabras)

FIN_AVISO_COMERCIAL_RE = re.compile(r"ID\s*:\s*\d+[^\n]*?v\./\d{2}/\d{2}/\d{4}")
SECCION_COMERCIAL_RE = re.compile(r"secci[oó]n comercial", re.IGNORECASE)


def _inicio_real_seccion_comercial(texto: str) -> int | None:
    """La cabecera "SECCIÓN COMERCIAL" (todo mayuscula) aparece una sola vez,
    como anuncio al pie del sumario administrativo -- no marca el inicio real
    del contenido. El inicio real es la SEGUNDA aparicion del texto (en
    cualquier combinacion de mayus/minus), que es la cabecera de pagina
    repetida "... BOLETIN OFICIAL / Sección Comercial 1" justo antes de
    "EDICTOS JUDICIALES". Devuelve None si la edicion no tiene Seccion
    Comercial (no deberia pasar, pero mejor no asumir)."""
    ocurrencias = [m.start() for m in SECCION_COMERCIAL_RE.finditer(texto)]
    return ocurrencias[1] if len(ocurrencias) >= 2 else None


# --------------------------------------------------------------------------
# Indice de ediciones y descarga
# --------------------------------------------------------------------------

def obtener_indice_ediciones() -> list[dict]:
    resp = requests.get(INDICE_URL, headers={"Accept": "application/json"}, timeout=20)
    resp.raise_for_status()
    return resp.json()


def ultimo_nro_procesado() -> int:
    if not LOG_PATH.exists():
        return 0
    ultimo = 0
    with open(LOG_PATH, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            try:
                nro = int(json.loads(linea).get("nro", 0))
            except (ValueError, json.JSONDecodeError):
                continue
            ultimo = max(ultimo, nro)
    return ultimo


def url_pdf(fecha_iso: str) -> str:
    anio, mes, dia = fecha_iso.split("-")
    fecha = datetime(int(anio), int(mes), int(dia))
    dd_mm_aa = fecha.strftime("%d-%m-%y")
    return PDF_URL_TPL.format(anio=anio, mes=MESES_ES[fecha.month], dd_mm_aa=dd_mm_aa)


def descargar_pdf(url: str) -> tuple[str, str | None]:
    """Devuelve (texto_completo, last_modified_header). El Last-Modified se
    guarda en el log para ir juntando datos reales de horario de publicacion
    -- ver docs/boletin-oficial-proceso.md, "Horario de corrida"."""
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
    resp.raise_for_status()
    reader = PdfReader(io.BytesIO(resp.content))
    partes = [pagina.extract_text() or "" for pagina in reader.pages]
    return "\n".join(partes), resp.headers.get("Last-Modified")


# --------------------------------------------------------------------------
# Seccion Administrativa: Leyes, Decretos, Resoluciones
# --------------------------------------------------------------------------

def _pagina_al_final(linea: str) -> int | None:
    compacta = re.sub(r"\s+", "", linea)
    m = re.search(r"\.{2,}(\d{1,4})$", compacta)
    return int(m.group(1)) if m else None


def _sin_leader(linea: str) -> str:
    return re.split(r"\.{2,}", linea, maxsplit=1)[0].strip()


def _es_linea_ruido(linea: str) -> bool:
    return linea.startswith("--- PAGINA") or "BOLETIN OFICIAL" in linea.upper()


def parsear_sumario_administrativa(bloque: str) -> list[dict]:
    entradas = []
    categoria = organismo = codigo_pendiente = None
    modo = "AWAIT_CAT"
    buffer_titulo: list[str] = []

    for raw in bloque.splitlines():
        linea = raw.strip()
        if not linea or _es_linea_ruido(linea):
            continue
        if linea in CATEGORIAS_ADMIN:
            categoria = linea
            modo = "AWAIT_ORG"
            continue
        if modo == "AWAIT_ORG":
            organismo = _sin_leader(linea)
            modo = "AWAIT_CODE"
            continue
        if modo in ("AWAIT_CODE", "AWAIT_CODE_OR_ORG") and CODIGO_RE.match(linea):
            codigo_pendiente = linea
            buffer_titulo = []
            modo = "IN_TITLE"
            continue
        if modo == "IN_TITLE":
            pagina = _pagina_al_final(linea)
            parte = _sin_leader(linea)
            if parte:
                buffer_titulo.append(parte)
            if pagina is not None:
                entradas.append(
                    {
                        "categoria": categoria,
                        "organismo": organismo,
                        "codigo": codigo_pendiente,
                        "titulo": " ".join(buffer_titulo).strip(),
                        "pagina": pagina,
                    }
                )
                modo = "AWAIT_CODE_OR_ORG"
            continue
        if modo == "AWAIT_CODE_OR_ORG":
            organismo = _sin_leader(linea)
            modo = "AWAIT_CODE"
            continue

    return entradas


def _patron_de_codigo(codigo: str) -> re.Pattern:
    # el texto extraido del PDF a veces mete espacios sueltos en medio de un
    # codigo por artefactos de kerning (ej. "DTO-2026-2302-E-GER -GOB") --
    # tolerar espacios opcionales entre cada caracter en vez de exigir
    # coincidencia exacta.
    return re.compile(r"\s*".join(re.escape(c) for c in codigo))


def extraer_cuerpos_administrativa(texto: str, entradas: list[dict], fin_sumario: int, fin_seccion: int) -> None:
    """Completa cada entrada con su 'cuerpo' (texto completo), in-place."""
    cursor = fin_sumario
    posiciones = []
    for e in entradas:
        m = _patron_de_codigo(e["codigo"]).search(texto, cursor)
        posiciones.append(m.start() if m else -1)
        if m:
            cursor = m.end()

    for i, e in enumerate(entradas):
        ini = posiciones[i]
        if ini == -1:
            e["cuerpo"] = ""
            continue
        siguiente = posiciones[i + 1] if i + 1 < len(entradas) and posiciones[i + 1] != -1 else fin_seccion
        e["cuerpo"] = texto[ini:siguiente].strip()


# --------------------------------------------------------------------------
# Seccion Comercial: solo Licitaciones (ver docstring del modulo)
# --------------------------------------------------------------------------

def _es_linea_ruido_negrita(linea: str) -> bool:
    """Heuristica: la linea es texto en negrita duplicado por la extraccion
    del PDF (cada caracter aparece dos veces seguidas), no contenido real."""
    compacta = re.sub(r"\s+", "", linea)
    if len(compacta) < 6:
        return True
    pares = sum(1 for i in range(0, len(compacta) - 1, 2) if compacta[i] == compacta[i + 1])
    return pares >= (len(compacta) // 2) * 0.8


def parsear_licitaciones(bloque: str) -> list[dict]:
    avisos = []
    inicio = 0
    for m in FIN_AVISO_COMERCIAL_RE.finditer(bloque):
        parte = bloque[inicio:m.end()]
        inicio = m.end()
        lineas = [l.strip() for l in parte.splitlines() if l.strip()]

        def es_ruido(linea: str) -> bool:
            return (
                _es_linea_ruido_negrita(linea)
                or linea == "LICITACIONES"
                or _es_linea_ruido(linea)
                or set(linea) <= set("- ")
            )

        candidatas = [l for l in lineas if not es_ruido(l)][:2]
        titulo = " / ".join(candidatas)[:200] if candidatas else "Licitación pública"
        m_id = re.search(r"ID\s*:\s*(\d+)", parte)
        avisos.append({"id_aviso": m_id.group(1) if m_id else None, "titulo": titulo, "cuerpo": parte.strip()})
    return avisos


def extraer_bloque_licitaciones(texto: str) -> str | None:
    inicio_cuerpo_comercial = _inicio_real_seccion_comercial(texto)
    if inicio_cuerpo_comercial is None:
        return None
    ini = texto.find("\n LICITACIONES", inicio_cuerpo_comercial)
    if ini == -1:
        ini = texto.find("\nLICITACIONES", inicio_cuerpo_comercial)
    if ini == -1:
        return None
    fin = texto.find("COMUNICADOS", ini + 1)
    return texto[ini:fin] if fin != -1 else texto[ini:]


def categorias_comerciales_no_parseadas(texto: str) -> list[str]:
    """Solo para el log auditable: nombres de categoria del indice de
    Seccion Comercial que no se parsean item por item en esta version."""
    inicio_cuerpo_comercial = _inicio_real_seccion_comercial(texto)
    if inicio_cuerpo_comercial is None:
        return []
    # el indice de Seccion Comercial termina donde arranca el contenido real
    # -- la segunda vez que aparece "SUCESORIOS" (la primera es su propia
    # entrada en el indice, con pagina al final; la segunda es el titulo de
    # la primera subseccion real de contenido).
    primera = texto.find("SUCESORIOS", inicio_cuerpo_comercial)
    segunda = texto.find("SUCESORIOS", primera + 1) if primera != -1 else -1
    fin_indice = segunda if segunda != -1 else inicio_cuerpo_comercial + 2000
    indice = texto[inicio_cuerpo_comercial:fin_indice]
    categorias = []
    for linea in indice.splitlines():
        linea = linea.strip()
        m = re.match(r"^([A-ZÁÉÍÓÚÑ ]{4,40})\s*\.{2,}", linea)
        if m and m.group(1).strip() != "LICITACIONES":
            categorias.append(m.group(1).strip())
    return categorias


# --------------------------------------------------------------------------
# Armado de items de la cablera + log
# --------------------------------------------------------------------------

def _item_backlog(id_sufijo: str, titulo: str, fecha: str, link: str, cuerpo: str) -> dict:
    return {
        "id": f"{FUENTE_ID_PREFIJO}-{id_sufijo}",
        "fuente": FUENTE_NOMBRE,
        "titulo": titulo[:300],
        "fecha": fecha,
        "link": link,
        "texto_original": cuerpo,
        "imagen_url": "",
        "estado": "pendiente",
        "agregado_el": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "procesado_el": None,
        "wp_edit_url": None,
        "motivo_descarte": None,
        "prioridad": "media",
    }


def procesar_edicion(nro: int, fecha: str, backlog: list[dict], ids_existentes: set[str]) -> tuple[list[dict], list[dict]]:
    """Devuelve (items_nuevos, entradas_de_log) para una edicion."""
    pdf_url = url_pdf(fecha)
    texto, last_modified = descargar_pdf(pdf_url)

    fin_sumario = texto.find("SECCIÓN COMERCIAL")
    fin_seccion_admin = _inicio_real_seccion_comercial(texto) or len(texto)

    sumario_admin = texto[texto.find("SUMARIO") + len("SUMARIO"):fin_sumario]
    entradas = parsear_sumario_administrativa(sumario_admin)
    extraer_cuerpos_administrativa(texto, entradas, fin_sumario, fin_seccion_admin)

    nuevos, log = [], []
    for e in entradas:
        base_link = f"{pdf_url}#page={e['pagina'] + 1}"
        if e["categoria"] == "DECRETOS" and RECHAZO_INDIVIDUAL_RE.search(_sin_espacios(e["titulo"])):
            log.append({"nro": nro, "fecha": fecha, "tipo": "filtrado", "categoria": e["categoria"],
                        "codigo": e["codigo"], "titulo": e["titulo"], "motivo": "rechazo_recurso_individual"})
            continue

        prioridad = "media"
        if e["categoria"] == "LEYES":
            prioridad = "baja" if _contiene_alguna(e["titulo"], LEY_PROTOCOLAR_PALABRAS) else "alta"
        elif e["categoria"] == "RESOLUCIONES":
            prioridad = "alta"
        elif e["categoria"] == "DECRETOS" and _contiene_alguna(e["titulo"], DECRETO_ALTA_PRIORIDAD_PALABRAS):
            prioridad = "alta"

        id_sufijo = f"{nro}-{e['codigo']}".lower()
        id_sufijo = re.sub(r"[^a-z0-9]+", "-", id_sufijo).strip("-")
        item = _item_backlog(id_sufijo, f"[{e['organismo']}] {e['titulo']}", fecha, base_link, e["cuerpo"] or e["titulo"])
        item["prioridad"] = prioridad
        if item["id"] not in ids_existentes:
            nuevos.append(item)

    bloque_lic = extraer_bloque_licitaciones(texto)
    if bloque_lic:
        for aviso in parsear_licitaciones(bloque_lic):
            if not aviso["id_aviso"]:
                continue
            id_sufijo = f"{nro}-lic-{aviso['id_aviso']}"
            item = _item_backlog(id_sufijo, f"[Licitación] {aviso['titulo']}", fecha, pdf_url, aviso["cuerpo"])
            item["prioridad"] = "alta"
            if item["id"] not in ids_existentes:
                nuevos.append(item)

    no_parseadas = categorias_comerciales_no_parseadas(texto)
    log.append({
        "nro": nro, "fecha": fecha, "tipo": "resumen_edicion",
        "pdf_last_modified": last_modified,
        "entradas_administrativa": len(entradas),
        "sobrevivientes_administrativa": sum(1 for e in entradas if not (e["categoria"] == "DECRETOS" and RECHAZO_INDIVIDUAL_RE.search(_sin_espacios(e["titulo"])))),
        "licitaciones_encontradas": len(bloque_lic and parsear_licitaciones(bloque_lic) or []),
        "categorias_seccion_comercial_no_parseadas": no_parseadas,
    })
    return nuevos, log


def guardar_log(entradas_log: list[dict]) -> None:
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        for entrada in entradas_log:
            f.write(json.dumps(entrada, ensure_ascii=False) + "\n")


def main() -> None:
    print(f"Consultando {INDICE_URL} ...")
    try:
        indice = obtener_indice_ediciones()
    except requests.RequestException as e:
        print(f"No se pudo consultar el indice: {e}")
        sys.exit(1)

    ultimo = ultimo_nro_procesado()
    if ultimo == 0:
        # primera corrida (sin log todavia): el indice tiene ediciones desde
        # 2020 -- arrancar solo desde la mas reciente, nunca desde el
        # historico completo (séria bajar y parsear miles de PDFs).
        mas_reciente = max(int(ed["nro"]) for ed in indice)
        ultimo = mas_reciente - 1
        print(f"Primera corrida: arranco desde la edicion mas reciente (nro {mas_reciente}), sin procesar el historico.")

    pendientes = sorted((ed for ed in indice if int(ed["nro"]) > ultimo), key=lambda ed: int(ed["nro"]))

    if not pendientes:
        print(f"Sin ediciones nuevas (ultimo nro procesado: {ultimo}).")
        return

    backlog = cargar_backlog()
    ids_existentes = {item.get("id") for item in backlog} | cargar_ids_archivados()
    total_nuevos = []

    for edicion in pendientes:
        nro, fecha = int(edicion["nro"]), edicion["fecha"]
        print(f"Procesando edicion {nro} ({fecha}) ...")
        try:
            nuevos, log = procesar_edicion(nro, fecha, backlog, ids_existentes)
        except (requests.RequestException, ValueError) as e:
            print(f"  No se pudo procesar la edicion {nro}: {e} -- se reintentara en la proxima corrida.")
            continue

        ids_existentes.update(item["id"] for item in nuevos)
        total_nuevos.extend(nuevos)
        guardar_log(log)
        filtrados = sum(1 for l in log if l.get("tipo") == "filtrado")
        print(f"  {len(nuevos)} item(s) nuevo(s) a la cablera, {filtrados} filtrado(s) (ver {LOG_PATH.name}).")

    if not total_nuevos:
        print("Ninguna edicion nueva produjo items para la cablera.")
        return

    backlog.extend(total_nuevos)
    guardar_backlog(backlog)

    print(f"\nAgregados {len(total_nuevos)} item(s) nuevo(s) a la cablera:")
    for item in total_nuevos:
        print(f"  - [{item['prioridad']}] [{item['id']}] {item['titulo'][:100]}")
    print("\nQuedaron en estado 'pendiente' -- revisalos en admin/index.html.")


if __name__ == "__main__":
    main()
