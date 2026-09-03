# -*- coding: utf-8 -*-
"""Escanea todos los posts en busca de <img src> que apunten a un dominio externo (hotlinking:
visiondesarrollista.org, analisisdigital.com.ar) y los re-aloja en la propia biblioteca de medios
de desarrolloentrerriano.org, reescribiendo el contenido para apuntar a la copia local.
Seguro de re-correr: si ya no quedan imagenes externas, no hace nada.
"""
import mimetypes
import re
from _wp import WP_URL, AUTH
import requests

PROPIO = WP_URL.replace("https://", "").replace("http://", "")


def subir_imagen(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        r.raise_for_status()
        content_type = r.headers.get("Content-Type", "").split(";")[0] or mimetypes.guess_type(url)[0] or "image/jpeg"
        if "image" not in content_type:
            return None
        ext = mimetypes.guess_extension(content_type) or ".jpg"
        fname = re.sub(r"[^a-zA-Z0-9]", "-", url.split("/")[-1].split("?")[0])[:80]
        if not fname.lower().endswith(ext):
            fname += ext
        resp = requests.post(
            f"{WP_URL}/wp-json/wp/v2/media", auth=AUTH,
            headers={"Content-Disposition": f'attachment; filename="{fname}"', "Content-Type": content_type},
            data=r.content, timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["source_url"]
    except Exception as e:
        print(f"    fallo subiendo {url}: {e}")
        return None


def main():
    r = requests.get(f"{WP_URL}/wp-json/wp/v2/posts", auth=AUTH, params={"per_page": 100, "status": "publish,draft"})
    r.raise_for_status()
    posts = r.json()

    total_posts_afectados = 0
    total_imagenes = 0

    for p in posts:
        content = p["content"]["rendered"]
        imgs = re.findall(r'<img[^>]+src="([^"]+)"', content)
        externas = [u for u in imgs if PROPIO not in u]
        if not externas:
            continue

        nuevo_content = content
        cambios = 0
        for url_externa in set(externas):
            nueva_url = subir_imagen(url_externa)
            if nueva_url:
                nuevo_content = nuevo_content.replace(url_externa, nueva_url)
                cambios += 1
                total_imagenes += 1

        if cambios:
            resp = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{p['id']}", auth=AUTH, json={"content": nuevo_content}, timeout=30)
            resp.raise_for_status()
            print(f"OK: post {p['id']} '{p['title']['rendered'][:50]}' - {cambios} imagenes re-alojadas")
            total_posts_afectados += 1

    print(f"\nTotal: {total_posts_afectados} posts corregidos, {total_imagenes} imagenes re-alojadas")


if __name__ == "__main__":
    main()
