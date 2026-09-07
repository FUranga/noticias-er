# Agenda

Registro de hechos futuros con fecha (o "próxima sesión/reunión" sin fecha exacta) que aparecen mencionados dentro de un comunicado — no son noticia en sí mismos, pero son algo concreto que va a pasar o que queda pendiente de resolución.

Distinto de `docs/temas-a-seguir.md` (pistas sueltas, sin fecha, que podrían convertirse en una investigación) y distinto de `data/backlog.json` (comunicados ya recibidos, con estado editorial de noticiabilidad). Acá no hay decisión editorial de por medio — se guarda **todo** lo que aparezca con una fecha o un "próximo paso" concreto, se haya convertido el comunicado en nota o no.

## Para qué sirve (2026-09-04, definido por Francisco)

Dos razones, una decidida y otra en evaluación:
1. **Uso propio de Francisco, ya**: tener a mano qué va a pasar y cuándo, para no perderlo de vista — por ejemplo al armar un newsletter a futuro, o para volver a chequear un trámite legislativo que quedó abierto.
2. **Posible sección pública de agenda** (legislativa u otra) — todavía sin decidir si se implementa ni cómo. No construir la sección todavía; solo juntar los datos para no tener que reconstruir el historial cuando se decida.

**Conexión con un futuro newsletter** (2026-09-04): cuando se piense el formato de newsletter (ver `docs/vision-y-etapas.md`, Etapa 1), probablemente valga la pena incluir fechas clave/de servicio (vencimientos, plazos) además de los hechos noticiosos — por eso `tipo: "plazo"` no se limita a lo legislativo, también entra ahí un vencimiento impositivo (ver ejemplo de ATER más abajo) u otro dato de servicio, aunque nunca se haya convertido en nota propia. Es bueno tener las fechas clave registradas incluso si al final no se usan.

**Cargar la agenda a tiempo, no después del hecho (2026-09-07, idea de Francisco)**: el valor real de una convocatoria a audiencia pública (ej. EPRE) está en enganchar la fecha *antes* de que pase, no en registrarla en retrospectiva junto con la cobertura del hecho ya ocurrido — para entonces ya no sirve como agenda, solo como archivo. Esto tiene una implicancia editorial además de la de registro: si se detecta a tiempo, vale la pena pensar **difundirlo activamente hacia la comunidad afectada** (ej. avisar en Federación/Chajarí sobre una audiencia del EPRE en su zona), no solo guardarlo para uso propio — un servicio de utilidad concreta, no solo cobertura. Todavía no se construyó ningún mecanismo para esto (ni de detección proactiva de convocatorias futuras, ni de difusión dirigida); es la versión más concreta hasta ahora de la "posible sección pública de agenda" mencionada arriba. Encaja con `docs/servicios-publicos-tarifas.md` (agenda de audiencias del EPRE) y con la lógica de `docs/vision-y-etapas.md`.

## Cómo se usa

Dos caminos, complementarios — no son alternativos, cada uno cubre un caso distinto:

1. **Automático, al evaluar un comunicado** (skill `evaluar-comunicado`, o al redactarlo con `redactar-noticia`/`procesar-cablera`): si aparece una fecha futura concreta o un "próximo paso" identificable *dentro* de un comunicado que trata sobre otra cosa (ej. un comunicado de aniversario que de paso menciona que los festejos siguen hasta tal fecha), se agrega igual — Francisco nunca marcaría el ítem entero como "esto es agenda", pero el dato vale la pena guardarlo. Independiente de si el comunicado en sí pasa el filtro de noticiabilidad.
2. **Manual, desde `admin/index.html`**: cuando el comunicado **es directamente** un anuncio de agenda (ej. "la próxima audiencia pública es tal día"), Francisco lo marca ahí mismo con el botón "Agregar a agenda" de cada ítem — sin esperar a que corra una sesión de Claude Code. El panel completa `origen_id`, `fuente` y `agregado_el` automáticamente; pide `evento`, `fecha` (opcional), `fuente` (editable), `tipo` y `detalle` en un diálogo corto. Disponible para un ítem en cualquier estado de la cablera (los 4 estados son los mismos para toda fuente, ver `docs/boletin-oficial-proceso.md`) — la decisión de agenda es independiente de la decisión de noticiabilidad. El panel muestra un badge "en agenda" si el ítem ya tiene al menos una entrada.
3. **Manual, sin ítem de origen (2026-09-07)**: la macro-pestaña **"Agenda"** del panel (junto a "Cablera" y "Boletín Oficial") lista todo `data/agenda.json`, con sus propios sub-estados (`pendiente` ["A cubrir"] / `cubierto` / `descartado`) y un botón "+ Agregar evento" para cargar algo que no vino de ningún comunicado puntual — ej. una fecha que Francisco supo por otro medio. En ese caso `origen_id` queda `null` y `fuente` se completa a mano. Marcar "cubierto" pide opcionalmente el link/referencia de la nota que lo cubrió; "Descartar" pide opcionalmente el motivo — ambos se agregan a `detalle`.
4. **Vista "Próximas 2 semanas" (2026-09-07)**: NO es una pestaña de estado más (eso confundía "en qué estado está" con "cómo lo estoy mirando") — es un botón toggle que aparece solo dentro de la pestaña "A cubrir", activado por defecto. Agrupa por día los ítems con `fecha` entre hoy y los próximos 13 días, saltando los días sin nada; "Ver lista completa" vuelve a la lista plana de siempre (incluye los sin fecha exacta y los ya vencidos). Reemplazó al viejo estado manual `vencido_sin_seguimiento` (había que acordarse de tocar un botón para declarar que algo se venció, y en la práctica nunca se usaba) — ahora cualquier ítem `pendiente` cuya `fecha` ya pasó se marca solo con un badge "vencida" en la lista de "A cubrir", sin que nadie tenga que declarar nada a mano.

## Esquema de cada ítem (`data/agenda.json`)

```json
{
  "id": "slug-corto-descriptivo",
  "fecha": "2026-09-09",
  "evento": "Descripción corta del hecho futuro",
  "tipo": "evento | sesión legislativa | trámite en comisión | plazo",
  "fuente": "Organismo que lo informó",
  "origen_id": "id del ítem en data/backlog.json de donde salió (o null)",
  "detalle": "Contexto breve, una o dos oraciones",
  "agregado_el": "2026-09-04T00:00:00Z",
  "estado": "pendiente | cubierto | vencido_sin_seguimiento"
}
```

- `fecha`: `null` si es un "próximo paso" sin fecha exacta (ej. "próxima sesión", "en próximas reuniones") — igual vale la pena guardarlo.
- `estado`: arranca en `pendiente` (se muestra como "A cubrir" en el panel). Pasa a `cubierto` si terminó saliendo una nota sobre eso (con `origen_id` o un link agregado en `detalle`), o a `descartado` si el editor decide explícitamente dejar de seguirlo (con motivo opcional en `detalle`) — no borrar, sirve como historial. Que la `fecha` ya haya pasado sin que nada de esto ocurra NO es un estado aparte: el panel lo marca solo con un badge "vencida" mientras siga en `pendiente`, sin que haga falta declarar nada a mano.

## Ítems

*(se completa a medida que aparecen en comunicados — ver historial de commits para el detalle de cuándo se agregó cada uno)*
