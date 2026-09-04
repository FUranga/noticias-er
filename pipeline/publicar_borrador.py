r"""
Sube una noticia ya redactada (formato de salida de la skill `redactar-noticia`)
como borrador (`draft`) en WordPress, via su API REST.

Uso:
    python publicar_borrador.py nota.txt
    python publicar_borrador.py nota.txt https://ejemplo.org/imagen.jpg
    python publicar_borrador.py nota.txt C:\ruta\a\imagen_local.jpg "Foto: Gobierno de Entre Rios"

El segundo argumento (opcional) es una imagen destacada: una URL o una ruta
local. Si se pasa, se sube a la biblioteca de medios de WordPress y se
asocia al borrador como imagen destacada.

El tercer argumento (opcional, solo tiene efecto si hay imagen) es el
credito de la foto (ver docs/politica-imagenes.md) -- se guarda como
"caption" del media en WordPress, y el frontend lo muestra como leyenda
visible debajo de la imagen.

El archivo de entrada tiene que tener el formato:

    Titulo: ...

    Bajada: ...

    [Cuerpo en parrafos cortos, con la atribucion de cada dato tejida adentro]

Credenciales en pipeline/.env (nunca se commitea - ver .env.example):
    WP_URL=https://tu-dominio-temporal.hostingersite.com
    WP_USER=tu-usuario-de-wordpress
    WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
"""

import mimetypes
import os
import re
import sys
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv()

WP_URL = os.environ.get("WP_URL", "").rstrip("/")
WP_USER = os.environ.get("WP_USER", "")
WP_APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")


def parse_nota(texto: str) -> dict:
    """Separa el texto en titulo / bajada / cuerpo segun el formato de redactar-noticia."""
    titulo_m = re.search(r"^T[ií]tulo:\s*(.+)$", texto, re.MULTILINE)
    bajada_m = re.search(r"^Bajada:\s*(.+)$", texto, re.MULTILINE)

    if not titulo_m:
        raise ValueError("No encontre una linea 'Titulo:' en el archivo.")

    titulo = titulo_m.group(1).strip()
    bajada = bajada_m.group(1).strip() if bajada_m else ""

    # El cuerpo es todo lo que queda despues de la bajada.
    inicio_cuerpo = bajada_m.end() if bajada_m else titulo_m.end()
    cuerpo = texto[inicio_cuerpo:].strip()

    return {"titulo": titulo, "bajada": bajada, "cuerpo": cuerpo}


def a_html(nota: dict) -> str:
    """Arma el content HTML del post: bajada en negrita como lead, despues los parrafos del cuerpo."""
    partes = []
    if nota["bajada"]:
        partes.append(f"<p><strong>{nota['bajada']}</strong></p>")
    for parrafo in nota["cuerpo"].split("\n\n"):
        parrafo = parrafo.strip()
        if parrafo:
            partes.append(f"<p>{parrafo}</p>")
    return "\n".join(partes)


def _nombre_archivo(origen: str) -> str:
    nombre = os.path.basename(urlparse(origen).path) or "imagen.jpg"
    return nombre


def subir_imagen_destacada(origen: str) -> int:
    """Sube una imagen (URL o ruta local) a la biblioteca de medios y devuelve su id."""
    if origen.startswith("http://") or origen.startswith("https://"):
        r = requests.get(origen, timeout=30)
        r.raise_for_status()
        contenido = r.content
        content_type = r.headers.get("Content-Type", "").split(";")[0] or mimetypes.guess_type(origen)[0] or "image/jpeg"
    else:
        with open(origen, "rb") as f:
            contenido = f.read()
        content_type = mimetypes.guess_type(origen)[0] or "image/jpeg"

    nombre = _nombre_archivo(origen)
    resp = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media",
        auth=(WP_USER, WP_APP_PASSWORD),
        headers={
            "Content-Disposition": f'attachment; filename="{nombre}"',
            "Content-Type": content_type,
        },
        data=contenido,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["id"]


def set_credito_imagen(imagen_id: int, credito: str) -> None:
    """Guarda el credito de la foto como 'caption' del media ya subido."""
    resp = requests.post(
        f"{WP_URL}/wp-json/wp/v2/media/{imagen_id}",
        auth=(WP_USER, WP_APP_PASSWORD),
        json={"caption": credito},
        timeout=30,
    )
    resp.raise_for_status()


def crear_borrador(nota: dict, imagen_id: int | None = None) -> dict:
    if not (WP_URL and WP_USER and WP_APP_PASSWORD):
        raise RuntimeError(
            "Faltan WP_URL / WP_USER / WP_APP_PASSWORD. Revisa pipeline/.env "
            "(copia .env.example si todavia no lo creaste)."
        )

    payload = {
        "title": nota["titulo"],
        "content": a_html(nota),
        "excerpt": nota["bajada"],
        "status": "draft",
    }
    if imagen_id:
        payload["featured_media"] = imagen_id

    resp = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts",
        auth=(WP_USER, WP_APP_PASSWORD),
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    if len(sys.argv) not in (2, 3, 4):
        print("Uso: python publicar_borrador.py <archivo_de_nota.txt> [imagen_url_o_ruta] [credito_de_foto]")
        sys.exit(1)

    ruta = sys.argv[1]
    imagen_origen = sys.argv[2] if len(sys.argv) >= 3 else None
    credito = sys.argv[3] if len(sys.argv) == 4 else None

    with open(ruta, encoding="utf-8") as f:
        texto = f.read()

    nota = parse_nota(texto)
    print(f"Titulo detectado: {nota['titulo']}")

    imagen_id = None
    if imagen_origen:
        try:
            print(f"Subiendo imagen destacada desde: {imagen_origen}")
            imagen_id = subir_imagen_destacada(imagen_origen)
            print(f"Imagen subida (media id {imagen_id})")
            if credito:
                set_credito_imagen(imagen_id, credito)
                print(f"Credito guardado: {credito}")
        except Exception as e:
            print(f"No se pudo subir la imagen ({e}) - sigo sin imagen destacada.")

    resultado = crear_borrador(nota, imagen_id)
    editar_url = f"{WP_URL}/wp-admin/post.php?post={resultado['id']}&action=edit"
    print(f"Borrador creado (id {resultado['id']}). Revisalo aca:\n{editar_url}")


if __name__ == "__main__":
    main()
