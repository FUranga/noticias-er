# -*- coding: utf-8 -*-
"""Restaura la fecha original de cada post despues de un bulk-edit-a-publish desde wp-admin
(el bulk edit del listado de WP resetea 'date' a 'ahora' si no se preserva explicitamente).
Bug conocido: paso 2 veces en esta sesion, cada vez que se publico en lote manualmente.
Matchea por TITULO contra un diccionario fecha original conocida -- si en el futuro cambia
un titulo, este script deja de encontrarlo (se imprime en 'Sin fecha conocida').
"""
import json
import os
from _wp import WP_URL, AUTH
import requests

# Fechas originales conocidas (titulo -> fecha ISO), juntadas de los scripts de importacion
# (Visión Desarrollista + analisisdigital.com.ar, no vienen del JSON de históricos)
FECHAS = {
    "Las mentiras de Milei no tapan el derrumbe del sector privado": "2026-08-22T20:41:44",
    "El túnel subfluvial no tiene una «huella nazi»": "2026-04-28T20:08:45",
    "Marciano Martínez, el último desarrollista entrerriano": "2025-12-15T13:49:58",
    "Sergio Varisco, uno de los nuestros": "2021-05-28T12:34:04",
    "El fin del aislamiento entrerriano": "2019-12-13T00:00:52",
    "¿Qué aprendimos en 60 años del gobierno desarrollista?": "2018-05-03T00:00:30",
    "El espíritu federalista": "2015-08-13T12:15:15",
    "Hacia un modelo regional: la urgencia de transformar la gestión de residuos en Entre Ríos": "2026-06-04T21:03:17",
    "La observación electoral como herramienta de control sobre los gobernantes": "2020-10-08T13:17:10",
    "Alimentar la tierra para potenciar el futuro: el desafío de una producción sostenible": "2026-06-15T14:28:34",
    "Moine disertará sobre la profesionalización del Estado en Entre Ríos": "2021-04-21T17:26:31",
    "Entre Ríos espera su milagro argentino: entrevista a Raúl Uranga en la revista Qué": "2015-08-13T12:12:23",
    "La región centro, punto productivo estratégico hacia el mundo": "2025-04-07T18:28:14",
    "A 60 años del discurso de Paraná": "2022-02-05T11:51:02",
    "La avicultura entrerriana lidera el mercado interno pero las exportaciones retroceden": "2021-07-03T13:18:27",
    "Charla virtual 'Hidrovía, qué está en juego en la licitación'": "2021-05-26T12:08:36",
    "Magallán: «El Estado hace poco para prevenir los incendios forestales»": "2021-05-14T17:27:07",
    "Molina: «La industria de los biocombustibles enfrenta una crisis muy grande»": "2021-05-26T01:30:00",
    "Charla virtual sobre las responsabilidades en los incendios forestales": "2021-05-13T11:44:07",
    "Morchio: “La ley de fitosanitarios necesita un cambio radical para adaptarse a las nuevas tecnologías”": "2021-04-16T16:35:29",
    "Ferrari del Sel: “Los políticos no estudian los problemas nacionales»": "2017-12-05T00:20:37",
    "Protagonistas: Carlos Sylvestre Begnis": "2017-12-05T00:08:56",
    "Sauret: «Los desarrollistas somos mercadointernistas por definición»": "2017-10-25T00:20:26",
    "Discurso de Carlos Sylvestre Begnis tras la firma del contrato del túnel subfluvial": "2017-05-26T16:13:05",
    "Marciano Martínez: «Los partidos políticos se forjan a partir de la militancia en la calle»": "2015-08-13T12:20:46",
    "Protagonistas: Raúl Uranga": "2015-08-13T12:14:00",
}

# Sumar las fechas de las 54 historicas desde el JSON (docs/novedades-historicas-fundacion.json)
JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "docs", "novedades-historicas-fundacion.json")
with open(JSON_PATH, encoding="utf-8") as f:
    historicos = json.load(f)
for item in historicos:
    fecha = item.get("fecha") or "2015-01-01"
    if len(fecha) == 10:
        fecha += "T12:00:00"
    FECHAS[item["titulo"]] = fecha


def main():
    r = requests.get(f"{WP_URL}/wp-json/wp/v2/posts", auth=AUTH, params={"per_page": 100, "status": "publish,draft"})
    r.raise_for_status()
    posts = r.json()
    print(f"Total posts (publish+draft): {len(posts)}")

    corregidos, sin_match = 0, []
    for p in posts:
        titulo = p["title"]["rendered"]
        fecha_correcta = FECHAS.get(titulo)
        if not fecha_correcta:
            sin_match.append((p["id"], titulo))
            continue
        fecha_actual = p["date"]
        if fecha_actual[:10] == fecha_correcta[:10]:
            continue  # ya esta bien
        resp = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{p['id']}", auth=AUTH, json={"date": fecha_correcta}, timeout=30)
        resp.raise_for_status()
        print(f"Corregido: {p['id']} {titulo[:50]} -> {fecha_correcta[:10]}")
        corregidos += 1

    print(f"\nTotal corregidos: {corregidos}")
    if sin_match:
        print(f"Sin fecha conocida ({len(sin_match)}):")
        for pid, t in sin_match:
            print(" -", pid, t)


if __name__ == "__main__":
    main()
