# Prensa de FUNDER — gacetillas y contactos de medios

Documento de referencia para la skill `armar-gacetilla` y para cuando se resuelva el envío a
periodistas. Esto es distinto del flujo editorial del medio (`skills/redactar-noticia`, etc.): acá
FUNDER es quien emite el comunicado, no quien lo recibe.

## Contacto de prensa por defecto

Salvo que el editor indique lo contrario para un envío puntual, toda gacetilla de FUNDER lleva:

- **Nicolás Loza**, Coordinador de FUNDER
- Tel: **3434054369**
- Email: **funderru@gmail.com**

## Embargo

Toda gacetilla pregunta explícitamente si el contenido está embargado:
- Sin embargo → encabezado "PARA DIFUSIÓN INMEDIATA".
- Con embargo → encabezado "EMBARGADO HASTA [fecha y hora exacta indicada por el editor]" — la fecha
  nunca se asume, la tiene que dar el editor.

## Listado de periodistas — pendiente

El editor va a pasar un listado de medios/periodistas de Entre Ríos para poder enviar las gacetillas.
Cuando lo pase:
- Guardarlo acá o en un archivo estructurado aparte (a definir cuando llegue el primer listado real —
  probablemente algo tipo `docs/medios-entre-rios.json` o una tabla en este mismo documento, según
  cuántos contactos y qué datos traiga cada uno).
- El editor va a pedir, más adelante y por separado, una **auditoría y actualización** de ese listado
  (confirmar que los contactos/medios sigan vigentes, que los mails no reboten, etc.) — no adelantarse
  a hacer esa auditoría antes de que el editor la pida ni de tener el listado real en mano.

## Envío — no implementado todavía

Falta definir el mecanismo real de envío (mail merge manual, un ESP tipo Mailchimp/Brevo, Gmail con
BCC, etc.). Hasta que esté decidido, `armar-gacetilla` solo entrega el texto listo — el envío lo hace
el editor a mano. Cuando se implemente el envío automatizado, sigue aplicando la regla general del
proyecto: nada se manda sin que el editor lo revise y apruebe explícitamente antes de cada envío (no
alcanza con una aprobación genérica de "podés mandar gacetillas" — cada envío puntual se confirma).
