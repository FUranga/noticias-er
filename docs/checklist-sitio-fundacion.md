# Checklist — sitio de FUNDER (desarrolloentrerriano.org)

Documento vivo para ir tildando a medida que se completa. No todo es urgente — está agrupado por qué tan bloqueante es.

## 1. Pie de página (footer) — lo más visible que falta

- [x] **Redes sociales**: íconos con link a Facebook (`facebook.com/desarrolloentrerriano`), Instagram (`@funder_ok`), X/Twitter (`@FunderRU`), YouTube (`@FunderOrg-ER`). Cargados en el footer (Kadence `footer_social_items` + `{id}_link` theme mods).
- [x] **Dirección física**: 25 de Mayo 46, Paraná, Entre Ríos — agregada al footer (junto al copyright, en `footer_html_content`).
- [x] **Teléfono y email**: (0343) 4230844 / funderru@gmail.com — agregados al footer. **Pendiente**: confirmar que sigan vigentes, son de un snapshot de 2019.
- [ ] **CUIT / datos legales de la Fundación** — si corresponde mostrarlo públicamente (común en fundaciones argentinas, genera confianza institucional).
- [ ] **Copyright** — ya está ("© 2026 Fundación para el Desarrollo Entrerriano"), sin el crédito de Kadence.
- [ ] **Link a Política de Privacidad** — ver punto 3.

## 2. Contenido que falta o hay que revisar

- [ ] **Autoridades actuales** — la lista publicada es de 2019, marcada como desactualizada. Necesito que me pases quién integra el Consejo de Administración hoy.
- [ ] **Confirmar datos de contacto vigentes** (teléfono, email, dirección).
- [ ] **Año de fundación de FUNDER**: confirmado que es 1992 (no 1990 — eso era la fecha de la APF).
- [ ] **"¿Qué es el CEN?"** (Centro de Estudios Nacionales) — no se pudo recuperar el contenido original, hay que rehacerlo si se quiere esa sección.
- [ ] **Página "Informes"** — hoy es un placeholder ("Próximamente"). Definir si van a subir informes/publicaciones ahí y en qué formato (PDF descargable, notas largas, etc.).
- [ ] **Filtrar/curar las 54 notas históricas + 20 de Visión Desarrollista** que importamos — quedaron todas publicadas de una, vale la pena que las repases con calma en algún momento (no es urgente, ya están online).
- [x] **Categorización de los 81 posts** — pasada heurística automática (`categorizar.py`) asignando Opinión/Evento/Informe/Entrevista/Institucional por patrones de título y autor. **Pendiente**: revisión manual, ~44 posts cayeron en el catch-all "Institucional" por defecto.

## 3. Legal / cumplimiento — bajo pero real

- [ ] **Política de Privacidad** — hay un borrador default de WordPress en inglés sin publicar (`Privacy Policy`, id 3). Traducirla y adaptarla, o escribir una propia.
- [ ] **Aviso de cookies** — si usan Google Analytics u otro trackeo, corresponde un banner de consentimiento (Argentina tiene su propia ley de protección de datos personales, Ley 25.326).
- [ ] **Términos de uso** — opcional para un sitio institucional chico, pero prolijo tenerlo.

## 4. Técnico / infraestructura

- [ ] **Certificado SSL (https)** — confirmar que Hostinger ya lo activó automáticamente (normalmente sí, pero vale la pena chequear que no haya contenido mixto/warnings).
- [ ] **Backups automáticos** — confirmar que el plan de Hostinger los tenga habilitados.
- [ ] **Idioma del sitio** — ya corregido a español genérico (`es_ES`), resolvió los textos en inglés del theme.
- [ ] **Google Search Console** — dar de alta el sitio para que aparezca bien indexado en Google (gratis, 10 minutos).
- [ ] **Google Analytics (o similar)** — para saber cuánta gente visita, qué páginas leen. Opcional pero recomendable.
- [ ] **Sitemap.xml** — Kadence/plugins de SEO suelen generarlo solos, confirmar que exista (`/sitemap.xml` o similar) y esté enviado a Search Console.
- [ ] **Favicon** — ya está (el logo de FUNDER).

## 5. Diseño / UX — pulido final

- [x] Logo del theme configurado.
- [x] Fondos grises eliminados.
- [x] Sombras en las tarjetas de artículo eliminadas (`article, .entry, .content-bg, .wp-block-post { box-shadow: none !important; }` en Additional CSS).
- [x] Menú con submenú "Sobre".
- [x] Sección de Novedades dinámica en la portada + archivo completo paginado (9 posts por página).
- [x] Categorías visibles: Opinión, Evento, Informe, Entrevista, Institucional.
- [ ] **Revisar cómo se ve en celular** (mobile) — todo lo armamos mirando desktop, vale la pena chequear el menú, las tarjetas de Novedades y las fotos en una pantalla chica.
- [ ] **Página 404** (cuando alguien entra a un link roto) — Kadence trae una por defecto, confirmar que no diga cosas en inglés.

## 6. Más adelante (no bloqueante para lanzar)

- [ ] Newsletter / lista de correo (si quieren capturar contactos interesados).
- [ ] Sección de transparencia/financiamiento (común en fundaciones serias — quién las financia, balance anual si corresponde).
- [ ] Formulario de contacto real (hoy `/contacto/` es texto estático, no un formulario que envíe mail).

---

Metele por donde quieras — no hay un orden obligatorio salvo que yo marcaría **footer (sección 1)** y **autoridades/contacto actualizados (sección 2)** como lo más visible/urgente, y lo legal (sección 3) como lo segundo más importante aunque no se note tanto.
