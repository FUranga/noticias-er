# Calendario de publicaciones periódicas

Insumo para pasar de monitoreo puramente reactivo (esperar que un comunicado llegue) a uno también proactivo (saber de antemano cuándo sale algo). Complementa `docs/fuentes.md` (dónde está cada fuente) — esto es **cuándo** revisarla. Pensado para alimentar, más adelante, un sistema de alertas o simplemente un recordatorio manual antes de armar el newsletter (ver `docs/vision-y-etapas.md`, Etapa 1).

Se ordena por periodicidad, no por organismo, para que sea más fácil convertirlo en cronograma operativo.

## Diario / semanal

| Qué | Organismo | Frecuencia |
|---|---|---|
| Boletín Oficial de la Nación | Nacional | Diario hábil — **implementado 2026-09-07**: `pipeline/monitorear_boletin_nacional.py` filtra solo lo que menciona "Entre Ríos" o "Salto Grande" (ver `docs/fuentes.md`, entrada BORA) |
| Boletín Oficial de Entre Ríos (Mi Entre Ríos) | Provincial | **Corregido 2026-09-06**: el índice de ediciones muestra publicación en días hábiles consecutivos (no semanal como se creía) — ver `docs/boletin-oficial-proceso.md`. Un dato de `Last-Modified` sugiere publicación ~13:24 hora Argentina. |
| Boletín Oficial Digital Municipal de Paraná | Municipal | Según publicación (más reciente que el provincial) |
| Transferencias de coparticipación a provincias | Ministerio de Economía / Nación | Automáticas a diario, informe consolidado mensual |

## Mensual

| Qué | Organismo | Cuándo |
|---|---|---|
| Índice de Precios al Consumidor (IPC) | INDEC | Mediados de cada mes, sobre el mes anterior |
| Canasta Básica Alimentaria y Total (nacional) | INDEC | Junto con el IPC |
| Canasta Básica Alimentaria y Total de Paraná (propia) | DGEC Entre Ríos | Mensual |
| Dotación de personal de la administración pública nacional | INDEC | Mensual |
| Índices de producción industrial (manufacturero, minero, pesquero) | INDEC | Mensual |
| Informe consolidado de coparticipación girada por provincia | Ministerio de Economía / Secretaría de Hacienda | Mensual, días posteriores al cierre del mes |
| Escala salarial de empleados municipales de Paraná | Municipalidad de Paraná (datos.parana.gob.ar) | Mensual |

## Trimestral

| Qué | Organismo | Cuándo |
|---|---|---|
| Mercado de trabajo — tasas e indicadores (EPH), Gran Paraná y Concordia | INDEC | ~45 días después de cerrado el trimestre |
| Evolución de la distribución del ingreso (EPH) | INDEC | Ídem |
| Índices de precios y cantidades del comercio exterior | INDEC | Trimestral |
| Ejecución presupuestaria nacional por jurisdicción | presupuestoabierto.gob.ar | Trimestral |

## Semestral

| Qué | Organismo | Cuándo |
|---|---|---|
| Incidencia de la pobreza e indigencia en 31 aglomerados (incluye Gran Paraná y Concordia) | INDEC | Fines de marzo (2° semestre anterior) y fines de septiembre (1° semestre) |
| Calendario de difusión completo del semestre siguiente | INDEC | indec.gob.ar/indec/web/Calendario-Fecha-0, publicado con antelación |

## Anual, con fecha fija o cuasi-fija

| Qué | Organismo | Fecha |
|---|---|---|
| Apertura de sesiones ordinarias del Congreso de la Nación | Nacional | 1° de marzo |
| Apertura de sesiones ordinarias de la Legislatura de Entre Ríos | Provincial | 15 de febrero (se corre a día hábil si cae fin de semana/feriado) |
| Listado de juicios en trámite del Estado provincial | Fiscalía de Estado ER | 31 de marzo (al Gobernador y la Legislatura) |
| Rendición de cuentas anual de municipios (memoria, ejecución presupuestaria, deuda) | Municipios de ER, incl. Paraná | Antes del 30 de abril (Ley Orgánica de Municipios 10.027) |
| Memoria Anual y Cuenta General del Ejercicio Presupuestario | Tribunal de Cuentas de Entre Ríos | Sin fecha fija — tcer.gob.ar/novedades.html, típicamente con 1-2 años de rezago |
| Presupuesto municipal de Paraná (aprobación) | HCD Paraná | Fin de año calendario (para el ejercicio siguiente) |
| Plan Anual de Acción de Auditoría (POA/PAA) | AGN | Aprobado en febrero de cada año |
| Censo Nacional (próximo: 2032) | INDEC | Cada 10 años (último: 2022) |

## Sin periodicidad fija pero "vigilables" (alertar cuando aparecen)

- Informes de auditoría especial del TCER (ej. IOSPER) — sin cronograma anunciado, monitorear la web.
- Resoluciones del Colegio de Auditores Generales de la AGN que mencionen Entre Ríos — el buscador público se actualiza sin calendario fijo; conviene un scraping periódico con palabras clave ("Entre Ríos", "Paraná", "Salto Grande", nombres de municipios).
- Fallos de la CSJN o de la Cámara Federal de Paraná en causas de relevancia pública.
- Convocatorias a concurso del Consejo de la Magistratura (nacional y provincial) para cargos con asiento en la provincia.

## Sugerencia operativa

El calendario más denso y confiable es el de INDEC (publica su propio cronograma semestral con antelación, algo que ningún organismo provincial hace) — tomarlo como columna vertebral de cualquier sistema de alertas y superponerle los hitos fijos provinciales/municipales (30/4, 15/2, 31/3), dejando un canal aparte de "vigilancia sin fecha" para AGN, TCER y Poder Judicial.

**Mecanismo de ingesta todavía no resuelto**: ninguna de las fuentes de esta tabla tiene RSS confirmado — la mayoría publica en PDF o HTML tabulado. Ver `docs/arquitectura-tecnica.md` (sección "Estrategia de ingesta de comunicados") para cómo encaja esto en las etapas de automatización ya definidas.
