# Plan del proyecto — NeuroVix

> Fases, entregables y criterios de éxito. Última actualización: 2026-10-02.
> **Calendario realineado** con la ventana crítica de aplicaciones internacionales (ver `~/.config/opencode/planes/plan-investigacion-internacional.md`). NeuroVix se secuencia para *alimentar* las aplicaciones, no para competir con ellas.

## Objetivo doble

1. **Producto:** herramienta de apoyo al triaje temprano de ACV mediante cuantificación de asimetría facial, 100% on-device y sin hardware especial.
2. **Investigación:** artefacto publicable (preprint + repo público reproducible) que responda la pregunta del [protocolo](protocolo.md). Es la pieza insignia de portafolio para la ruta de investigación internacional (meta: OIST).

## Resumen de fases (calendario realineado)

| Fase | Ventana | Entregable principal | Anclaje externo |
|---|---|---|---|
| 0. Planeación y literatura | 2–9 oct 2026 | Docs + arte previo mapeado | — |
| 1. MVP geométrico | 9–30 oct 2026 | Demo en vivo + índice de asimetría | Evidencia citable: **MPI (1 nov)** |
| 1.5. Mantenimiento | 1 nov – 16 dic 2026 | Literatura + robustez de landmarks + tareas pequeñas | **EPFL (29 nov) · ETH (16 dic)** |
| 2. Protocolo experimental | 4 ene – 27 feb 2027 | Evaluación rigurosa + resultados | **UTSIP (~15 ene) · ENLACE (5 feb)** |
| 3. Redacción y publicación | 1 mar – 30 abr 2027 | Preprint + repo público | **OIST con preprint (± 15 oct 2027)** |

## Regla de prioridad

Durante la **ventana crítica (nov–dic 2026)** las aplicaciones internacionales tienen prioridad absoluta y NeuroVix entra en modo mantenimiento. Si el proyecto entra en conflicto con el promedio (≥8.6) o con deadlines de aplicación, el proyecto cede.

## Fase 0 — Planeación y literatura (2–9 oct 2026)

- [x] Análisis contra el marco de 6 pruebas → [riesgos.md](riesgos.md)
- [x] Decisiones de diseño (copiloto, edge, núcleo geométrico)
- [x] Estructura de planeación en markdown
- [x] MCP paper-search conectado y verificado (PubMed/arXiv/bioRxiv/medRxiv/CrossRef)
- [ ] Setup: `git init`, estructura de carpetas, entorno Python
- [ ] Revisión de literatura: barrido sistemático + related work inicial
- [ ] Fichas de la bibliografía base (5 papers ya identificados: angle maps PFP, symmetry scoring, blinking dinámico, fine-tuning en video, evaluación objetivo)

**Entregable:** este plan + protocolo + riesgos + related work inicial.

## Fase 1 — MVP geométrico (9–30 oct 2026)

- [ ] Pipeline de captura estable (OpenCV + MediaPipe FaceMesh)
- [ ] Módulo de landmarks con índices documentados (`landmarks.py`)
- [ ] Normalización: escala (interocular) y pose (roll/yaw)
- [ ] Línea base de reposo por sesión
- [ ] Gesto: sonrisa → índice de asimetría interpretable
- [ ] Demo en vivo: overlay de malla + métricas en tiempo real
- [ ] **Robustez R7:** sanity check de estabilidad de landmarks ante asimetría sintética controlada

**Criterio de terminado (DoD):** la demo corre en tiempo real en laptop, cuantifica asimetría inducida controladamente y documenta su comportamiento ante caras asimétricas. Se cierra antes del cierre de la aplicación MPI.

## Fase 1.5 — Modo mantenimiento (1 nov – 16 dic 2026)

Prioridad absoluta: aplicaciones (EPFL 29 nov · ETH 16 dic). NeuroVix se mantiene vivo sin competir:

- [ ] Completar related work (lectura + fichas de papers)
- [ ] Preparar datos de desarrollo (grabaciones propias con consentimiento)
- [ ] Tareas pequeñas de documentación y tests
- [ ] Exploración de datasets proxy (Mobus / Hugging Face / PubMed) sin compromiso de resultados

**Regla:** no iniciar experimentos grandes en esta ventana.

## Fase 2 — Protocolo experimental (4 ene – 27 feb 2027)

- [ ] Features cinemáticas temporales (velocidad, onset lag, perfiles)
- [ ] Gestos adicionales: mostrar dientes, levantar cejas
- [ ] Estrategia de datos implementada (síntesis + búsqueda de proxy)
- [ ] Evaluación: splits por sujeto, sens@spec, AUC con IC
- [ ] Escalera de baselines y ablations
- [ ] Análisis de error de falsos negativos
- [ ] **Milestone:** resultados preliminares antes del **5 feb** (insumo para el ensayo ENLACE)

**DoD:** tabla de resultados reproducible con métricas, ablations y análisis de error.

## Fase 3 — Redacción y publicación (1 mar – 30 abr 2027)

- [ ] Preprint en inglés (formato arXiv)
- [ ] README en inglés + tests + reproducibilidad (semillas, versiones)
- [ ] Identificar venue y calendario de envíos (LatinX in AI @ NeurIPS · ML4H · IEEE EMBC student track)

**DoD:** PDF público + repo reproducible.
**Resultado esperado para la ruta:** preprint disponible 5+ meses antes de la aplicación a OIST (15 oct 2027).

## Backlog (post-v1)

- Clasificador ML como capa de producto (si la evidencia lo justifica)
- Empaquetado móvil (ONNX / TFLite)
- Extender a escala FAST completa (habla, debilidad de brazos)
- Validación clínica formal (requiere protocolo ético y hospital)
- Modo comparación antes/después de trombólisis

## Riesgos activos

Ver [riesgos.md](riesgos.md). Los tres que gobiernan el diseño y el calendario: R1 (datos), R2 (tolerancia al error) y R7 (degradación de landmarks en caras asimétricas).
