# ABS/models/actions/speech_input_processor.py
import numpy as np

def broadcast_update_interpersonal_risk(speaker, agents):
    """
    スピーカーの発言によって他の全エージェントの対人リスクを更新する。
    各 i（≠speaker） に対して、risk[i][speaker.id] を更新する。

    Parameters
    ----------
    speaker : Agent
        発言を行ったエージェント（reaction_strength, expressed_attitudeを持つ）
    agents : list[Agent]
        全エージェントリスト（interpersonal_risk 辞書を持つ）
    """
    for receiver in agents:
        if receiver.id != speaker.id:
            delta = - (speaker.reaction_strength + speaker.expressed_attitude) / 2
            current = receiver.interpersonal_risk.get(speaker.id, 0.0)
            updated = np.clip(current + delta, -1, 1)
            receiver.interpersonal_risk[speaker.id] = updated
