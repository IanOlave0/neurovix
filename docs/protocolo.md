# Protocolo experimental — NeuroVix

> Diseño del estudio que convierte el MVP en artefacto de investigación. Versión 0.1 (borrador).

## 1. Pregunta de investigación

**RQ:** ¿En qué medida las features cinemáticas temporales (velocidad de gesto, retraso de inicio entre hemisferios, simetría de perfiles de movimiento) mejoran la discriminación de parálisis facial unilateral respecto a las métricas de asimetría estática?

**Hipótesis:**

- **H1:** El modelo con features cinemáticas supera al modelo estático (ΔAUC > 0) en validación con splits por sujeto.
- **H2:** El gesto de elevación de cejas permite distinguir afectación central (frente preservada) de periférica.
- **H3 (exploratoria):** El retraso de inicio (*onset lag*) entre hemisferios es la feature individual más discriminativa.

## 2. Definiciones operativas

- **Sujeto sano control:** sin antecedentes de parálisis facial ni síndromes neurológicos.
- **Asimetría inducida (síntesis):** deformación controlada de landmarks de un hemisferio con intensidad documentada. Sirve para pruebas de sensibilidad — **no** es verdad de campo clínica.
- **Línea base:** captura de reposo del propio sujeto al inicio de cada sesión; toda feature de gesto se expresa como delta contra el reposo.

## 3. Features

### 3.1 Landmarks (grupos de interés)

| Grupo | Estructura | Uso |
|---|---|---|
| Comisuras labiales | esquinas de boca, labio superior/inferior | Asimetría de sonrisa / mostrar dientes |
| Cejas | puntos medios y extremos | Central vs. periférica |
| Ojos | esquinas, párpados | Normalización de escala (interocular) |
| Contorno facial | mentón, mejillas | Normalización de pose |

> Nota técnica: fijar los índices exactos de MediaPipe FaceMesh en un módulo `landmarks.py` con constantes documentadas (los índices cambian entre versiones).

### 3.2 Familias de features

**Estáticas (por frame):**

- Distancias euclídeas entre pares contralaterales, normalizadas por distancia interocular
- Ángulos de desviación de comisuras respecto al eje medio facial
- Áreas triangulares de regiones faciales (órbita, boca)

**Cinemáticas (por gesto):**

- Velocidad por punto: `v_i(t) = ||p_i(t+Δt) − p_i(t)|| / Δt`
- Retraso de inicio entre hemisferios: lag de máxima correlación cruzada entre series de desplazamiento izquierda y derecha
- Simetría de perfiles: diferencia de velocidad máxima y duración del movimiento entre lados
- Amplitud del gesto por lado (desplazamiento máximo)

**Normalizaciones:**

- Escala: distancia interocular (o ancho facial)
- Pose: corrección de roll/yaw (matriz de transformación facial de MediaPipe o estimación por landmarks estables)
- Temporal: alineación del inicio de gesto por umbral de movimiento

### 3.3 Exclusiones

- No usar la coordenada *z* como feature primaria sin validar su estabilidad (profundidad monocular ruidosa).
- Descartar frames con pose fuera de rango (yaw/roll > umbral) u oclusiones (manos, lentes).

## 4. Estrategia de datos

| Fuente | Estado | Uso | Limitación explícita |
|---|---|---|---|
| Síntesis por deformación de landmarks | Disponible en Fase 2 | Pruebas de sensibilidad, calibración | Un "actor deformado" no reproduce la cinemática de un paciente |
| Proxy parálisis de Bell (datasets públicos) | A buscar (Mobus / HF / PubMed) | Señal de dominio, validación cruzada | Bell es periférica; no equivale a ACV central |
| Colaboración clínica | Stretch goal | Validación externa | Tiempos, ética, permisos |
| Grabaciones propias (equipo, con consentimiento) | Disponible | Desarrollo y sanity checks | No es evidencia clínica |

**Vía futura (post-Fase 2):** desidentificación que preserva movimiento
(SafeTriage, arXiv:2506.16578) como mecanismo para compartir cinemática
facial sin exponer identidades — ver `docs/literatura.md` F6.

**Regla:** cada resultado declara con qué fuente se obtuvo y qué **no** se puede afirmar.

## 5. Protocolo de evaluación

**Unidad de análisis:** sujeto (no frame). **Splits por sujeto** (GroupKFold) — jamás split aleatorio por frame (leakage de identidad).

**Métricas primarias:**

- Sensibilidad con especificidad fija al 90% (métrica de triaje)
- AUC de la curva ROC con IC 95% vía bootstrap agrupado por sujeto
- Calibración (curva de confiabilidad)

**Escalera de baselines (ablation):**

1. Regla geométrica simple (umbral en asimetría estática)
2. ML sobre features estáticas
3. ML sobre estáticas + cinemáticas ← propuesta
4. (Opcional) Modelo temporal secuencial como techo, si los datos lo justifican

**Análisis de error:** caracterización de falsos negativos. En triaje, el FN es el error crítico.

**Reproducibilidad:** semillas fijas, versiones de dependencias, script único de evaluación.

## 6. Ética y privacidad

- Procesamiento 100% on-device; ningún video o landmark sale del dispositivo.
- Consentimiento informado para cualquier grabación usada en desarrollo.
- La salida nunca es "no hay ACV": es un índice + recomendación de derivación (copiloto).
- Sin uso diagnóstico en personas reales hasta validación clínica formal.

## 7. Amenazas a la validez

| Amenaza | Tipo | Mitigación |
|---|---|---|
| Síntesis ≠ patología real | Constructo | Declararla explícitamente; buscar proxy clínico |
| Bell ≠ ACV | Externa | Limitar conclusiones a parálisis periférica cuando aplique |
| Confounders de captura (luz, pose, cámara) | Interna | Normalización + exclusiones + análisis por subgrupos |
| Desbalanceo extremo de clases | Estadística | Métricas robustas (sens@spec, AUC), ponderación |
| Comparaciones múltiples en ablations | Estadística | Pre-registrar la escalera de comparaciones |
