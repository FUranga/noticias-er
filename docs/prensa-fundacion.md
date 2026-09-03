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

## Plan a futuro: envío automatizado por mail (planteado, no implementado)

El editor preguntó si se podía armar para que el envío del mail sea directo (no copiar/pegar a mano) —
queda anotado acá como el plan para cuando el listado de periodistas esté cargado y auditado, pero
**no se implementa hasta que el editor lo pida explícitamente**.

**Opción recomendada: SMTP directo desde `funderru@gmail.com` con una App Password de Gmail**, mismo
patrón que las Application Passwords de WordPress que ya usa este proyecto (`smtplib` de Python, sin
sumar un servicio nuevo). Alcanza de sobra para el volumen de un listado de medios de Entre Ríos.
Límite a tener en cuenta: Gmail normal corta en ~500 destinatarios/día (una gacetilla puntual no se
acerca a eso, pero conviene no mandar en copia oculta a cientos de contactos de una — separar en
tandas si el listado crece mucho).

Alternativa si más adelante hace falta trackear aperturas/clics o crece mucho el volumen: un ESP chico
(Brevo tiene plan gratis con API simple) — más piezas para mantener, se justifica solo si el envío por
Gmail se queda corto.

**Cómo se integraría con `armar-gacetilla`:**
1. La skill arma el texto de la gacetilla (ya implementado).
2. Un paso nuevo arma el mail (asunto = título de la gacetilla, cuerpo = el texto ya armado) y muestra
   al editor **a quién se le mandaría** (la lista completa de destinatarios, no solo un conteo) antes
   de mandar nada.
3. El editor confirma explícitamente ese envío puntual. Recién ahí se dispara el `smtplib.send_message`
   con las credenciales de `funderru@gmail.com` guardadas en `fundacion-wp/.env` (mismo patrón que
   `FUNDER_WP_APP_PASSWORD`).
4. Nunca hay un modo "mandalo siempre que armes una gacetilla" — cada tanda de envío es una acción que
   se confirma en el momento, igual que cualquier otro envío de mensajes en nombre del usuario.

Para armar esto en serio hace falta primero: (a) el listado real de periodistas con emails
verificados, y (b) que el editor decida explícitamente activar esta funcionalidad.
