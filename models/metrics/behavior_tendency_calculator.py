# ABS/models/metrics/behavior_tendency.py
import numpy as np

def speak_probability_calculator(agent):
    """
    発言確率（0〜1）：主体性、気分、メンタル、心理的安全性、信頼平均に基づく
    """
    style = (agent.style + 1) / 2
    mood = (agent.mood + 1) / 2
    mental = (agent.mental_strength + 1) / 2
    safety = (agent.agent_psychological_safety + 1) / 2
    if agent.trust:
        trust_avg = np.mean(list(agent.trust.values()))
        trust_avg = (trust_avg + 1) / 2
    else:
        trust_avg = 0.5

    return np.clip((style + mood + mental + safety + trust_avg) / 5, 0, 1)

def calc_expressed_attitude(agent_i):
    """
    表出された態度行列（i→j）：潜在的態度 × 心理的安全性
    """
    n = len(agent_i.trust)
    expressed_attitude = {}
    for j_id in agent_i.trust:
        latent_attitude = agent_i.attitude  # 個人の固定値（-1〜1）
        safety = agent_i.agent_psychological_safety  # -1〜1
        expressed = latent_attitude * ((safety + 1) / 2)  # 安全性が低いほど抑制
        expressed_attitude[j_id] = np.clip(expressed, -1, 1)
    return expressed_attitude

def calc_expressed_attitude(agent_i):
    """
    表出された態度行列（i→j）：潜在的態度 × 心理的安全性
    """
    n = len(agent_i.trust)
    expressed_attitude = {}
    for j_id in agent_i.trust:
        latent_attitude = agent_i.attitude  # 個人の固定値（-1〜1）
        safety = agent_i.agent_psychological_safety  # -1〜1
        expressed = latent_attitude * ((safety + 1) / 2)  # 安全性が低いほど抑制
        expressed_attitude[j_id] = np.clip(expressed, -1, 1)
    return expressed_attitude
