// Contenido de DEMO/VISUAL, no editorial real -- pensado para mostrar la
// home poblada (pedido de Francisco, 2026-09-07). Ningun dato acá es un
// hecho real: nombres de funcionarios son ficticios o genéricos por cargo,
// nunca atribuidos a una persona real en ejercicio. Borrar este archivo (y
// su uso en `wp.ts`) cuando deje de hacer falta la demo visual.

import type { WpPost } from "./wp";

function post(p: {
  id: number;
  slug: string;
  date: string;
  categoria: string;
  categoriaSlug: string;
  titulo: string;
  bajada: string;
  cuerpo: string[];
  seedFoto: string;
  autor?: string;
}): WpPost {
  return {
    id: p.id,
    slug: p.slug,
    date: p.date,
    sticky: false,
    title: { rendered: p.titulo },
    excerpt: { rendered: `<p>${p.bajada}</p>` },
    content: { rendered: p.cuerpo.map((par) => `<p>${par}</p>`).join("\n") },
    _embedded: {
      "wp:featuredmedia": [
        {
          source_url: `https://picsum.photos/seed/${p.seedFoto}/1200/750`,
          alt_text: "",
          caption: { rendered: `<p>Foto: Agencia Entrerriana (demo)</p>` },
        },
      ],
      author: [{ name: p.autor ?? "Redacción" }],
      "wp:term": [[{ name: p.categoria, slug: p.categoriaSlug, taxonomy: "category" }]],
    },
  };
}

export const mockPosts: WpPost[] = [
  // Política
  post({
    id: -1,
    slug: "legislatura-aprobo-marco-desarrollo-norte-entrerriano",
    date: "2026-09-06T18:20:00",
    categoria: "Política",
    categoriaSlug: "politica",
    titulo: "La Legislatura sancionó el marco de desarrollo para el Norte Entrerriano",
    bajada: "La ley crea un régimen de promoción productiva e institucional para los departamentos del norte de la provincia.",
    cuerpo: [
      "La Cámara de Diputados dio sanción definitiva a la ley que crea un marco institucional de desarrollo para el Norte Entrerriano, después de que el Senado la aprobara a fines de agosto.",
      "El texto habilita beneficios impositivos y líneas de financiamiento específicas para proyectos productivos en la región, con una comisión de seguimiento integrada por legisladores de ambas cámaras.",
      "Todavía resta la promulgación del Poder Ejecutivo para que entre en vigencia.",
    ],
    seedFoto: "norte-er-legislatura",
  }),
  post({
    id: -2,
    slug: "gobierno-provincial-congelo-designaciones-entes-autarquicos",
    date: "2026-09-05T12:00:00",
    categoria: "Política",
    categoriaSlug: "politica",
    titulo: "El gobierno provincial extendió el congelamiento de designaciones en entes autárquicos",
    bajada: "La medida, vigente desde octubre pasado, alcanza a organismos como IAPV, IAFAS y Vialidad.",
    cuerpo: [
      "El Poder Ejecutivo prorrogó por seis meses más el congelamiento de nuevas designaciones y contrataciones en la administración central y en los entes autárquicos, según un decreto difundido esta semana.",
      "La medida original databa de octubre de 2025 y se enmarca en el plan de ajuste fiscal de la gestión provincial.",
      "Gremios estatales cuestionaron la extensión y advirtieron sobre la sobrecarga de tareas en las áreas con vacantes sin cubrir.",
    ],
    seedFoto: "congelamiento-designaciones",
  }),
  post({
    id: -3,
    slug: "comision-bicameral-caja-jubilaciones-dictamen",
    date: "2026-09-04T09:40:00",
    categoria: "Política",
    categoriaSlug: "politica",
    titulo: "La comisión bicameral que seguirá a la Caja de Jubilaciones obtuvo dictamen",
    bajada: "El proyecto, impulsado en julio, pasa ahora al recinto del Senado para su tratamiento.",
    cuerpo: [
      "El proyecto que crea una comisión bicameral de seguimiento de la Caja de Jubilaciones y Pensiones de Entre Ríos obtuvo dictamen favorable en la comisión de Asuntos Constitucionales del Senado.",
      "La comisión estaría integrada por diez legisladores, cinco de cada cámara, respetando la representación proporcional de los bloques.",
      "De aprobarse en el recinto, sería el primer mecanismo formal de control legislativo permanente sobre el organismo previsional provincial.",
    ],
    seedFoto: "caja-jubilaciones",
  }),
  post({
    id: -4,
    slug: "oposicion-pidio-informes-fondos-viales",
    date: "2026-09-03T16:10:00",
    categoria: "Política",
    categoriaSlug: "politica",
    titulo: "Bloques de la oposición pidieron informes sobre la ejecución de fondos viales",
    bajada: "El pedido apunta a obras de la Dirección Provincial de Vialidad iniciadas en 2024 y todavía sin terminar.",
    cuerpo: [
      "Legisladores de la oposición presentaron un pedido de informes formal para que el Poder Ejecutivo detalle el estado de ejecución de un conjunto de obras viales financiadas con fondos nacionales y provinciales.",
      "El pedido incluye un listado de quince obras iniciadas desde 2024, de las cuales según los legisladores solo cuatro estarían terminadas.",
      "El Ejecutivo tiene un plazo de treinta días para responder.",
    ],
    seedFoto: "fondos-viales",
  }),
  post({
    id: -5,
    slug: "concejo-parana-media-sancion-boleto-estudiantil",
    date: "2026-09-02T11:00:00",
    categoria: "Política",
    categoriaSlug: "politica",
    titulo: "El Concejo Deliberante de Paraná dio media sanción a la ampliación del boleto estudiantil gratuito",
    bajada: "El proyecto extiende el beneficio a estudiantes terciarios y universitarios de la ciudad.",
    cuerpo: [
      "El Concejo Deliberante de Paraná aprobó en primera lectura la ampliación del boleto estudiantil gratuito, que hasta ahora alcanzaba solo a estudiantes de nivel secundario.",
      "La iniciativa pasa a una segunda vuelta con audiencia pública antes de su sanción definitiva, según establece la carta orgánica municipal.",
    ],
    seedFoto: "boleto-estudiantil",
  }),
  post({
    id: -6,
    slug: "fiscalia-estado-informe-anual-juicios",
    date: "2026-09-01T10:00:00",
    categoria: "Política",
    categoriaSlug: "politica",
    titulo: "Fiscalía de Estado detalló los juicios en trámite contra la provincia",
    bajada: "El informe anual, elevado a la Legislatura, incluye causas por deuda pública y obra vial.",
    cuerpo: [
      "Fiscalía de Estado presentó ante la Legislatura el informe anual sobre juicios en trámite contra la provincia, una obligación legal poco difundida hasta ahora.",
      "El documento agrupa las causas por monto reclamado y por área, con la deuda pública y los reclamos por obra vial entre los rubros de mayor exposición económica.",
    ],
    seedFoto: "fiscalia-estado",
  }),

  // Economía
  post({
    id: -7,
    slug: "exportaciones-entrerrianas-suben-primer-semestre",
    date: "2026-09-06T14:30:00",
    categoria: "Economía",
    categoriaSlug: "economia",
    titulo: "Las exportaciones entrerrianas crecieron en el primer semestre de 2026",
    bajada: "El complejo agroindustrial explicó la mayor parte del incremento interanual.",
    cuerpo: [
      "Las exportaciones de Entre Ríos crecieron en el primer semestre de 2026 respecto del mismo período del año anterior, impulsadas principalmente por el complejo avícola y el arrocero.",
      "El dato surge de un informe del Consejo Empresario de Entre Ríos que compara la performance exportadora de la provincia con el resto de la región centro.",
      "El informe advierte que buena parte del crecimiento responde a precios internacionales más que a mayor volumen físico exportado.",
    ],
    seedFoto: "exportaciones-er",
  }),
  post({
    id: -8,
    slug: "ceer-advierte-caida-consumo-energia-industrial",
    date: "2026-09-05T09:15:00",
    categoria: "Economía",
    categoriaSlug: "economia",
    titulo: "Un informe privado advirtió sobre la caída del consumo eléctrico industrial",
    bajada: "La baja se concentra en las industrias metalúrgica y frigorífica de la provincia.",
    cuerpo: [
      "El Consejo Empresario de Entre Ríos difundió un informe que muestra una caída interanual del consumo eléctrico industrial, con mayor impacto en la industria metalúrgica y frigorífica.",
      "Empresarios del sector atribuyen la baja a la contracción de la actividad y al encarecimiento de la tarifa eléctrica para grandes usuarios.",
    ],
    seedFoto: "consumo-industrial",
  }),
  post({
    id: -9,
    slug: "ater-anuncia-moratoria-impositiva-comercios",
    date: "2026-09-04T13:00:00",
    categoria: "Economía",
    categoriaSlug: "economia",
    titulo: "ATER lanzó una moratoria impositiva para pequeños comercios",
    bajada: "El plan de pagos alcanza a Ingresos Brutos con hasta 24 cuotas y quita de intereses.",
    cuerpo: [
      "La Administración Tributaria de Entre Ríos (ATER) lanzó un régimen de moratoria para pequeños contribuyentes de Ingresos Brutos, con planes de pago de hasta 24 cuotas y quita parcial de intereses resarcitorios.",
      "El organismo estima que la medida podría alcanzar a unos 18.000 contribuyentes con deuda en mora.",
    ],
    seedFoto: "ater-moratoria",
  }),
  post({
    id: -10,
    slug: "camara-comercio-parana-reporta-baja-ventas-agosto",
    date: "2026-09-03T08:30:00",
    categoria: "Economía",
    categoriaSlug: "economia",
    titulo: "La Cámara de Comercio de Paraná registró una baja de ventas en agosto",
    bajada: "El relevamiento propio mostró una caída interanual en rubros de indumentaria y electrodomésticos.",
    cuerpo: [
      "La Cámara de Comercio, Industria y Producción de Paraná difundió su relevamiento mensual de ventas, con una caída interanual concentrada en indumentaria, calzado y electrodomésticos.",
      "El sector gastronómico y de alimentos, en cambio, mostró un leve crecimiento.",
    ],
    seedFoto: "comercio-parana",
  }),
  post({
    id: -11,
    slug: "puerto-diamante-licita-dragado",
    date: "2026-09-02T15:45:00",
    categoria: "Economía",
    categoriaSlug: "economia",
    titulo: "El puerto de Diamante llamó a licitación para el dragado del canal de acceso",
    bajada: "La obra busca permitir el ingreso de buques de mayor calado.",
    cuerpo: [
      "El ente portuario de Diamante abrió la licitación pública para el dragado del canal de acceso, con el objetivo de permitir el ingreso de buques de mayor calado y aumentar la carga operada.",
      "La apertura de ofertas está prevista para fines de septiembre.",
    ],
    seedFoto: "puerto-diamante",
  }),
  post({
    id: -12,
    slug: "sector-avicola-entrerriano-exporta-nuevo-mercado",
    date: "2026-09-01T11:20:00",
    categoria: "Economía",
    categoriaSlug: "economia",
    titulo: "Frigoríficos avícolas entrerrianos habilitaron un nuevo mercado de exportación",
    bajada: "El acuerdo sanitario permite el envío de productos aviares a un país de Medio Oriente.",
    cuerpo: [
      "Dos frigoríficos avícolas radicados en Entre Ríos quedaron habilitados para exportar a un nuevo mercado tras un acuerdo sanitario bilateral gestionado por el Senasa.",
      "El sector avícola es uno de los principales empleadores industriales de la provincia.",
    ],
    seedFoto: "sector-avicola",
  }),

  // Boletín Oficial / Justicia
  post({
    id: -13,
    slug: "epre-convoca-audiencia-publica-revision-tarifaria",
    date: "2026-09-06T10:00:00",
    categoria: "Boletín Oficial",
    categoriaSlug: "boletin-oficial",
    titulo: "El EPRE convocó a audiencia pública por la revisión tarifaria integral",
    bajada: "La audiencia se realizará en Paraná con defensores del usuario designados por colegios profesionales.",
    cuerpo: [
      "El Ente Provincial Regulador de la Energía convocó a audiencia pública en el marco de la Revisión Tarifaria Integral (RTI) en curso, según una resolución publicada en el Boletín Oficial.",
      "Participarán defensores de los usuarios propuestos por colegios profesionales, tal como establece el reglamento de audiencias públicas del organismo.",
    ],
    seedFoto: "epre-audiencia",
  }),
  post({
    id: -14,
    slug: "tribunal-cuentas-observa-rendicion-municipio",
    date: "2026-09-05T17:30:00",
    categoria: "Boletín Oficial",
    categoriaSlug: "boletin-oficial",
    titulo: "El Tribunal de Cuentas observó la rendición de un municipio del interior",
    bajada: "El organismo detectó gastos sin respaldo documental por un monto significativo.",
    cuerpo: [
      "El Tribunal de Cuentas de Entre Ríos observó la rendición de cuentas anual de un municipio del interior provincial, al detectar gastos sin la documentación respaldatoria exigida por la normativa.",
      "El municipio tiene un plazo para presentar el descargo correspondiente antes de que el organismo se expida en forma definitiva.",
    ],
    seedFoto: "tribunal-cuentas",
  }),
  post({
    id: -15,
    slug: "stj-confirma-fallo-causa-ambiental",
    date: "2026-09-04T12:15:00",
    categoria: "Boletín Oficial",
    categoriaSlug: "boletin-oficial",
    titulo: "El Superior Tribunal de Justicia confirmó un fallo en una causa ambiental",
    bajada: "La sentencia obliga a una empresa a remediar un predio en la costa del río Paraná.",
    cuerpo: [
      "El Superior Tribunal de Justicia de Entre Ríos confirmó la sentencia de primera instancia que obliga a una empresa a remediar un predio contaminado sobre la costa del río Paraná.",
      "La causa había sido iniciada por una organización ambientalista local hace más de tres años.",
    ],
    seedFoto: "fallo-ambiental",
  }),
  post({
    id: -16,
    slug: "boletin-oficial-decreto-contratacion-directa-salud",
    date: "2026-09-03T09:00:00",
    categoria: "Boletín Oficial",
    categoriaSlug: "boletin-oficial",
    titulo: "Un decreto autorizó una contratación directa por excepción para el Ministerio de Salud",
    bajada: "La compra de insumos médicos evitó el proceso de licitación pública por razones de urgencia.",
    cuerpo: [
      "El Poder Ejecutivo autorizó, por decreto, una contratación directa por excepción para la compra de insumos médicos destinados a hospitales públicos, invocando razones de urgencia sanitaria.",
      "La normativa exige en estos casos una justificación técnica y legal específica, incluida como anexo del decreto.",
    ],
    seedFoto: "decreto-salud",
  }),
  post({
    id: -17,
    slug: "consejo-magistratura-concurso-jueces-vacantes",
    date: "2026-09-02T08:45:00",
    categoria: "Boletín Oficial",
    categoriaSlug: "boletin-oficial",
    titulo: "El Consejo de la Magistratura abrió concurso para cubrir tres juzgados vacantes",
    bajada: "Los cargos corresponden a juzgados civiles y de familia del interior provincial.",
    cuerpo: [
      "El Consejo de la Magistratura de Entre Ríos abrió la inscripción para el concurso de antecedentes y oposición que cubrirá tres juzgados vacantes en el interior de la provincia.",
      "El proceso incluye una instancia de entrevista pública con los candidatos preseleccionados.",
    ],
    seedFoto: "consejo-magistratura",
  }),

  // Municipios
  post({
    id: -18,
    slug: "concordia-adhiere-compromiso-transparencia",
    date: "2026-09-06T08:00:00",
    categoria: "Municipios",
    categoriaSlug: "municipios",
    titulo: "Concordia adhirió al Compromiso Provincial de Transparencia",
    bajada: "La ciudad completó la publicación de su escala salarial y nómina de autoridades.",
    cuerpo: [
      "La Municipalidad de Concordia formalizó su adhesión al Compromiso Provincial de Transparencia y Apertura Gubernamental, y ya publicó la escala salarial y la nómina de autoridades exigidas.",
      "Resta la publicación de las declaraciones juradas patrimoniales sintéticas, según el propio cronograma municipal.",
    ],
    seedFoto: "concordia-transparencia",
  }),
  post({
    id: -19,
    slug: "gualeguaychu-presupuesto-2027-debate",
    date: "2026-09-05T14:00:00",
    categoria: "Municipios",
    categoriaSlug: "municipios",
    titulo: "El Concejo de Gualeguaychú comenzó el debate del presupuesto 2027",
    bajada: "El proyecto del Ejecutivo municipal prevé un fuerte incremento en obra pública.",
    cuerpo: [
      "El Concejo Deliberante de Gualeguaychú inició el tratamiento en comisión del proyecto de presupuesto municipal para 2027, que contempla un incremento en la partida de obra pública respecto del ejercicio actual.",
      "La oposición local cuestionó las proyecciones de recaudación sobre las que se arma el cálculo.",
    ],
    seedFoto: "gualeguaychu-presupuesto",
  }),
  post({
    id: -20,
    slug: "victoria-defensoria-pueblo-municipal",
    date: "2026-09-03T10:30:00",
    categoria: "Municipios",
    categoriaSlug: "municipios",
    titulo: "Victoria evalúa crear una defensoría del pueblo municipal",
    bajada: "El proyecto surge después de que la ciudad quedara fuera del ranking de transparencia provincial.",
    cuerpo: [
      "Un bloque del Concejo Deliberante de Victoria presentó un proyecto para crear una defensoría del pueblo municipal, inspirado en la de Paraná, la única con jurisdicción en la provincia hasta ahora.",
      "La iniciativa llega después de que la ciudad quedara entre los municipios que no adhirieron al Compromiso Provincial de Transparencia.",
    ],
    seedFoto: "victoria-defensoria",
  }),
  post({
    id: -21,
    slug: "federacion-declara-interes-audiencia-epre",
    date: "2026-09-01T09:00:00",
    categoria: "Municipios",
    categoriaSlug: "municipios",
    titulo: "Federación declaró de interés municipal la audiencia pública del EPRE",
    bajada: "El Concejo Deliberante local acompañó la convocatoria a la revisión tarifaria eléctrica.",
    cuerpo: [
      "El Concejo Deliberante de Federación declaró de interés municipal la audiencia pública convocada por el ente regulador de energía sobre la revisión tarifaria integral.",
      "La sesión se realizará en esa ciudad, según la resolución de convocatoria.",
    ],
    seedFoto: "federacion-epre",
  }),

  // Sociedad
  post({
    id: -22,
    slug: "uader-abre-inscripcion-becas-comedores",
    date: "2026-09-04T16:00:00",
    categoria: "Sociedad",
    categoriaSlug: "sociedad",
    titulo: "La UADER abrió la inscripción a becas de comedor para el segundo cuatrimestre",
    bajada: "El programa alcanza a estudiantes de todas las facultades de la universidad provincial.",
    cuerpo: [
      "La Universidad Autónoma de Entre Ríos abrió la inscripción a su programa de becas de comedor para el segundo cuatrimestre, destinado a estudiantes con dificultades económicas acreditables.",
      "El cupo se amplió un 10% respecto del cuatrimestre anterior, según informó la universidad.",
    ],
    seedFoto: "uader-becas",
  }),
  post({
    id: -23,
    slug: "hospital-parana-amplia-guardia-pediatrica",
    date: "2026-09-02T13:30:00",
    categoria: "Sociedad",
    categoriaSlug: "sociedad",
    titulo: "Un hospital de Paraná amplió su guardia pediátrica",
    bajada: "La ampliación busca reducir los tiempos de espera registrados durante el invierno.",
    cuerpo: [
      "El hospital público de referencia pediátrica en Paraná amplió su guardia con dos consultorios adicionales, tras el pico de consultas respiratorias registrado durante el invierno.",
      "Autoridades del centro de salud señalaron que los tiempos de espera se redujeron desde la implementación del cambio.",
    ],
    seedFoto: "hospital-pediatrico",
  }),
  post({
    id: -24,
    slug: "copnaf-programa-acompañamiento-familias",
    date: "2026-08-31T11:00:00",
    categoria: "Sociedad",
    categoriaSlug: "sociedad",
    titulo: "COPNAF amplió un programa de acompañamiento a familias en situación de vulnerabilidad",
    bajada: "El organismo sumó equipos técnicos en tres departamentos del interior.",
    cuerpo: [
      "El Consejo Provincial del Niño, el Adolescente y la Familia (COPNAF) amplió su programa de acompañamiento familiar con nuevos equipos técnicos en tres departamentos del interior provincial.",
      "El organismo había sido cuestionado en el pasado por la falta de cobertura territorial fuera de Paraná.",
    ],
    seedFoto: "copnaf-programa",
  }),
];

function porCategoria(slug: string) {
  return mockPosts.filter((p) => p._embedded?.["wp:term"]?.[0]?.[0]?.slug === slug);
}

export const mockEconomia = porCategoria("economia");
export const mockBoletinOficial = porCategoria("boletin-oficial");
export const mockMunicipios = porCategoria("municipios");
export const mockSociedad = porCategoria("sociedad");
