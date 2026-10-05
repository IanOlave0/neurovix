# CANVAS 0.1 — NeuroVix (idea inicial sin maquillar)

> Idea inicial: "App con IA que detecta EVC por cara desde el celular." ALERTA igual que HIDRANEX: solución antes que problema, segmento, valor y necesidad de IA.

## 1. Segmentos
- Adultos 45-70 con riesgo vascular atendidos en urgencias/prehospitalario MX [EV-02]
- Paramédicos TUM / enfermería triaje que dudan ante asimetría sutil [H-01: dudan y retrasa traslado — validar con observación]
- Hospitales 2º/3er nivel con Código Cerebro [EV-12]

## 2. Problema (antes que tecnología)
- EVC 170mil/año MX, 7/10 discapacidad, 20% muere 30d [EV-01/EV-02]
- Cada minuto = 1.9M neuronas; ventana IV ≤4.5h, puerta-aguja ≤60min [EV-04/EV-06]
- 20-40% sospechas son mimics; 9% ictus se pierde; EMS mal clasifica 28% [EV-10]
- Cara es primer dominio FAST/CAMALEÓN/NIHSS [EV-07/EV-08/EV-09]

## 3. Propuesta (hipótesis)
- Copiloto on-device que cuantifica asimetría + cinemática y prenotifica con contexto [H-02]
- No diagnostica, sesgo a falso positivo, humano decide [EV-riesgo R2 docs/riesgos.md]

## 4. Canales
- Piloto investigación vía coordinación emergencias/UMAE + convenio [H-03, EV-23 evita CompraNet fase 1]
- Capacitación TUM/enfermería en turno [EV-27]

## 5. Relación
- Soporte + trazabilidad (sugerencia, hora, operador, decisión clínica) [EV-26 antídoto]
- Nunca "no hay ACV" [diseño docs/README.md]

## 6. Ingresos (modelo híbrido por validar)
- H-03: institución paga por indicadores (tiempo notificación, traslados secundarios evitados, adherencia Código Cerebro), no por accuracy. [H]

## 7. Recursos clave
- App Android (Face Landmarker 478 + 52 blendshapes, LIVE_STREAM) CPU-only [EV-14/EV-15]
- Módulo landmarks.py con índices fijos [docs/protocolo.md]
- Checklist CAMALEÓN auto-sellado hora [EV-09/EV-12]

## 8. Actividades clave
- Validar degradación landmarks en asimetría (NRMSE 8.56 vs 7.09) [EV-16]
- Buscar proxy Bell + síntesis, declarar límites (Bell≠ACV) [EV-20, docs/protocolo.md]
- Medir sens@spec90, AUC con IC, splits por sujeto [docs/protocolo.md]

## 9. Socios
- IMSS/Cruz Roja/Protección Civil, CENETEC, comité ética [EV-12/EV-23]
- MediaPipe/Google Edge, ONNX/LiteRT [EV-13/EV-14]

## 10. Costos
- Desarrollo + validación clínica + capacitación rotación TUM + MDM + soporte + revalidación SaMD [H, EV-25]
- Ventaja: usa smartphone existente, offline, sin CT/helicóptero [H vs MSU $70k incremental EV-operativa]

## Clasificación E/H/S por bloque
- Segmentos: EV (carga) + H (duda retrasa — falta F-01) + EV (Código Cerebro existe)
- Problema: EV fuerte (EV-01 a EV-12)
- Solución/IA: S-01 "IA necesaria" → se descarta como argumento; H-02 reglas simples primero, ML solo si supera baseline [igual que HIDRANEX H-06]
- Canales/ingresos: H-03 (falta F-03 willingness-to-pay)
- Recursos: EV (FaceMesh/Landmarker CPU)
- Actividades: EV (riesgo landmarks) + H (onset lag H-protocolo)

## Evidencia actual vs faltante
- Actual: carga, ventana, FAST/NIHSS/CAMALEÓN, FaceMesh CPU, degradación, no-dataset, NOMs, LAASSP, LFPDPPP 2025, SaMD, alert fatigue.
- Faltante: F-01 a F-06 (ver 00-banco-evidencia.md). No avanzar a desarrollo hasta definir métricas M y seguridad SEC en Canvas 0.2.
