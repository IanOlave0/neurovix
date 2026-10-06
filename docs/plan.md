# Plan del proyecto — NeuroVix

> Fases, entregables y criterios de éxito. Última actualización: 2026-10-02.
> **Calendario realineado** con la ventana crítica de aplicaciones internacionales (ver `~/.config/opencode/planes/plan-investigacion-internacional.md`). NeuroVix se secuencia para *alimentar* las aplicaciones, no para competir con ellas.

## Objetivo doble

1. **Producto:** herramienta de apoyo al triaje temprano de ACV mediante cuantificación de asimetría facial, 100% on-device y sin hardware especial.
2. **Investigación:** artefacto publicable (preprint + repo público reproducible) que responda la pregunta del [protocolo](protocolo.md). Es la pieza insignia de portafolio para la ruta de investigación internacional (meta: OIST).

## Resumen de fases (calendario realineado)

| Fase | Ventana | Entregable principal | Meta de evidencia |
|---|---|---|---|
| 0. Planeación y literatura | 2–9 oct 2026 | Docs + arte previo mapeado | — |
| 1. MVP geométrico | 9–30 oct 2026 | Demo en vivo + índice de asimetría | Demo citable + resultados preliminares |
| 1.5. Mantenimiento | 1 nov – 16 dic 2026 | Literatura + robustez de landmarks + tareas pequeñas | Related work completo; sin experimentos grandes |
| 2. Protocolo experimental | 4 ene – 27 feb 2027 | Evaluación rigurosa + resultados | Tabla de resultados reproducible |
| 3. Redacción y publicación | 1 mar – 30 abr 2027 | Preprint + repo público | PDF público + repo reproducible |

## Regla de prioridad

Durante la **ventana de aplicaciones internacionales (nov–dic 2026)** estas tienen prioridad absoluta y NeuroVix entra en modo mantenimiento. Si el proyecto entra en conflicto con materias o deadlines externos, el proyecto cede.

## Fase 0 — Planeación y literatura (2–9 oct 2026)

- [x] Análisis contra el marco de 6 pruebas → [riesgos.md](riesgos.md)
- [x] Decisiones de diseño (copiloto, edge, núcleo geométrico)
- [x] Estructura de planeación en markdown
- [x] MCP paper-search conectado y verificado (PubMed/arXiv/bioRxiv/medRxiv/CrossRef)
- [x] Setup: `git init`, estructura de carpetas, entorno Python (repo público + `.venv` 3.11 + `requirements.txt` fijado + tests 4/4)
- [x] Revisión de literatura: barrido sistemático + related work inicial (9 fichas en docs/literatura.md; huecos R1/R3 confirmados)
- [x] Fichas de la bibliografía base (9 papers: 5 PubMed + 2 arXiv directos + 2 metodológicos; ver docs/literatura.md)

**Entregable:** este plan + protocolo + riesgos + related work inicial.

## Fase 1 — MVP geométrico (9–30 oct 2026)

- [ ] Pipeline de captura estable (OpenCV + MediaPipe FaceMesh)
- [ ] Módulo de landmarks con índices documentados (`landmarks.py`)
- [ ] Normalización: escala (interocular) y pose (roll/yaw)
- [ ] Línea base de reposo por sesión
- [ ] Gesto: sonrisa → índice de asimetría interpretable
- [ ] Demo en vivo: overlay de malla + métricas en tiempo real
- [ ] **Robustez R7:** sanity check de estabilidad de landmarks ante asimetría sintética controlada

**Criterio de terminado (DoD):** la demo corre en tiempo real en laptop, cuantifica asimetría inducida controladamente y documenta su comportamiento ante caras asimétricas. Cierre 30 oct: demo funcional + evidencia preliminar documentada.

## Fase 1.5 — Modo mantenimiento (1 nov – 16 dic 2026)

Prioridad absoluta: aplicaciones internacionales. NeuroVix se mantiene vivo sin competir:

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
- [ ] **Milestone:** resultados preliminares a inicios de febrero (insumo para ensayos de aplicación)

**DoD:** tabla de resultados reproducible con métricas, ablations y análisis de error.

## Fase 3 — Redacción y publicación (1 mar – 30 abr 2027)

- [ ] Preprint en inglés (formato arXiv)
- [ ] README en inglés + tests + reproducibilidad (semillas, versiones)
- [ ] Identificar venue y calendario de envíos (LatinX in AI @ NeurIPS · ML4H · IEEE EMBC student track)

**DoD:** PDF público + repo reproducible.
**Resultado esperado:** preprint disponible con margen para el ciclo de aplicaciones de otoño 2027.

## Backlog (post-v1)

- Clasificador ML como capa de producto (si la evidencia lo justifica)
- Empaquetado móvil (ONNX / TFLite)
- Extender a escala FAST completa (habla, debilidad de brazos)
- Validación clínica formal (requiere protocolo ético y hospital)
- Modo comparación antes/después de trombólisis

## Riesgos activos

Ver [riesgos.md](riesgos.md). Los tres que gobiernan el diseño y el calendario: R1 (datos), R2 (tolerancia al error) y R7 (degradación de landmarks en caras asimétricas).
