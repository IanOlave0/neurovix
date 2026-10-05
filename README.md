# NeuroVix 🧠

> Biomarcador neurológico cuantitativo desde la cámara de cualquier dispositivo: apoyo al triaje temprano de Evento Vascular Cerebral (EVC/ACV) mediante detección de asimetría facial.

**Estado:** 🟡 Fase 0 — Planeación y revisión de literatura
*(Nombre provisional; el repo puede renombrarse.)*

## El problema

- El EVC es la principal causa de discapacidad en adultos en México y Latinoamérica.
- Cada minuto sin tratamiento destruye ~1.9 millones de neuronas (Saver, 2006 — *"Time is Brain"*).
- Cuello de botella: en emergencias, las asimetrías faciales sutiles generan duda en paramédicos, personal de primer nivel y familiares, retrasando el traslado en la "hora dorada".

## La solución

Convertir la cámara frontal de un teléfono, tablet o laptop en un biomarcador objetivo:

1. **Captura en vivo** del rostro del paciente
2. **Landmarking 3D** con MediaPipe FaceMesh
3. **Métricas cinemático-dinámicas**: desviación angular, asimetría de vectores, velocidad de gesto y retraso de inicio entre hemisferios
4. **Índice de Parálisis Facial Objetivo** (interpretable)
5. **Recomendación copiloto** — nunca decisión autónoma

## Principios de diseño (no negociables)

| Principio | Implicación |
|---|---|
| **Copiloto, no juez** | Nunca emitir "no hay ACV". Sesgo deliberado hacia el falso positivo. El humano decide. |
| **100% on-device** | El video nunca sale del dispositivo. Privacidad por diseño. |
| **Núcleo interpretable primero** | Índice geométrico defendible antes que clasificador. El ML es capa v2. |
| **Fundamento clínico** | Gestos con racional clínico: la frente preservada orienta ACV central vs. parálisis periférica. |

## Stack

- **Captura / landmarks:** Python · OpenCV · MediaPipe FaceMesh
- **Features:** NumPy / SciPy (geometría vectorial 3D, normalización de escala y pose)
- **ML (Fase 2):** Scikit-learn / XGBoost
- **Despliegue (Fase 3+):** ONNX / TFLite

## Estructura del repo

```
neurovix/
├── README.md
└── docs/
    ├── plan.md        # Fases, timeline y entregables
    ├── protocolo.md   # Diseño experimental: pregunta, features, evaluación
    └── riesgos.md     # Análisis de riesgos y mitigaciones
```

## ⚠️ Disclaimer médico

Este proyecto es investigación y educación. **No es un dispositivo médico, no diagnostica y no sustituye la atención profesional.** Ante cualquier sospecha de ACV, llama inmediatamente a servicios de emergencia.
