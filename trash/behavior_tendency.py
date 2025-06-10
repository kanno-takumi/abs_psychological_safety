import numpy as np

def init_behavior_tendency(n_agents, init_value=0.0):
    """
    行動傾向パラメータを初期化する。

    Returns
    -------
    speak_probability : np.ndarray
        発言確率ベクトル（n_agents）
    reaction_strength : np.ndarray
        意見に対する反応の強さベクトル（n_agents）
    expressed_attitude : np.ndarray
        表出された態度ベクトル（n_agents）
    """
    speak_probability = np.full(n_agents, init_value)
    reaction_strength = np.full(n_agents, init_value)
    expressed_attitude = np.full(n_agents, init_value)

    return speak_probability, reaction_strength, expressed_attitude
