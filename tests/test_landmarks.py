"""Red de seguridad del modulo de landmarks (riesgo R7).

Estos tests no necesitan camara: verifican invariantes de la topologia.
Si un upgrade de `mediapipe` mueve los indices, ESTO falla primero,
no el pipeline clinico.
"""

from src.landmarks import EYES, MOUTH, N_LANDMARKS, validar_indices


def test_malla_completa():
    assert N_LANDMARKS == 468


def test_indices_en_rango_y_sin_duplicados():
    validar_indices()  # lanza AssertionError con el detalle


def test_grupos_simetricos():
    # Cada lado aporta el mismo numero de puntos: la asimetria que midamos
    # debe venir de la cara, no de un grupo mal definido.
    assert len([k for k in EYES if k.startswith("left")]) == len(
        [k for k in EYES if k.startswith("right")]
    )
    assert len([k for k in MOUTH if "left" in k or "right" in k]) == 2


def test_ojos_y_boca_no_se_solapan():
    assert not set(EYES.values()) & set(MOUTH.values())
