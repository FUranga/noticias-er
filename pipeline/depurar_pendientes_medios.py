r"""
Depura los items "medios-*" en estado "pendiente" de data/backlog.json, en
dos pasadas (Francisco, 2026-09-12 -- ver conversacion de diseno):

1. Filtro mecanico por patron de TITULO (data/criterios_depuracion_medios.json)
   -- mismas categorias que se vinieron aplicando a mano en el triage manual
   de Boletin+Medios del 2026-09-11/12 (deporte, espectaculo, policial menor,
   efemeride, edicto, nacional sin angulo de ER, servicio/agenda, tramite sin
   resultado). Es un filtro de CONTENIDO, no de antiguedad -- corre sobre
   cualquier pendiente de Medios sin importar cuando llego.

2. Lo que sobrevive al punto 1 pero lleva mas de HORAS_EXPIRACION en estado
   "pendiente" se descarta con un motivo que dice explicitamente que fue
   automatico por antiguedad, nunca como si hubiera sido una evaluacion
   editorial real -- la decision de que ES noticia sigue siendo humana (ver
   CLAUDE.md); esto es pura higiene de cola para que "Medios > Pendientes"
   no acumule para siempre lo que nadie llego a mirar.

Ambas pasadas dejan el motivo con el sufijo "(automatico)" para que se
distinga a simple vista, en el panel, de un descarte editorial real -- y
"Reabrir" en admin/index.html deshace cualquiera de los dos sin friccion,
igual que cualquier otro descarte.

Uso:
    python depurar_pendientes_medios.py
"""

import json
import re
import sys
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from monitorear_gobierno_er import cargar_backlog, guardar_backlog  # noqa: E402

CRITERIOS_PATH = Path(__file__).resolve().parent.parent / "data" / "criterios_depuracion_medios.json"
HORAS_EXPIRACION = 48


def _normalizar(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def cargar_criterios() -> dict:
    with open(CRITERIOS_PATH, encoding="utf-8") as f:
        return json.load(f)["categorias"]


def clasificar_por_titulo(titulo: str, criterios: dict) -> str | None:
    t = _normalizar(titulo or "")
    for nombre, cfg in criterios.items():
        for palabra in cfg["palabras"]:
            if re.search(rf"\b{re.escape(_normalizar(palabra))}", t):
                return cfg["motivo"]
    return None


def es_medios_pendiente(item: dict) -> bool:
    return item.get("id", "").startswith("medios-") and item.get("estado") == "pendiente"


def horas_desde(agregado_el: str | None) -> float | None:
    if not agregado_el:
        return None
    try:
        dt = datetime.strptime(agregado_el, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None
    return (datetime.now(timezone.utc) - dt).total_seconds() / 3600


def main() -> None:
    criterios = cargar_criterios()
    backlog = cargar_backlog()

    por_contenido = 0
    por_antiguedad = 0

    for item in backlog:
        if not es_medios_pendiente(item):
            continue

        motivo = clasificar_por_titulo(item.get("titulo", ""), criterios)
        if motivo:
            item["estado"] = "descartado"
            item["motivo_descarte"] = f"{motivo} (automático)"
            por_contenido += 1
            continue

        horas = horas_desde(item.get("agregado_el"))
        if horas is not None and horas > HORAS_EXPIRACION:
            item["estado"] = "descartado"
            item["motivo_descarte"] = (
                f"Vencido: pasaron mas de {HORAS_EXPIRACION} horas sin revision editorial (automático)."
            )
            por_antiguedad += 1

    total = por_contenido + por_antiguedad
    if total == 0:
        print("Nada para depurar.")
        return

    guardar_backlog(backlog)
    print(f"Descartados {por_contenido} por contenido (filtro mecanico) + {por_antiguedad} por antiguedad (>{HORAS_EXPIRACION}h).")


if __name__ == "__main__":
    main()
