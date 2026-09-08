r"""
Utilidad compartida para parsear feeds RSS/Atom con reintentos.

Motivo (incidente 2026-09-07 y recurrencia 2026-09-08): un feed de
WordPress puede devolver XML a medio regenerar -- un hipo de un segundo del
lado del servidor, no una caida real -- y `feedparser` lo marca como
invalido y sin entradas. Sin reintento, ese hipo tira todo el job de
GitHub Actions aunque el feed este perfectamente sano un segundo despues
(confirmado a mano: mismo feed, mismo minuto, XML valido en el reintento
manual). Reintentar antes de darse por vencido evita perder una corrida
entera por eso.
"""

import time

import feedparser


def parsear_feed_con_reintentos(url: str, *, agent: str = "Mozilla/5.0", intentos: int = 3, espera_base: int = 3):
    """Parsea `url` con feedparser, reintentando si da bozo sin entradas.

    Espera `espera_base * intento` segundos entre reintentos (backoff
    simple). Si despues de `intentos` intentos sigue sin entradas validas,
    levanta RuntimeError con el ultimo error visto.
    """
    ultimo_error = None
    for intento in range(1, intentos + 1):
        parsed = feedparser.parse(url, agent=agent)
        if not (parsed.bozo and not parsed.entries):
            return parsed
        ultimo_error = parsed.get("bozo_exception")
        if intento < intentos:
            time.sleep(espera_base * intento)
    raise RuntimeError(f"Feed invalido y sin entradas tras {intentos} intento(s): {ultimo_error}")
