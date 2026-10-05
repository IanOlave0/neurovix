# CANVAS 0.2 — NeuroVix (revisado con evidencia)

> Cambia después de personas, empatía y valor. Solo lo validado.

## Cambios vs 0.1

- "Universidades" → IES no aplica; aquí: hospitales 2º/3er nivel con Código Cerebro + prehospitalario 911/Cruz Roja [EV-12].
- "App con IA" → reglas simples primero (umbral ángulo/desviación + CAMALEÓN); ML solo si H-cinemática supera baseline [EV-17/18].
- "Usuario=cliente" → BP-01 decide, UP-01 usa [02-buyer-user.md].
- "Alerta=solución" → alerta solo con zona facial + hora inicio + contexto + historial + tier severidad [EV-26].
- "Un solo lienzo" → dos lienzos [04-propuesta-valor.md].
- "Ya es viable" → no; persisten H críticas + F-01…F-06 + SEC/Legal.

## CANVAS 0.2 breve

- Segmentos: prehospitalario + triaje con Código Cerebro [EV-12].
- Valor buyer: minutos + adherencia + trazabilidad para comité [EV-06/EV-22].
- Valor user: duda resuelta en <30seg offline sin typing [EV-09/EV-26].
- Canales: convenio investigación, capacitación turno [H-03].
- Ingresos: H-03 por indicadores, no por licencia IA.
- Recursos: Landmarker 478 LIVE_STREAM CPU, landmarks.py, checklist CAMALEÓN [EV-14/15].
- Actividades: validar landmarks en asimetría [EV-16], síntesis + proxy Bell con límites [EV-20], splits por sujeto sens@spec90 AUC [protocolo].
- Socios: IMSS/Cruz Roja, CENETEC, ética [EV-23].
- Costos: validación + capacitación + MDM + SaMD [EV-25].

## Métricas TI I define, TI II mide (metas didácticas, no resultados)

- M-01 detección ≤5min anomalía inducida; M-02 sens ≥90%; M-03 FP ≤10% piloto; M-04 zona ≥85%; M-05 entrega ≥95%; M-06 disp ≥99% piloto; M-07 diagnóstico ≥30% menor vs base; M-08 SUS ≥75; M-09 TCO acordado; M-10 autonomía si batería (análogo HIDRANEX p.26, adaptado).

## Viabilidad + SEC

- Técnica: CPU factible [EV-15]; riesgo degradación [EV-16] + no-dataset [EV-20].
- Operativa: gradual por convenio, tickets/flujo 911 existente [EV-12].
- Económica/legal/ética: LAASSP/CENETEC [EV-23]; LFPDPPP 2025 consentimiento escrito sensible [EV-24]; SaMD probable [EV-25]; NOM-004/024/034 [EV-21/22]; sesgo tez/edad/lengua a validar.
- SEC-01…07 desde diseño: identidad dispositivo, cifrado tránsito/reposo (Keystore/Keychain), mínimo privilegio, rotación credenciales, firmware/modelo firmado, log anonimizado, threat model + respuesta incidentes (aunque offline, OWASP MASVS + borrado selectivo + MDM).

## Cierre TI I (igual que HIDRANEX)

Dejar fundamentado POR QUÉ vale la pena, QUÉ se desarrollará y CÓMO se validará en TI II. Definir métricas ≠ haber demostrado resultados.

## Pregunta final (para tu entrega)

¿Qué cambió después de investigar y por qué? Respuesta lista: de "detector IA" a "copiloto CAMALEÓN objetivo on-device que auto-sella hora y prenotifica con contexto, con reglas primero y ML solo si supera baseline, entrando por convenio investigación por riesgo SaMD/datos" — cambios trazados a EV-04/06/09/11/12/14-16/20/23-26.
