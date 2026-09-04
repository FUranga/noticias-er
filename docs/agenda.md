# Agenda

Registro de hechos futuros con fecha (o "próxima sesión/reunión" sin fecha exacta) que aparecen mencionados dentro de un comunicado — no son noticia en sí mismos, pero son algo concreto que va a pasar o que queda pendiente de resolución.

Distinto de `docs/temas-a-seguir.md` (pistas sueltas, sin fecha, que podrían convertirse en una investigación) y distinto de `data/backlog.json` (comunicados ya recibidos, con estado editorial de noticiabilidad). Acá no hay decisión editorial de por medio — se guarda **todo** lo que aparezca con una fecha o un "próximo paso" concreto, se haya convertido el comunicado en nota o no.

## Para qué sirve (2026-09-04, definido por Francisco)

Dos razones, una decidida y otra en evaluación:
1. **Uso propio de Francisco, ya**: tener a mano qué va a pasar y cuándo, para no perderlo de vista — por ejemplo al armar un newsletter a futuro, o para volver a chequear un trámite legislativo que quedó abierto.
2. **Posible sección pública de agenda** (legislativa u otra) — todavía sin decidir si se implementa ni cómo. No construir la sección todavía; solo juntar los datos para no tener que reconstruir el historial cuando se decida.

**Conexión con un futuro newsletter** (2026-09-04): cuando se piense el formato de newsletter (ver `docs/vision-y-etapas.md`, Etapa 1), probablemente valga la pena incluir fechas clave/de servicio (vencimientos, plazos) además de los hechos noticiosos — por eso `tipo: "plazo"` no se limita a lo legislativo, también entra ahí un vencimiento impositivo (ver ejemplo de ATER más abajo) u otro dato de servicio, aunque nunca se haya convertido en nota propia. Es bueno tener las fechas clave registradas incluso si al final no se usan.

## Cómo se usa

Dos caminos, complementarios — no son alternativos, cada uno cubre un caso distinto:

1. **Automático, al evaluar un comunicado** (skill `evaluar-comunicado`, o al redactarlo con `redactar-noticia`/`procesar-cablera`): si aparece una fecha futura concreta o un "próximo paso" identificable *dentro* de un comunicado que trata sobre otra cosa (ej. un comunicado de aniversario que de paso menciona que los festejos siguen hasta tal fecha), se agrega igual — Francisco nunca marcaría el ítem entero como "esto es agenda", pero el dato vale la pena guardarlo. Independiente de si el comunicado en sí pasa el filtro de noticiabilidad.
2. **Manual, desde `admin/index.html`**: cuando el comunicado **es directamente** un anuncio de agenda (ej. "la próxima audiencia pública es tal día"), Francisco lo marca ahí mismo con el botón "Agregar a agenda" de cada ítem — sin esperar a que corra una sesión de Claude Code. El panel completa `origen_id`, `fuente` y `agregado_el` automáticamente; pide `evento`, `fecha` (opcional), `tipo` y `detalle` en un diálogo corto. Disponible para un ítem en cualquier estado de la cablera (`pendiente`, `a_publicar`, `descartado`, `procesado`) — la decisión de agenda es independiente de la decisión de noticiabilidad. El panel muestra un badge "en agenda" si el ítem ya tiene al menos una entrada.

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
- `estado`: arranca en `pendiente`. Pasa a `cubierto` si terminó saliendo una nota sobre eso (con `origen_id` o un link agregado en `detalle`), o `vencido_sin_seguimiento` si la fecha ya pasó y no se hizo nada — no borrar, sirve como historial de qué se dejó pasar.

## Ítems

*(se completa a medida que aparecen en comunicados — ver historial de commits para el detalle de cuándo se agregó cada uno)*
