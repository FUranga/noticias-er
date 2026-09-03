# -*- coding: utf-8 -*-
"""Crea la pagina 'Novedades' (archivo de posts paginado) y 'Informes' (placeholder),
las configura como page_for_posts, y arma el menu principal completo con submenu 'Sobre'.
Script de setup inicial -- ya corrido una vez. Volver a correrlo crearia paginas/menu duplicados
(usa crear_pagina_simple sin chequear si ya existen). Se preserva como referencia de la estructura.
"""
from _wp import WP_URL, AUTH
import requests

PAGES = {
    "inicio": 55,
    "quienes_somos": 5,
    "fundador": 6,
    "raul_uranga": 7,
    "autoridades": 8,
    "contacto": 9,
    "biblioteca": 10,
}


def crear_pagina_simple(titulo, contenido, status="publish"):
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/pages", auth=AUTH, json={"title": titulo, "content": contenido, "status": status}, timeout=30)
    r.raise_for_status()
    return r.json()["id"]


def main():
    # 1) Pagina "Novedades" (va a ser la pagina de posts -> listado paginado automatico)
    novedades_id = crear_pagina_simple("Novedades", "")
    print(f"Pagina Novedades creada: id {novedades_id}")

    # 2) Pagina "Informes" placeholder
    informes_id = crear_pagina_simple(
        "Informes",
        "<p><em>Próximamente.</em></p>",
    )
    print(f"Pagina Informes creada: id {informes_id}")

    # 3) Configurar Novedades como pagina de posts
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/settings", auth=AUTH, json={"page_for_posts": novedades_id}, timeout=30)
    r.raise_for_status()
    print("page_for_posts ->", r.json().get("page_for_posts"))

    # 4) Crear el menu
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/menus", auth=AUTH, json={"name": "Principal", "locations": ["primary"]}, timeout=30)
    r.raise_for_status()
    menu = r.json()
    menu_id = menu["id"]
    print(f"Menu creado: id {menu_id}, locations: {menu.get('locations')}")

    def item(title, menu_order, parent=0, object_id=None, url=None, object_type="page"):
        payload = {
            "title": title,
            "menus": menu_id,
            "menu_order": menu_order,
            "parent": parent,
            "status": "publish",
        }
        if object_id:
            payload["object"] = object_type
            payload["object_id"] = object_id
            payload["type"] = "post_type"
        else:
            payload["type"] = "custom"
            payload["url"] = url or "#"
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/menu-items", auth=AUTH, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()["id"]

    # "Sobre" como item padre (link custom "#", solo despliega el submenu)
    sobre_id = item("Sobre", 1, url="#")
    item("FUNDER", 1, parent=sobre_id, object_id=PAGES["quienes_somos"])
    item("Autoridades", 2, parent=sobre_id, object_id=PAGES["autoridades"])
    item("Raúl Uranga", 3, parent=sobre_id, object_id=PAGES["raul_uranga"])
    item("El fundador", 4, parent=sobre_id, object_id=PAGES["fundador"])

    item("Novedades", 2, object_id=novedades_id)
    item("Informes", 3, object_id=informes_id)
    item("Contacto", 4, object_id=PAGES["contacto"])
    item("Inicio", 5, object_id=PAGES["inicio"])

    print("Menu armado con exito.")


if __name__ == "__main__":
    main()
