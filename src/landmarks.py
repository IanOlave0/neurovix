"""Grupos de landmarks de MediaPipe FaceMesh usados por NeuroVix.

Diseno deliberado (ver docs/protocolo.md, seccion 3.1 y riesgo R7):
- Los indices viven AQUI como constantes con nombre, nunca como numeros
  magicos regados en el codigo. Si MediaPipe cambia la topologia entre
  versiones, hay UN solo lugar que auditar.
- `validar_indices()` es la red de seguridad: cualquier upgrade de
  dependencias que mueva un indice rompe los tests, no el diagnostico.

Indices canonicos de la topologia FaceMesh (468 puntos), verificados contra
la documentacion de la malla. Al actualizar `mediapipe`, revalidar este
modulo corriendo la suite: `pytest tests/ -v`.
"""

N_LANDMARKS = 468

# Punta de la nariz (referencia del eje medio facial).
NOSE_TIP = 1
# Menton (contorno inferior).
CHIN = 152

# Ojos: esquinas externa e interna de cada lado.
# La distancia interocular derivada de estos puntos es la unidad de
# normalizacion de escala (protocolo, seccion 3.2).
LEFT_EYE_OUTER = 33
LEFT_EYE_INNER = 133
RIGHT_EYE_INNER = 362
RIGHT_EYE_OUTER = 263

# Boca: comisuras y centros labiales (gesto de sonrisa / mostrar dientes).
MOUTH_LEFT = 61
MOUTH_RIGHT = 291
UPPER_LIP = 13
LOWER_LIP = 14

EYES = {
    "left_outer": LEFT_EYE_OUTER,
    "left_inner": LEFT_EYE_INNER,
    "right_inner": RIGHT_EYE_INNER,
    "right_outer": RIGHT_EYE_OUTER,
}

MOUTH = {
    "left_corner": MOUTH_LEFT,
    "right_corner": MOUTH_RIGHT,
    "upper_lip": UPPER_LIP,
    "lower_lip": LOWER_LIP,
}

# TODO(Fase 1): grupos de cejas y contorno para el gesto de elevacion de
# cejas (discriminacion central vs. periferica, hipotesis H2).


def validar_indices() -> None:
    """Falla rapido si un indice sale del rango de la malla."""
    todos = [NOSE_TIP, CHIN, *EYES.values(), *MOUTH.values()]
    assert len(todos) == len(set(todos)), "indices duplicados en landmarks.py"
    fuera = [i for i in todos if not 0 <= i < N_LANDMARKS]
    assert not fuera, f"indices fuera de rango [0, {N_LANDMARKS}): {fuera}"
