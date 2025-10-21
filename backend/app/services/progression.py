from dataclasses import dataclass
from typing import List, Optional

# -------------------------------------------------------------
# 🏋️‍♂️ MODELOS DE DATOS INTERNOS
# -------------------------------------------------------------

@dataclass
class SetLog:
    """Registro de una serie individual de entrenamiento"""
    reps: int
    weight: float
    rir: Optional[int] = None
    rpe: Optional[float] = None


@dataclass
class Suggestion:
    """Resultado de la recomendación"""
    next_weight: float
    reason: str

# -------------------------------------------------------------
# 🧠 FUNCIÓN DE RECOMENDACIÓN
# -------------------------------------------------------------

def recommend_next(
    history: List[List[SetLog]],
    rep_min: int = 6,
    rep_max: int = 10,
) -> Suggestion:
    """
    Analiza las últimas sesiones y sugiere la siguiente carga de peso.
    Usa una regla de sobrecarga progresiva simple.
    """

    if not history:
        return Suggestion(next_weight=20.0, reason="Sin historial, empezamos con peso base 20 kg")

    last_session = history[-1]
    if not last_session:
        return Suggestion(next_weight=20.0, reason="Última sesión vacía, peso base 20 kg")

    # Cálculo básico: promedio de peso de la última sesión
    avg_weight = sum(s.weight for s in last_session) / len(last_session)
    avg_reps = sum(s.reps for s in last_session) / len(last_session)

    # Regla sencilla:
    if avg_reps >= rep_max:
        next_w = round(avg_weight * 1.025, 1)
        return Suggestion(
            next_weight=next_w,
            reason=f"Subimos un 2.5 % (de {avg_weight} kg a {next_w} kg) porque hiciste {avg_reps:.0f} reps promedio."
        )
    elif avg_reps < rep_min:
        next_w = round(avg_weight * 0.975, 1)
        return Suggestion(
            next_weight=next_w,
            reason=f"Bajamos un 2.5 % (de {avg_weight} kg a {next_w} kg) porque hiciste {avg_reps:.0f} reps promedio."
        )
    else:
        return Suggestion(
            next_weight=avg_weight,
            reason=f"Mantenemos {avg_weight} kg; rango ideal {rep_min}-{rep_max} reps (hiciste {avg_reps:.0f})."
        )
