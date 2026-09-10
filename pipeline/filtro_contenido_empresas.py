r"""
Filtro deterministico de contenido no editorial para la fuente "empresa"
(pipeline/monitorear_empresas.py). Muchas de las 67 empresas monitoreadas
via RSS solo tienen un feed generico de WordPress (`/feed/` del sitio
entero), sin seccion de prensa propia -- ese feed trae catalogo de
productos, recetas, avisos de busqueda laboral y blogs de tips genericos,
no comunicados. Este modulo detecta esos patrones para no cargarlos como
"pendiente" -- se marcan "descartado" con motivo, nunca se ocultan del
todo (ver docs/fuentes.md y el hallazgo del 2026-09-10).

No reemplaza el criterio editorial sobre lo que SI es un comunicado --
solo saca lo que estructuralmente no lo es (receta, aviso laboral, ficha
de producto sin hecho noticioso, articulo de tips). Ver
`feedback_forkear_triage_cablera` / `proyecto_ruido_estructural_cablera`
en la memoria del proyecto para el contexto de por que se agrego esto.
"""

import re

RUTAS_AVISO_LABORAL = [
    "/rrhh/",
    "/busqueda-laboral/",
    "/bolsa-de-trabajo/",
    "/empleos/",
    "/trabaja-con-nosotros/",
    "/trabajanosotros",
    "/careers/",
]

PATRON_TIPS_GENERICOS = re.compile(
    r"^(c[oó]mo |consejos para |¿qu[eé] es|¿c[oó]mo |¿por qu[eé]|la importancia de |ventajas de |ventajas del )",
    re.IGNORECASE,
)

VERBOS_DE_ACCION_INSTITUCIONAL = re.compile(
    r"\b("
    r"firm[oó]|firma|anunci[oó]|anuncia|present[oó]|presenta|particip[oó]|participa|"
    r"inform[oó]|informa|lanz[oó]|lanza|inaugur[oó]|inaugura|denunci[oó]|denuncia|"
    r"rechaz[oó]|rechaza|solicit[oó]|solicita|celebr[oó]|celebra|entreg[oó]|entrega|"
    r"aprob[oó]|aprueba|convoc[oó]|convoca|manifiesta|manifest[oó]|considera|"
    r"exige|reclam[oó]|reclama|advirti[oó]|advierte|sostuvo|sostiene|destac[oó]|destaca|"
    r"expres[oó]|expresa|afirm[oó]|afirma|sancion[oó]|sanciona"
    r")\b",
    re.IGNORECASE,
)


def clasificar_no_editorial(titulo: str, texto: str, link: str, es_camara: bool = False) -> str | None:
    """Devuelve un motivo de descarte si el item matchea un patron no
    editorial conocido, o None si parece contenido editorial valido
    (comunicado real, aunque sea autopromocional -- eso lo evalua el
    editor, no este filtro).

    `es_camara`: True para las 6 fuentes de `data/fuentes_camaras.json`
    (UIER, CEER, Centro Comercial de Parana, FEDER, Bolsa de Cereales ER,
    CAMARCO ER) -- camaras reales con seccion de prensa verificada, que
    publican comunicados cortos y legitimos sin necesariamente usar un
    verbo de la lista de abajo (ej. "Informe de coyuntura julio 2026",
    "Visita del Secretario de Turismo de Nacion Daniel Scioli"). Para esas
    NO se aplica el chequeo de "sin verbo de accion" (alto riesgo de falso
    positivo, confirmado 2026-09-10: 10/12 y 5/11 de FEDER/CEER
    respectivamente se marcaban mal con ese chequeo solo). El resto de
    `data/organismos_empresas.json` (empresas individuales, RSS solo
    confirmado tecnicamente, contenido nunca verificado) si lo usa --
    ahi el chequeo dio cero falsos positivos contra los comunicados reales
    conocidos."""
    link_lower = (link or "").lower()
    if any(ruta in link_lower for ruta in RUTAS_AVISO_LABORAL):
        return "Aviso de busqueda laboral (filtro automatico de contenido no editorial)."

    texto_lower = (texto or "").lower()
    if "ingredientes" in texto_lower and ("preparaci" in texto_lower or "paso 1" in texto_lower):
        return "Receta/contenido de blog gastronomico (filtro automatico de contenido no editorial)."

    if PATRON_TIPS_GENERICOS.match((titulo or "").strip()):
        return "Articulo de tips/blog generico sin hecho noticioso (filtro automatico de contenido no editorial)."

    if es_camara:
        return None

    palabras = texto.split() if texto else []
    if len(palabras) < 300 and not VERBOS_DE_ACCION_INSTITUCIONAL.search(texto_lower):
        return "Descripcion de producto/servicio sin hecho noticioso (filtro automatico de contenido no editorial)."

    return None
