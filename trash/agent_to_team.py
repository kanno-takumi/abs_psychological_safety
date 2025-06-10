import numpy as np

def __init__(n_agents, init_value=0.5):
    """
    個人→チームに対して持つ主観的な動的パラメータを初期化

    Returns:
        subjective_psych_safety: np.ndarray of shape (n_agents,)
        perceived_informal_climate: np.ndarray of shape (n_agents,)
    """
    agent_psychological_safety = np.full(n_agents, init_value)
    agent_casual_atmosphere = np.full(n_agents, init_value)
    return agent_psychological_safety, agent_casual_atmosphere
