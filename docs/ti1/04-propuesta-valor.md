# Propuesta de valor — por perfil

> Un lienzo por perfil, trazado a empatía. Evaluado con puntaje (no 100).

## Lienzo BP-01 (Buyer)

- Tareas: lograr meta puerta-aguja ≤60min, justificar piloto ante comité/CENETEC, evitar auditoría [EV-06/EV-23].
- Dolores: falsas alarmas, costo oculto, bloqueo CompraNet, riesgo SaMD [EV-25/EV-26].
- Ganancias: tablero tiempos, adherencia Código Cerebro, convenio ligero [EV-12].
- Aliviadores: modo investigación offline sin interoperabilidad fase 1; trazabilidad completa; etiqueta "apoyo, no diagnóstico" + ruta SaMD declarada [EV-22/EV-25].
- Creadores: reporte "minutos ahorrados + traslados evitados" (umbrales Reimer 2020 como ref, no promesa) [H].
- Productos: dashboard web + informe piloto con M-01…M-10 definidos antes [ver Canvas 0.2].

**Encaje: 84/100** — encaje lógico bueno, pero ganancias/TCO y evidencia willingness-to-pay aún débiles (F-03).

## Lienzo UP-01 (User)

- Tareas: decidir prenotificación en <30seg con duda facial [H + EV-10].
- Dolores: typing, señal, luz, culpa legal, alerta sin contexto [EV-26].
- Ganancias: checklist CAMALEÓN 10seg, hora auto, video-no-sale [EV-09/EV-24].
- Aliviadores: 1 toque, offline, lenguaje no-autónomo, solo alta severidad interrumpe (tier) [EV-26 AHRQ].
- Creadores: overlay malla + índice interpretable (ángulo/desviación) + delta vs reposo [EV-17/18 + docs/protocolo.md].
- Productos: app Android (Landmarker 478, CPU) + módulo landmarks.py + exclusión yaw/roll>umbral, sin z como primaria [EV-14/15 + protocolo].

**Encaje: 88/100** — perfil uso mejor sustentado (FAST/NIHSS/CAMALEÓN + degradación conocida EV-16); falta probar experiencia en escena real (F-01/F-06) y validar onset lag (F-04).

## Regla
Dos lienzos separados. No mezclar. ML solo si H-cinemática supera reglas simples en splits por sujeto (docs/protocolo.md escalera ablations).
