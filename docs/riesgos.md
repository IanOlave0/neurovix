# Análisis de riesgos — NeuroVix

> Evaluación contra el marco de 6 pruebas + registro de riesgos. Última actualización: 2026-10-02.

## Veredicto por prueba

| Prueba | Veredicto | Razón |
|---|---|---|
| 1. Facilidad de construcción | [OK] Pasa fuerte | MVP geométrico en 2-3 semanas; CPU-only; modelos preentrenados |
| 2. Usabilidad y adopción | [OK] Pasa fuerte | Usuario claro; cero hardware especial; demo interactiva; reserva regulatoria |
| 3. Competencia e innovación | [Reserva] Pasa con reservas | Existe arte previo; diferenciación: cinemática temporal + triaje prehospitalario + edge LATAM + central vs. periférica |
| 4. Datos | [Crítico] Riesgo crítico | No hay dataset público de parálisis facial aguda por ACV con gestos |
| 5. Tolerancia al error | [Reserva] Riesgo alto, mitigable | Categoría de falso negativo letal — requiere diseño copiloto |
| 6. Viabilidad económica | [OK] Pasa fuerte | Inferencia edge ~$0; ROI en hora dorada |

## Cómo sobrevive a cada prueba

### Prueba 4 — Datos (el filtro crítico)

**Estrategia:** el núcleo es geométrico/rule-based → no requiere entrenamiento. El clasificador es capa v2 construida sobre:

1. Síntesis controlada por deformación de landmarks (etiquetada como limitación)
2. Proxy Bell's palsy como señal de dominio
3. Colaboración clínica como stretch goal

**Regla:** nunca afirmar más de lo que la fuente de datos permite.

### Prueba 5 — Tolerancia al error

**Reglas de diseño obligatorias:**

- Nunca emitir "no hay ACV" — solo "asimetría baja: si hay síntomas, acude a emergencias"
- Sesgo deliberado hacia el falso positivo (sobre-derivar es aceptable; no detectar no lo es)
- Humano en el bucle: la app informa, la persona decide
- Disclaimer visible: no es dispositivo médico

## Registro de riesgos

| ID | Riesgo | Prob. | Impacto | Mitigación | Estado |
|---|---|---|---|---|---|
| R1 | No conseguir datos clínicos | Alta | Alto | Núcleo sin entrenamiento + síntesis + proxy | Mitigado por diseño |
| R2 | Falso negativo da falsa tranquilidad | Media | Muy alto | Copiloto + sesgo FP + disclaimers | Mitigado por diseño |
| R3 | Percepción de "wrapper de MediaPipe" | Media | Alto | Features cinemáticas + ablations + literatura (9 fichas en docs/literatura.md; arte previo mapeado: parálisis periférica crónica, sin triaje prehospitalario agudo) | En mitigación (Fase 2) |
| R4 | Confounders de pose/iluminación | Alta | Medio | Normalización + exclusiones | Pendiente (Fase 1) |
| R5 | Scope creep (muchas features/gestos) | Alta | Medio | Fases con DoD; MVP primero | Controlado |
| R6 | Regulatorio si se presenta como diagnóstico | Media | Alto | Framing research/educativo; sin uso clínico | Mitigado por diseño |
| R7 | Degradación de landmarks en caras asimétricas (modelos entrenados con caras sanas) | Alta | Alto | Validar robustez en asimetría sintética desde Fase 1; documentar límites; fine-tuning como opción | Detectado en literatura (oct 2026) |
