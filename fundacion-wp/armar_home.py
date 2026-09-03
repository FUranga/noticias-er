# -*- coding: utf-8 -*-
"""Genera y publica el HTML completo de la portada (pagina 'Inicio', id 55) de desarrolloentrerriano.org.
Es la fuente de verdad del markup actual de la home: hero con foto de Casa de Gobierno,
bajada institucional, links a Quienes somos/Contacto, y el bloque de Novedades (Query Loop nativo de WP).
Volver a correr este script sobreescribe la home con exactamente este contenido.
"""
from _wp import WP_URL, AUTH
import requests

IMG = {
    "logo": f"{WP_URL}/wp-content/uploads/2026/09/logo-funder.png",
    "raul": f"{WP_URL}/wp-content/uploads/2026/09/raul-uranga.png",
    "lucio": f"{WP_URL}/wp-content/uploads/2026/09/Lucio-Isidro-Uranga-225x300-1.jpg",
    "biblioteca": f"{WP_URL}/wp-content/uploads/2026/09/biblioteca-mario-domingo.jpg",
    "palacio": f"{WP_URL}/wp-content/uploads/2026/09/Palacio_Municipal_de_Parana-620x330-1.jpg",
    "tunel": f"{WP_URL}/wp-content/uploads/2026/09/firma-tunel.jpg",
}

# Paleta fiel a la identidad vieja de FUNDER: rojo/negro/blanco, plano (sin degrade)
ROJO = "#B4192B"
NEGRO = "#111111"
TEXT = "#1c1c1c"
MUTED = "#5a5a5a"
BG_ALT = "#f4f4f2"
SERIF = "Georgia, 'Times New Roman', Times, serif"
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

HOME_ID = 55


def novedades_block():
    """Bloque nativo de WordPress (Query Loop) - de verdad dinamico, se actualiza solo."""
    return f"""
  <div style="background:#fff; padding:56px 24px;">
    <div style="max-width:1040px; margin:0 auto;">
      <div style="display:flex; align-items:center; gap:12px; margin-bottom:30px;">
        <div style="background:{ROJO}; color:#fff; font-family:{SANS}; font-size:13px; letter-spacing:1px; text-transform:uppercase; font-weight:700; padding:8px 16px;">Novedades FUNDER</div>
        <div style="flex:1; height:1px; background:#ddd;"></div>
      </div>

<!-- wp:query {{"queryId":1,"query":{{"perPage":6,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","author":"","search":"","exclude":[],"sticky":"","inherit":false}},"displayLayout":{{"type":"flex","columns":3}}}} -->
<div class="wp-block-query">
<!-- wp:post-template -->
<!-- wp:post-featured-image {{"isLink":true,"height":"160px"}} /-->
<!-- wp:post-date {{"format":"d/m/Y"}} /-->
<!-- wp:post-title {{"isLink":true,"level":3}} /-->
<!-- /wp:post-template -->
</div>
<!-- /wp:query -->

      <div style="text-align:center; margin-top:36px;">
        <a href="{WP_URL}/novedades/" style="font-family:{SANS}; font-size:14px; color:{ROJO}; text-decoration:none; font-weight:600; border-bottom:1px solid {ROJO}; padding-bottom:2px;">Ver m&aacute;s &rarr;</a>
      </div>

    </div>
  </div>"""


def main():
    html = f"""
<style>.entry-hero.page-hero-section {{ display:none !important; }}</style>
<div style="margin:-1px 0 0; background:#fff;">
  <img src="{WP_URL}/wp-content/uploads/2026/09/casa-gobierno-entre-rios.jpg" alt="Casa de Gobierno de Entre R&iacute;os" title="Foto: Agustingagliardone / Wikimedia Commons (CC BY-SA 3.0)" style="width:100%; max-height:340px; object-fit:cover; display:block;">
  <div style="max-width:640px; margin:0 auto; text-align:center; padding:56px 24px 56px;">
    <div style="width:46px; height:3px; background:{ROJO}; margin:0 auto 26px;"></div>
    <p style="font-family:{SERIF}; font-size:19px; line-height:1.6; color:{TEXT}; margin:0 0 34px;">
      Debatimos la agenda del desarrollo para Entre R&iacute;os, inspirados en las ideas y la obra de gobierno de Ra&uacute;l Uranga.
    </p>
    <div style="display:flex; gap:28px; justify-content:center; flex-wrap:wrap;">
      <a href="{WP_URL}/quienes-somos/" style="font-family:{SANS}; font-size:14px; color:{ROJO}; text-decoration:none; font-weight:600; border-bottom:1px solid {ROJO}; padding-bottom:2px;">Qui&eacute;nes somos</a>
      <a href="{WP_URL}/contacto/" style="font-family:{SANS}; font-size:14px; color:{ROJO}; text-decoration:none; font-weight:600; border-bottom:1px solid {ROJO}; padding-bottom:2px;">Contacto</a>
    </div>
  </div>
</div>
{novedades_block()}
"""

    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/pages/{HOME_ID}",
        auth=AUTH,
        json={"content": html},
        timeout=30,
    )
    r.raise_for_status()
    page = r.json()
    print(f"Pagina 'Inicio' (id {HOME_ID}) actualizada -> {page['link']}")


if __name__ == "__main__":
    main()
