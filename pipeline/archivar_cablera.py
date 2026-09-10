r"""
Muda de data/backlog.json a data/archivo/ los items que ya terminaron su
ciclo editorial, para que la cablera activa no crezca para siempre (Francisco,
2026-09-10 -- el archivo ya pesaba 3.2MB / 1169+ items y rompia la carga del
panel admin via la API de Contents de GitHub).

No es una decision editorial: no cambia el estado de ningun item, solo lo
saca de backlog.json y lo guarda tal cual en otro archivo. Los items movidos
siguen existiendo (y buscables via grep/git) en data/archivo/, solo dejan de
aparecer en admin/index.html.

Dos modos, pensados para correr con distinta frecuencia (ver
.github/workflows/archivar_descartados.yml y archivar_publicados.yml):

  descartados -- estado "descartado" o "referido" (decisiones editoriales
    finales que nunca generan un borrador en WordPress). Semanal: son el
    volumen mas alto y no hace falta revisitarlos.

  publicados -- estado "a_publicar" con wp_edit_url ya cargado (el pipeline
    ya subio el borrador a WordPress; lo que pasa despues -- revision y
    publicacion final -- ocurre en WordPress, no en la cablera). Mensual: se
    les da margen por si el editor todavia los esta revisando en WordPress.

Uso:
    python archivar_cablera.py descartados
    python archivar_cablera.py publicados
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from monitorear_gobierno_er import cargar_backlog, guardar_backlog  # noqa: E402

ARCHIVO_DIR = Path(__file__).resolve().parent.parent / "data" / "archivo"
ARCHIVO_DESCARTADOS_PATH = ARCHIVO_DIR / "backlog-descartados.json"
ARCHIVO_PUBLICADOS_PATH = ARCHIVO_DIR / "backlog-publicados.json"

ESTADOS_DESCARTABLES = {"descartado", "referido"}


def cargar_archivo(path: Path) -> list[dict]:
    if not path.exists():
        return []
    import json

    with open(path, encoding="utf-8") as f:
        return json.load(f)


def guardar_archivo(path: Path, items: list[dict]) -> None:
    import json

    ARCHIVO_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def archivar(candidatos: list[dict], archivo_path: Path, etiqueta: str) -> None:
    if not candidatos:
        print(f"Sin items para archivar ({etiqueta}).")
        return

    backlog = cargar_backlog()
    ids_a_mover = {i["id"] for i in candidatos}
    restantes = [i for i in backlog if i["id"] not in ids_a_mover]

    archivo = cargar_archivo(archivo_path)
    archivo.extend(candidatos)
    guardar_archivo(archivo_path, archivo)
    guardar_backlog(restantes)

    print(f"Archivados {len(candidatos)} item(s) ({etiqueta}) -> {archivo_path}:")
    for item in candidatos:
        print(f"  - [{item['id']}] {item['titulo']}")


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ("descartados", "publicados"):
        print("Uso: python archivar_cablera.py <descartados|publicados>")
        sys.exit(1)

    backlog = cargar_backlog()

    if sys.argv[1] == "descartados":
        candidatos = [i for i in backlog if i.get("estado") in ESTADOS_DESCARTABLES]
        archivar(candidatos, ARCHIVO_DESCARTADOS_PATH, "descartados/referidos")
    else:
        candidatos = [
            i
            for i in backlog
            if i.get("estado") == "a_publicar" and i.get("wp_edit_url")
        ]
        archivar(candidatos, ARCHIVO_PUBLICADOS_PATH, "publicados")


if __name__ == "__main__":
    main()
