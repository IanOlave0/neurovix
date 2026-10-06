# Revisión de literatura — NeuroVix (Fase 0)

> Barrido sistemático oct-2026 vía paper-search MCP (PubMed, arXiv, medRxiv).
> Criterio de inclusión: cuantificación automatizada de asimetría/parálisis
> facial con landmarks, triaje de ACV desde video, o métodos transferibles
> (features geométricas, dinámica temporal, privacidad de video clínico).

## Bitácora de búsqueda (rastro de método)

| Fuente | Queries | Resultado |
|---|---|---|
| PubMed | "automated facial palsy detection facial landmarks" | 5 relevantes (núcleo clínico) |
| PubMed | "prehospital stroke triage facial video computer vision", "automated Cincinnati stroke scale facial droop detection", "facial palsy dataset video landmarks" | Vacío — queries demasiado específicas para indexado por keywords |
| PubMed | "stroke facial video", "stroke triage artificial intelligence" | Ruido (clínicas TIA, gestión hospitalaria) — coinciden palabras, no problema |
| arXiv | "facial palsy detection facial landmarks", "stroke detection facial asymmetry video", "MediaPipe face mesh facial analysis" | 2 hits directos + 3 metodológicos; resto ruido (deepfakes, animatrónica, MRI) |
| medRxiv | "facial palsy detection video", "stroke face video triage" | Herramienta ignoró las queries (devolvió resultados no relacionados) — no usar hasta verificar fix |

## Fichas

### Núcleo clínico (parálisis facial automatizada)

**F1. Heinrich et al. 2026 — Angle maps de asimetría en parálisis periférica.**
405 datasets de 198 pacientes, 9 expresiones estandarizadas, 478 landmarks → 225
pares → 91 pares informativos (ojos, nariz, boca). Correlación 0.32–0.73 con
scores clínicos. Robusto a rotación de cabeza.
PubMed 42072220 · doi:10.3390/bioengineering13040426
*Relevancia: baseline de "asimetría estática densa"; nuestro contraste es cinemática + triaje agudo.*

**F2. Heinrich et al. 2025 — Symmetry scoring con deep learning (Sci Rep).**
Mismo cohorte; heatmaps de diferencia + score de simetría 0–0.99. En 9% de
casos el score cambió mientras el score clínico Stennert no → mayor
sensibilidad que la escala humana. Correlación −0.32 a −0.66 con severidad.
PubMed 40866588 · doi:10.1038/s41598-025-17172-1
*Relevancia: evidencia de que lo automatizado puede superar en sensibilidad a la escala clínica.*

**F3. Zhou et al. 2026 — Sistema objetivo de evaluación de parálisis facial.**
Automatización de FACE-gram (hoy manual). Enmarca el problema como
"subjetivo, inconsistente, ineficiente".
PubMed 40623140 · doi:10.1097/SCS.0000000000011638
*Relevancia: valida el framing "objetivar lo subjetivo".*

**F4. Supratak et al. 2025 — Features dinámicas de parpadeo (clave para H1).**
103 sujetos (86 sanos, 17 FNP), video de alta tasa. Normality scores de
parpadeo vía Isolation Forest: **+75% F1 vs. parámetros estáticos, +35% vs.
dinámicos crudos**. Feature ganadora: velocidad de cierre del párpado.
CompBiomed 2025. PubMed 39914202 · doi:10.1016/j.compbiomed.2025.109722
*Relevancia: RESPALDO EMPÍRICO de H1 — la velocidad supera a lo estático. Cita central del preprint.*

**F5. Kimura et al. 2025 — Los landmarkers fallan en caras paréticas (clave para R7).**
Modelo de 68 puntos entrenado en sanos aplicado a 30 pacientes: los detecta
como simétricos, no captura cierre de ojos. Requiere fine-tuning con
anotación. PubMed 39688730 · doi:10.1097/PRS.0000000000011924
*Relevancia: EVIDENCIA del riesgo R7. Justifica nuestra validación de robustez desde Fase 1.*

### Espacio del problema (ACV + video + privacidad)

**F6. SafeTriage, Cai et al. 2025 (arXiv:2506.16578) — Triaje de ACV desde video facial + desidentificación.**
Confirma que hay modelos IA detectando patrones de coordinación muscular
facial sutil en videos de pacientes con ACV en emergencias. Propone
transferencia de movimiento a identidades sintéticas para compartir datos
sin exponer pacientes + prompt tuning para el shift sano→paciente.
*Relevancia doble: (a) valida que el espacio-problema existe y está activo;
(b) la desidentificación que preserva movimiento es una vía futura para el
problema de datos (R1): compartir cinemática sin compartir caras.*

**F7. Oo et al. 2024/25 (arXiv:2405.16496) — Detección multimodal de parálisis facial, N=21.**
Compara modalidades: red feed-forward sobre *features de expresión*
(precisión 76.22) vs. ResNet sobre segmentos faciales (recall 83.47);
fusión 77.05. Landmarks + features ingenieriles compiten con CNN.
*Relevancia: precedente de N pequeña con ML clásico sobre features — nuestro régimen exacto.*

### Precedentes metodológicos (transferibles)

**F8. Ghimire & Lee 2016 (arXiv:1604.03225) — Features geométricas punto/línea/triángulo + SVM.**
Tracking de landmarks en secuencias, features normalizadas contra el primer
frame (¡línea base por sesión, como la nuestra!), AdaBoost + DTW y SVM:
95–97% en CK+.
*Relevancia: el blueprint metodológico "geometría + ML clásico en secuencias" con 10 años de precedente.*

**F9. Praveen et al. 2021/26 (arXiv:2101.09858) — Revisión de weakly-supervised FABA.**
Taxonomía de aprendizaje con anotación débil para análisis afectivo facial
en video: el paradigma para entrenar con pocos datos etiquetados.
*Relevancia: marco teórico si la vía de datos exige semisupervisión (Fase 2).*

### Referencias de contexto (conocimiento establecido)

- **Saver JL. 2006 — "Time is brain — quantified"** (1.9M neuronas/min). Stroke 37(1):263-266.
- **INEGI EDR 2024:** 34,784 muertes cerebrovasculares en México (7.ª causa nacional). Comunicado 142/25. (Vía banco de evidencia TI1.)

## Huecos confirmados (nuestra ventana)

1. **Sin dataset público de parálisis aguda por ACV con gestos** (confirma R1).
2. **Sin automatización de Cincinnati/FAST prehospitalaria con cinemática de gestos** (confirma diferenciación R3).
3. **Casi todo el arte previo es parálisis periférica crónica**, no evento agudo central (delimita nuestras afirmaciones).
