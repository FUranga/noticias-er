# data/energia/

Series de datos del cuadro tarifario eléctrico provincial (EPRE), separado de `data/backlog.json` porque es un dato de referencia, no una noticia — ver `docs/servicios-publicos-tarifas.md` ("Qué buscar al triagear un ítem del EPRE") para el criterio de por qué los cuadros mensuales se descartan como nota individual pero se guardan acá.

- **`cuadro-tarifario-epre.xlsx`** — Tarifa 1 (Pequeñas Demandas) residencial, mes a mes, mayo a octubre 2026. La hoja "Metodología" adentro del archivo documenta la fuente, qué se cubrió, qué no, y dos celdas marcadas explícitamente "NO CONFIRMADO" (septiembre 2026, grupo "Con Subsidio Provincial y Nacional") que necesitan verificación manual contra el anexo oficial antes de usarse en una nota.

No repetir la metodología acá — está completa dentro del propio Excel, mismo criterio que `data/series/exportaciones-sbc.json`.
