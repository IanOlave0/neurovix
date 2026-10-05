# Banco de evidencia — NeuroVix (TI I)

> Regla HIDRANEX: si no apunta a EV-xx, se marca H-xx o S-xx. No rellenar con ocurrencias. Datos SIMULADOS no existen aquí — todo es real o se marca FALTANTE.

## Clínica (EVC / triaje)

- **EV-01** Mortalidad EVC México 2021: 37,453 decesos, 7ª causa muerte. Fuente: SSA comunicado 531 (INNN), 2022. https://www.gob.mx/salud/prensa/531-en2021-ictus-o-enfermedad-vascular-cerebral-ocasiono-mas-de-37-mil-decesos-en-mexico
- **EV-02** Incidencia MX: 118/100mil ≈170mil casos/año; 20% muere 30 días; 7/10 con discapacidad. Fuente: idem EV-01.
- **EV-03** INEGI EDR 2024: 34,784 muertes cerebrovasculares (7º nacional). Fuente: INEGI comunicado 142/25. https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/edr/EDR2024-def_CP.pdf
- **EV-04** Time is Brain (Saver 2006): 1.9M neuronas/min, 14B sinapsis/min, 120M/hora. Fuente: Stroke 2006;37:263-266. DOI:10.1161/01.STR.0000196957.55928.ab
- **EV-05** Cada 15 min más rápido a tPA: menor mortalidad (OR 0.96), menos hemorragia (OR 0.96). Fuente: Saver et al. JAMA 2013;309:2480-88. DOI:10.1001/jama.2013.6959
- **EV-06** Ventanas AHA/ASA: IV ≤4.5h, trombectomía hasta 24h, meta puerta-aguja ≤60min. Fuente: StatPearls NBK557411 + AHA Guideline 2026 STR.0000000000000513.
- **EV-07** NIHSS ítem 4 cara 0-3 (0 normal, 3 completa). Fuente: NINDS NIHSS oficial 2024-25.
- **EV-08** FAST: cara es primer dominio; sensibilidad ~88% ictus anterior, pierde posteriores; BE-FAST baja omitidos 14.1%→9.9%. Fuente: Harbison Stroke 2003; Aroor Stroke 2017 DOI:10.1161/STROKEAHA.116.015169
- **EV-09** CAMALEÓN MX: CAra colgada + MAno pesada + LEngua trabada + ON. Fuente: SSA/INNN + Metro CDMX 2020. https://metro.cdmx.gob.mx/comunicacion/nota/el-metro-cdmx-implementa-la-estrategia-camaleon-para-la-identificacion-del-infarto-cerebral
- **EV-10** Error triaje real: 20-40% sospechas en ED son mimics; ~9% ictus se pierde en primer contacto; EMS mal clasifica ~28%. Fuente: StatPearls NBK541044; Circ CQO 2021; Stroke 2025 STROKEAHA.124.048067
- **EV-11** Central vs periférica: en ACV central frente preservada; en Bell toda hemicara incluida frente. Fuente: Tiemstra AFP 2007; AFP 2014 p283; Patel Cleve Clin 2015; Induruwa PMC6899254 2019.
- **EV-12** Código Cerebro IMSS: 911 → ambulancia → hora inicio → triaje rojo → TAC → lisis <4.5h. Fuente: IMSS 2022 + PAI Código Cerebro PDF. https://www.gob.mx/imss/prensa/lanza-imss-programa-codigo-cerebro-para-diagnosticar-y-mejorar-el-tiempo-de-respuesta-ante-eventos-cerebro-vasculares

## Técnica (edge / landmarks)

- **EV-13** FaceMesh: 468 landmarks 3D tiempo real en móvil sin profundidad. Fuente: MediaPipe docs + Kartynnik arXiv:1907.06724 (2019).
- **EV-14** Face Landmarker sucesor: 478 landmarks + 52 blendshapes + modo LIVE_STREAM. Fuente: Google Edge docs 2026. https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker
- **EV-15** CPU-only factible: BlazeFace liviano + Face Transform Procrustes en CPU + LiteRT/ONNX CPU default. Fuente: MediaPipe docs; LiteRT measurement; ONNX Runtime Mobile docs.
- **EV-16** Degradación probada en parálisis: NRMSE 8.56 vs 7.09 sanos (p<<0.01); reentrenar con 1440 fotos clínicas baja a 6.03. Fuente: Guarin arXiv:1910.11497 (2019).
- **EV-17** Precedente cinemático: 6 regiones + optical flow + symmetry score. Fuente: Taufique arXiv:2103.11059 (2021).
- **EV-18** Angle maps denso: 478 landmarks → 225 pares → 91 óptimos; Spearman 0.32-0.73 vs Stennert. Fuente: Bioengineering 13(4):426.
- **EV-19** Central vs periférica con landmarks logra 85.1% SVM (Palda: 103 perif +40 central +60 sanos). Fuente: Vletter arXiv:2201.11852 (2022).
- **EV-20** R1 confirmado: NO hay dataset público EVC agudo con gestos. DeepStroke publica código pero no datos. Fuente: arXiv:2109.12065 + github 0CTA0/MICCAI20_MMDL_PUBLIC.

## Operativa / legal (MX)

- **EV-21** NOM-034-SSA3-2013 regula atención prehospitalaria y ambulancias. Vigente. Fuente: DOF 2014.
- **EV-22** NOM-004-SSA3-2012 expediente + consentimiento; NOM-024-SSA3-2012 interoperabilidad ECE. Fuente: DOF 2012.
- **EV-23** Compra hospital público: LAASSP (licitación/invitación/adjudicación) vía Compras MX + evaluación CENETEC/GEM. Fuente: LAASSP PDF + CENETEC GEM.
- **EV-24** LFPDPPP nueva DOF 20-mar-2025: datos salud = sensibles, Art.9 consentimiento expreso escrito. Video facial = biométrico sensible. Fuente: diputados.gob.mx LFPDPPP PDF.
- **EV-25** SaMD MX: apps que cumplen definición SON SaMD; Regla 16 riesgo; Farmacopea Ed.5.0 vigente 10-jul-2023. Si declara apoyo triaje EVC probablemente SÍ SaMD. Fuente: Farmacopea + adherent.com resumen 2024.
- **EV-26** Alert fatigue: >2M alertas/mes en 66 camas UCI (187/paciente/día); override mayoría incluso críticas; antídoto = especificidad + contexto + tier severidad. Fuente: AHRQ PSNet Alert Fatigue; Ray PMC13385993 2026; Wu Nature 2026 s41746-026-02522-8.
- **EV-27** Barreras adopción Américas: infra TIC, seguridad, cultura, vacíos normativos, capacitación; facilitador = apoyo directivo + aceptabilidad personal. Fuente: Saiso PMC8530000 2021; OPS 2023.

## FALTANTE explícito (no afirmar, requiere investigación propia)

- **F-01** Tasa error/duda prehospitalaria específica MX y sens/espec FAST/CAMALEÓN en MX.
- **F-02** Tiempo onset-to-door / puerta-aguja promedio MX.
- **F-03** TCO y disposición a pagar por app on-device en IMSS/Cruz Roja.
- **F-04** Onset lag L-R como feature específica EVC agudo (hipótesis, sin paper 2024-26).
- **F-05** Dictamen Cofepris + protocolo consentimiento en EVC inconsciente (consentimiento diferido).
- **F-06** Tasa override alertas en ambulancia MX.
