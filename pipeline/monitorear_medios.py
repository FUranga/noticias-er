r"""
Captura del futuro agregador "Medios": agrega notas nuevas de otros medios
(provinciales y locales de Entre Rios, por ahora) a la cablera
(data/backlog.json) en estado "pendiente", bajo la macro-pestana "Medios"
de admin/index.html (filtra por el prefijo "medios-" del id).

No decide nada -- solo carga candidatos para que el editor los mire despues.
Ver CLAUDE.md: la decision de que es noticia es siempre humana. Distinto en
un punto de las demas fuentes de la cablera: el tratamiento editorial de un
item que viene de otro medio no es "reescribir un comunicado" -- es
atribuir de forma explicita y prominente, sumar valor propio antes que
reescribir, y con mas cuidado cuanto mas chico el medio de origen (ver
docs/estilo-editorial.md, seccion "Medios y empresas como fuente").

Filtro TOPICO Y LUGAR (2026-09-07, afinado en dos pasadas reales):
1. Primera corrida sin filtro: 60 items de solo 4 feeds, varios sin ninguna
   relacion con el proyecto (Cuba, Malvinas, un estudio de cancer) -- un
   medio generalista publica de todo, no solo su beat institucional.
2. Filtro de topicos solo (politica, economia, justicia, etc.): bajo de 60
   a 51 -- casi nada, porque palabras como "politica" o "empleo" aparecen
   en cualquier nota, tenga o no que ver con Entre Rios (una columna de
   opinion sobre Milei matchea "politica" sin decir "Entre Rios" en ningun
   lado).
Se necesitan LAS DOS cosas a la vez: topico Y lugar, no una sola. Filtro
mecanico por palabra clave (mismo espiritu que el filtro del Boletin
Oficial, ver docs/boletin-oficial-proceso.md: nunca decide que ES noticia,
solo que tipo de nota nunca tiene esa chance) sobre titulo + cuerpo. Listas
en data/topicos_medios.json y data/lugares_medios.json (parametrizables,
vivas -- se van a ir afinando con el uso real). Lo que no pasa el filtro NO
se pierde en silencio: queda logueado en data/log_filtro_medios.jsonl con
motivo, igual que el filtro del Boletin.

Sin filtro de organismos/personalidades todavia -- lista pendiente de
armar (ver docs/fuentes.md, seccion "Medios", "Proximos pasos").

Dos tipos de fuente en data/fuentes_medios.json:
- "rss": feed propio de un medio confirmado (parseado con feedparser).
- "google_news": busqueda de Google News RSS (parametro "query", mas
  "ventana_dias" opcional para el recorte "when:Nd" -- default 2 dias).
  Es un endpoint NO OFICIAL de Google (no documentado, puede cambiar o
  bloquearse sin aviso) -- util para agarrar medios que no tenemos
  mapeados o sin RSS propio confirmado, a costa de esa fragilidad. El link
  que devuelve es un redirect de news.google.com, no la URL directa del
  medio -- funciona para abrir la nota, pero no es la URL canonica.

Uso:
    python monitorear_medios.py
"""

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlparse

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from feed_utils import parsear_feed_con_reintentos  # noqa: E402
from monitorear_gobierno_er import cargar_backlog, guardar_backlog, limpiar_html  # noqa: E402
from monitorear_senado_er import slug_de_link  # noqa: E402

MEDIOS_PATH = Path(__file__).resolve().parent.parent / "data" / "fuentes_medios.json"
TOPICOS_PATH = Path(__file__).resolve().parent.parent / "data" / "topicos_medios.json"
LUGARES_PATH = Path(__file__).resolve().parent.parent / "data" / "lugares_medios.json"
LOG_FILTRO_PATH = Path(__file__).resolve().parent.parent / "data" / "log_filtro_medios.jsonl"

GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q={query}&hl=es-419&gl=AR&ceid=AR:es-419"


def cargar_medios() -> list[dict]:
    with open(MEDIOS_PATH, encoding="utf-8") as f:
        return json.load(f)


def cargar_topicos() -> dict[str, list[str]]:
    with open(TOPICOS_PATH, encoding="utf-8") as f:
        return json.load(f)


def cargar_lugares() -> list[str]:
    with open(LUGARES_PATH, encoding="utf-8") as f:
        return json.load(f)


def texto_matchea(texto: str, palabras: list[str]) -> list[str]:
    # \b (limite de palabra) evita falsos positivos por substring dentro de
    # otra palabra -- ej. "elección" matcheando adentro de "selección"
    # (bug real encontrado en la corrida de prueba: una nota de handball
    # sobre "selecciones menores" quedaba marcada como tópico "elecciones").
    texto = texto.lower()
    return [p for p in palabras if re.search(rf"\b{re.escape(p)}", texto)]


def loguear_filtrado(item: dict, motivo: str) -> None:
    entrada = {
        "id": item["id"],
        "fuente": item["fuente"],
        "titulo": item["titulo"],
        "link": item["link"],
        "motivo": motivo,
        "filtrado_el": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with open(LOG_FILTRO_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entrada, ensure_ascii=False) + "\n")


def _id_de_link(link: str, es_google_news: bool) -> str:
    if es_google_news:
        # El link de Google News es un redirect largo (news.google.com/rss/
        # articles/CBMi...) -- un slug legible se vuelve un blob gigante,
        # usamos un hash corto en su lugar.
        return hashlib.sha1(link.encode("utf-8")).hexdigest()[:12]
    return slug_de_link(link)


def _items_desde_parsed(parsed, id_prefijo: str, fuente_fallback: str | None) -> list[dict]:
    items = []
    es_google_news = fuente_fallback is None
    for entry in parsed.entries:
        titulo_crudo = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
        if not titulo_crudo or not link:
            continue

        # Google News antepone " - Medio" al final del título -- lo usamos
        # como fuente real cuando no nos dieron una fija (fuente_fallback).
        titulo, fuente = titulo_crudo, fuente_fallback
        if es_google_news and " - " in titulo_crudo:
            titulo, fuente = titulo_crudo.rsplit(" - ", 1)

        contenido = entry.get("content")
        cuerpo_html = contenido[0].get("value") if contenido else entry.get("summary") or ""

        try:
            fecha = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).strftime("%Y-%m-%d")
        except (TypeError, AttributeError):
            fecha = ""

        items.append(
            {
                "id": f"{id_prefijo}-{_id_de_link(link, es_google_news)}",
                "fuente": fuente or "Google News",
                "titulo": titulo.strip(),
                "fecha": fecha,
                "link": link,
                "texto": limpiar_html(cuerpo_html),
            }
        )
    return items


def obtener_items_de_medio(medio: dict) -> list[dict]:
    if medio.get("tipo") == "google_news":
        ventana = medio.get("ventana_dias", 2)
        query = quote(f"{medio['query']} when:{ventana}d")
        url = GOOGLE_NEWS_RSS.format(query=query)
        parsed = parsear_feed_con_reintentos(url)
        return _items_desde_parsed(parsed, f"medios-{medio['id']}", fuente_fallback=None)

    parsed = parsear_feed_con_reintentos(medio["rss"])
    return _items_desde_parsed(parsed, f"medios-{medio['id']}", fuente_fallback=medio["nombre"])


def item_backlog_desde_medio(item: dict, topicos_matcheados: list[str], lugares_matcheados: list[str]) -> dict:
    return {
        "id": item["id"],
        "fuente": item["fuente"],
        "titulo": item["titulo"],
        "fecha": item["fecha"],
        "link": item["link"],
        "texto_original": item["texto"],
        "imagen_url": "",
        "estado": "pendiente",
        "agregado_el": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "procesado_el": None,
        "wp_edit_url": None,
        "motivo_descarte": None,
        "topicos_matcheados": topicos_matcheados,
        "lugares_matcheados": lugares_matcheados,
    }


def main() -> None:
    medios = [m for m in cargar_medios() if m.get("rss") or m.get("tipo") == "google_news"]
    if not medios:
        print("Ningun medio en data/fuentes_medios.json tiene RSS o busqueda configurada todavia -- nada que hacer.")
        return

    topicos = cargar_topicos()
    lugares = cargar_lugares()
    backlog = cargar_backlog()
    ids_existentes = {item.get("id") for item in backlog}
    nuevos = []
    filtrados_topico = 0
    filtrados_lugar = 0

    for medio in medios:
        origen = medio.get("query") or urlparse(medio.get("rss", "")).netloc
        print(f"Consultando {medio['nombre']} ({origen}) ...")
        try:
            items = obtener_items_de_medio(medio)
        except (requests.RequestException, RuntimeError) as e:
            print(f"  No se pudo consultar {medio['nombre']}: {e}")
            continue

        for item in items:
            if item["id"] in ids_existentes:
                continue
            ids_existentes.add(item["id"])

            texto_completo = f"{item['titulo']} {item['texto']}"
            topicos_ok = texto_matchea(texto_completo, [p for ps in topicos.values() for p in ps])
            if not topicos_ok:
                loguear_filtrado(item, "sin_topico")
                filtrados_topico += 1
                continue

            lugares_ok = texto_matchea(texto_completo, lugares)
            if not lugares_ok:
                loguear_filtrado(item, "sin_lugar")
                filtrados_lugar += 1
                continue

            # Guardamos el nombre de categoría de tópico (no la palabra
            # suelta) para que quede legible en el panel.
            categorias = [nombre for nombre, palabras in topicos.items() if any(p in texto_completo.lower() for p in palabras)]
            nuevos.append(item_backlog_desde_medio(item, categorias, lugares_ok))

    total_filtrados = filtrados_topico + filtrados_lugar
    if not nuevos and not total_filtrados:
        print("Sin novedades: todo lo consultado ya estaba cargado.")
        return

    if nuevos:
        backlog.extend(nuevos)
        guardar_backlog(backlog)

    print(f"\nAgregados {len(nuevos)} item(s) nuevo(s) (macro-pestaña 'Medios'):")
    for item in nuevos:
        print(f"  - [{item['id']}] {item['fuente']}: {item['titulo']} ({', '.join(item['topicos_matcheados'])} | {', '.join(item['lugares_matcheados'])})")
    if total_filtrados:
        print(f"\nFiltrados {filtrados_topico} sin tópico + {filtrados_lugar} sin lugar -- ver {LOG_FILTRO_PATH.name}.")
    if nuevos:
        print("\nQuedaron en estado 'pendiente' -- revisalos en admin/index.html.")


if __name__ == "__main__":
    main()
