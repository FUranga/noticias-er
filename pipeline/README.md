# Pipeline de publicación

Script chico que toma una noticia ya redactada (la salida de la skill `redactar-noticia`) y la sube a WordPress como borrador (`draft`), lista para que el editor la revise y publique desde el editor nativo de WordPress. Ver `docs/arquitectura-tecnica.md` para el contexto completo del pipeline de agencia.

## 1. Generar la Application Password en WordPress (una sola vez)

1. Entrá a tu WordPress como admin → **Usuarios → Tu perfil**.
2. Bajá hasta la sección **Application Passwords**.
3. Ponele un nombre (ej. `pipeline-agencia`) y generá.
4. Copiá la clave que te muestra (formato `xxxx xxxx xxxx xxxx xxxx xxxx`) — solo se muestra una vez.

Esta clave NO es tu contraseña normal — es una credencial separada, solo para esta integración, que podés revocar en cualquier momento sin afectar tu login.

## 2. Configurar el script (una sola vez)

```
cd pipeline
copy .env.example .env      # (en PowerShell: Copy-Item .env.example .env)
```

Editá `.env` y completá:
- `WP_URL`: la URL de tu WordPress (sin barra al final).
- `WP_USER`: tu usuario de WordPress.
- `WP_APP_PASSWORD`: la clave que generaste en el paso 1.

Instalá las dependencias (una sola vez, requiere Python):
```
pip install -r requirements.txt
```

## 3. Uso normal

1. Pegás un comunicado en la skill `redactar-noticia` (Claude Code) y te devuelve el borrador en este formato:
   ```
   Título: ...

   Bajada: ...

   [Cuerpo en párrafos cortos]

   Fuente: ...
   ```
2. Guardás esa salida en un archivo de texto (ej. `nota.txt`).
3. Corrés:
   ```
   python publicar_borrador.py nota.txt
   ```
4. El script te devuelve el link directo para revisar el borrador en el editor de WordPress. Ahí editás y publicás cuando estés conforme — el script nunca publica solo, siempre crea el post en estado `draft`.

## Notas

- `.env` nunca se commitea (está en `.gitignore`). Si la Application Password se filtra, revocala desde WordPress (Usuarios → Tu perfil → Application Passwords → Revoke) y generá una nueva.
- Este script es intencionalmente simple (un archivo de texto por nota, ejecución manual) — automatizar la ingesta de comunicados (RSS, scraping) es un paso posterior, no parte de esta primera versión.
