# Buyer / User Persona — NeuroVix

> Se construyen ambos. Quien decide/adopta y quien usa son distintos (igual que HIDRANEX BP-01/UP-01).

## BP-01 — Responsable coordinación emergencias / gestión tecnológica hospital (Buyer)

- Rol: decide piloto, firma convenio, responde a auditoría y comité. No usa la app en ambulancia.
- Objetivos: bajar tiempo inicio-notificación, evitar traslados secundarios, adherencia Código Cerebro/GPC, pasar CENETEC/LAASSP sin bloqueo [EV-12/EV-23].
- Dolores: presupuesto centralizado (816 equipos $11,257 MDP ref), falsas alarmas queman Código Cerebro, integración NOM-024, responsabilidad si SaMD sin autorización [EV-25/EV-26].
- Ganancias: tablero con hora inicio auto-sellada + checklist CAMALEÓN + trazabilidad [EV-09].
- Criterios compra: costo, confiabilidad, facilidad implementación, soporte, escalabilidad [análogo EV-08 HIDRANEX, aquí EV-23/EV-27].
- Fuentes: EV-12, EV-21/22/23, EV-24/25, EV-27.

## UP-01 — Paramédico TUM / enfermería triaje (User)

- Rol: usa en escena con sirena, guantes, luz mala, familia gritando. No firma contrato, sufre fricción.
- Objetivos: confirmar duda facial en <30seg, prenotificar con hora, no añadir papeleo NOM-004 [H a validar, EV-12 flujo].
- Dolores: encuadre perfecto imposible, typing imposible, offline intermitente, miedo culpa legal si sigue/no sigue app, alertas sin contexto se silencian [EV-26, H-operativa].
- Ganancias: 1 toque, sin teclear, offline, lenguaje "apoyo, verificar CAMALEÓN", registro auto [EV-26 antídoto].
- Fuentes: EV-09/12, EV-21/22, EV-26/27 + F-01/F-06 faltantes (declarados H).

## Calificación (misma vara que HIDRANEX, no auto-100)

| Criterio | BP-01 | UP-01 |
|---|---|---|
| Sustentado con evidencia verificable | 8/10 (LAASSP/CENETEC/NOMs/SaMD oficiales, falta willingness-to-pay F-03) | 7/10 (FAST/NIHSS/Código Cerebro sólidos, falta tasa error MX F-01 y override MX F-06) |
| Describe forma profunda y persistente | 7/10 (decisor colegiado, no una persona; falta organigrama piloto vs compra) | 8/10 (turno, guantes, ruido, rotación — persistente) |
| Corresponde realmente al problema | 9/10 (sin él no hay adopción) | 9/10 (sin él no hay uso) |
| **Total** | **80/100** | **80/100** |

## Cuándo usar cada uno

- BP-01: decisiones de alcance, presupuesto, legal, TCO, interoperabilidad, capacitación, SaMD, convenio vs licitación. Situación: comité, CENETEC, auditoría.
- UP-01: decisiones de UX, flujo escena, lenguaje, tiempo, offline, alerta con contexto. Situación: ambulancia, triaje, turno noche.
- Nunca mezclar: lo que tranquiliza al buyer (tablero) estorba al user (más taps).

## 3 decisiones concretas que el perfil obligó a tomar

BP-01 obligó a:
1. No vender accuracy, vender tiempo notificación + traslados evitados + adherencia (si no, no pasa comité).
2. Entrar como investigación educativa offline con convenio, sin interoperabilidad NOM-024 fase 1 (evita bloqueo CompraNet).
3. Incluir capacitación + mantenimiento + trazabilidad en TCO desde día 1.

UP-01 obligó a:
1. 1 toque, sin typing, offline, <30seg; si añade tiempo en ventana 4.5h/60min se abandona.
2. Lenguaje no-diagnóstico + sesgo FP + "verificar CAMALEÓN, prenotificar" (protege legal y evita falsa tranquilidad).
3. Alerta solo con zona+hora inicio+historial + hora auto-sellada; sin eso es ruido y se silencia (EV-26).
