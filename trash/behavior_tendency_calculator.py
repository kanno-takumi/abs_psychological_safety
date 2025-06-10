# ABS/models/metrics/behavior_tendency_calculator.py
import numpy as np
from pprint import pprint

def speak_probability_calculator(agent):
    pprint(agent.__dict__)
    """
    発言確率（0〜1）：主体性、気分、メンタル、心理的安全性、信頼平均に基づく
    """
    style = (agent.style + 1) / 2
    mood = (agent.mood + 1) / 2
    mental = (agent.mental_strength + 1) / 2
    safety = (agent.agent_psychological_safety + 1) / 2
    trust_avg = (np.mean(list(agent.trust.values())) + 1) / 2
        
    return np.clip((style + mood + mental + safety + trust_avg) / 5, 0, 1)

def reaction_strength_calculator(agent):
    """
    意見に対する反応の強さ（0〜1）：主体性と心理的安全性に基づく
    """
    style = (agent.style + 1) / 2
    safety = (agent.agent_psychological_safety + 1) / 2
    return np.clip((style + safety) / 2, 0, 1)

def expressed_attitude_calculator(agent):
    """
    表出された態度（-1〜1）：潜在的態度 × 心理的安全性
    """
    latent_attitude = agent.attitude  # -1〜1
    safety = (agent.agent_psychological_safety + 1) / 2
    expressed = latent_attitude * safety
    return np.clip(expressed, -1, 1)
