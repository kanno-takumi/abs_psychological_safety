import numpy as np
from models.metrics.behavior_tendency_calculator import (
    calc_reaction_strength,
    calc_expressed_attitude
)

def attempt_speech(agent):
    """
    エージェントがこの時間単位（例：1分）で発言するかを判定し、
    発言する場合は内容を返す。
    
    Returns
    -------
    dict or None
    """
    if np.random.rand() < agent.speak_probability:
        return {
            "speaker_id": agent.id,
            "reaction_strength": calc_reaction_strength(),
            "expressed_attitude": calc_expressed_attitude(agent)
        }
    else:
        return None
