# -*- coding: utf-8 -*-
"""Asigna una categoria (Opinión/Evento/Informe/Entrevista/Institucional) a cada post existente
por heuristica de titulo/autor/contenido. Corrido una vez sobre los 81 posts importados.
Resultado: ~44 cayeron en el catch-all 'Institucional' -- pendiente de revision manual
(ver docs/checklist-sitio-fundacion.md, seccion 2). Re-correr es seguro (idempotente),
pero solo pisa la categoria, no aprende de correcciones manuales previas.
"""
import re
from _wp import WP_URL, AUTH
import requests

CAT_IDS = {"Opinión": 4, "Evento": 5, "Informe": 6, "Entrevista": 7, "Institucional": 8}

# Patrones por titulo (orden importa, primer match gana)
EVENTO_PAT = re.compile(r"charla virtual|seminario|encuentro|acto por|se realizar[aá]|se presenta el libro|inaugura la delegaci[oó]n|homenaje a", re.I)
ENTREVISTA_PAT = re.compile(r"^protagonistas|entrevista|:\s*[«\"]|^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+:\s", re.U)
OPINION_AUTORES = ["francisco uranga", "javier lisandro manzo", "francisco morchio", "marciano martínez", "esteban turcatti"]
INFORME_PAT = re.compile(r"an[aá]lisis del discurso|la avicultura|la regi[oó]n centro|desaf[ií]os de|desaf[ií]os para|hacia un modelo", re.I)


def elegir_categoria(titulo, autor, texto):
    t = titulo.lower()
    if EVENTO_PAT.search(titulo):
        return "Evento"
    if ENTREVISTA_PAT.search(titulo):
        return "Entrevista"
    if INFORME_PAT.search(titulo):
        return "Informe"
    autor_l = (autor or "").lower()
    if any(a in autor_l for a in OPINION_AUTORES):
        return "Opinión"
    if "por francisco uranga" in texto.lower()[:400] or "opini&oacute;n" in texto.lower()[:200]:
        return "Opinión"
    return "Institucional"


def main():
    r = requests.get(f"{WP_URL}/wp-json/wp/v2/posts", auth=AUTH, params={"per_page": 100, "status": "publish,draft", "_embed": "author"})
    r.raise_for_status()
    posts = r.json()
    print(f"Total posts: {len(posts)}")

    conteo = {}
    for p in posts:
        titulo = p["title"]["rendered"]
        content = p["content"]["rendered"]
        autor = None
        try:
            autor = p["_embedded"]["author"][0]["name"]
        except Exception:
            pass
        cat_nombre = elegir_categoria(titulo, autor, content)
        cat_id = CAT_IDS[cat_nombre]
        conteo[cat_nombre] = conteo.get(cat_nombre, 0) + 1

        resp = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{p['id']}", auth=AUTH, json={"categories": [cat_id]}, timeout=30)
        resp.raise_for_status()

    print("\nDistribucion:")
    for k, v in conteo.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
