r"""
Filtro deterministico de ruido estructural para la fuente del Consejo
General de Educacion de Entre Rios (pipeline/monitorear_cge.py).

El feed del CGE es muy activo (varios posts por hora en algunos
momentos, confirmado 2026-09-15) pero la enorme mayoria son llamados a
concurso, interinatos/suplencias, listados de aspirantes o convocatorias
de junta de clasificacion -- tramite de gestion docente rutinario, mismo
tipo de "aviso laboral" que ya se filtra para la fuente "empresa" (ver
pipeline/filtro_contenido_empresas.py) y el mismo patron de "convocatoria
sin resultado" de docs/criterios-noticiabilidad.md. Sin este filtro, el
volumen inunda "pendiente" sin aportar nada noticiable caso por caso.

No reemplaza el criterio editorial sobre que SI es noticia (una resolucion
de politica educativa, un conflicto, un cambio normativo) -- solo saca lo
que estructuralmente es gestion de cargos, nunca se oculta del todo (se
marca "descartado" con motivo, igual que el resto de la cablera).
"""

import re

PATRON_GESTION_DOCENTE = re.compile(
    r"\b("
    r"concurso|interinat|suplenc|junta de clasificaci[oó]n|listado de aspirantes|"
    r"orden de m[eé]rito|titularizaci[oó]n|acto p[uú]blico de oferta|oferta de cargos|"
    r"convocatoria a cargos|cargos vacantes|puntaje docente|inscripci[oó]n a concurso"
    r")\b",
    re.IGNORECASE,
)


def clasificar_no_editorial(titulo: str, texto: str) -> str | None:
    """Devuelve un motivo de descarte si el item matchea el patron de
    gestion de cargos docentes, o None si parece contenido editorial
    valido (una resolucion de politica, un conflicto, un anuncio con
    sustancia mas alla de la gestion rutinaria de cargos)."""
    combinado = f"{titulo or ''} {texto or ''}".lower()
    if PATRON_GESTION_DOCENTE.search(combinado):
        return (
            "Gestion rutinaria de cargos docentes (concurso/interinato/suplencia/junta de "
            "clasificacion) -- filtro automatico de ruido estructural, ver "
            "pipeline/filtro_contenido_cge.py."
        )
    return None
