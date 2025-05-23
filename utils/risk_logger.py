# ABS/utils/risk_logger.py
import numpy as np
import pandas as pd

def log_interpersonal_risk(step, agents):
    """
    対人リスク行列をログ形式に変換して返す（long形式）

    Parameters
    ----------
    step : int
        現在のシミュレーションステップ
    agents : list[Agent]
        全エージェント（interpersonal_risk 辞書を持つ）

    Returns
    -------
    pd.DataFrame
        columns: [step, from_id, to_id, risk]
    """
    records = []
    for i, agent_i in enumerate(agents):
        for j_id, risk in agent_i.interpersonal_risk.items():
            if j_id != agent_i.id:
                records.append({
                    "step": step,
                    "from_id": agent_i.id,
                    "to_id": j_id,
                    "risk": risk
                })
    return pd.DataFrame(records)
