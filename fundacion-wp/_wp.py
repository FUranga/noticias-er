# -*- coding: utf-8 -*-
"""Config compartida por los scripts de fundacion-wp/. Importar WP_URL y AUTH desde acá."""
import os
from dotenv import load_dotenv

load_dotenv()

WP_URL = os.environ["FUNDER_WP_URL"]
AUTH = (os.environ["FUNDER_WP_USER"], os.environ["FUNDER_WP_APP_PASSWORD"])
