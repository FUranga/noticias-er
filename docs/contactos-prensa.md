# Contactos de prensa para suscripción a listas de comunicados

Lista de trabajo para que Francisco se inscriba en listas de prensa desde la casilla de email dedicada del medio (ver `docs/arquitectura-tecnica.md`, sección "Estrategia de ingesta de comunicados" — Etapa 1). Cada entrada indica si el contacto de prensa está confirmado o no; **no se completó ningún email adivinado** — donde no hay contacto confirmado, se indica el canal alternativo (formulario, redes) o "no confirmado, revisar manualmente".

Fuente de cada organización: `docs/fuentes.md`. Actualizar ambos archivos en paralelo si se confirma o corrige un contacto.

## Gobierno provincial
- **Secretaría de Comunicación y Prensa (Gobierno de Entre Ríos)** — seccomunicacion@entrerios.gov.ar (confirmado por WebFetch en `portal.entrerios.gov.ar/noticias/`, 2026-09-03). Es el contacto centralizado de prensa del gobierno provincial — probablemente el más importante para pedir alta en lista.
- Ministerio de Producción, Turismo y Desarrollo Económico — no confirmado, revisar en `entrerios.gov.ar/minpro/` o a través de la Secretaría de Comunicación general.

## Legislatura de Entre Ríos
- **Cámara de Senadores** — prensa@senadoer.gob.ar (según búsqueda, no verificado por WebFetch directamente).
- Cámara de Diputados — no confirmado, revisar en `hcder.gov.ar` (sección de prensa mencionada en búsqueda pero sin email específico encontrado).

## Municipalidad de Paraná
- No confirmado — el sitio bloquea fetch automatizado (403), revisar manualmente en `parana.gob.ar` (sección de contacto/prensa) o a través de la Secretaría de Producción, Innovación y Empleo.

## Concejo Deliberante de Paraná
- No confirmado — revisar manualmente en `hcdparana.gob.ar`.

## Organizaciones privadas/empresarias
- **CACEPER** (Cámara de Comercio Exterior de ER) — prensa@caceper.com.ar (según búsqueda, no verificado directamente).
- **CAMARCO Entre Ríos** (construcción) — entrerios@camarco.org.ar (según búsqueda).
- **Centro Comercial e Industrial de Paraná** — cciparana@arnetbiz.com.ar (según búsqueda, no verificado directamente).
- UIER, CEER, FEDER, Bolsa de Cereales de Entre Ríos, Sociedad Rural de Paraná — sin email de prensa confirmado en esta pasada. FEDER tiene sección `/prensa/` en su sitio pero no se extrajo un email específico; Bolsa de Cereales ofrece suscripción por WhatsApp, no email.

## Sindicatos
- **ATE Entre Ríos** — ate@ateentrerios.org.ar (según búsqueda).
- **ATSA Entre Ríos** (sanidad) — atsaentrerios@gmail.com (confirmado por WebFetch).
- **UOCRA Seccional Paraná** — sine280@uocra.org (según búsqueda).
- **Sindicato de Empleados de Comercio de Gualeguaychú** (excepción, no es de Paraná) — contacto@secgchu.org.ar (según búsqueda).
- AGMER, UPCN Entre Ríos, Sindicato de Comercio de Paraná, UOM Paraná, AGDU, SADOP Entre Ríos, CGT Regional Paraná, CTA Entre Ríos — sin email de prensa confirmado en esta pasada; varios tienen formulario de contacto o solo redes sociales, revisar sitio por sitio.

## ONGs e instituciones académicas
- No confirmado — UNER y UADER no fueron auditadas para contacto de prensa específico en esta pasada.

## Próximos pasos de este archivo
- Completar los "no confirmado" a medida que se audite cada sitio (usar la skill `mapear-fuentes` o revisión manual).
- Cuando Francisco tenga la casilla de email lista, usar esta lista como base para las suscripciones — empezando por Secretaría de Comunicación y Prensa provincial (mayor volumen esperado) y Cámara de Senadores.
- Si alguna organización no tiene lista de mail formal, considerarla candidata para la Etapa 3/4 de ingesta (RSS o scraping) en vez de email — ver `docs/arquitectura-tecnica.md`.
