

# ABS/main.py
import numpy as np
from models.params.behavior_tendency import init_behavior_tendency
from models.params.agent_to_other import init_trust_and_risk
from models.metrics.behavior_tendency_calculator import (
    calc_speak_probability, calc_reaction_strength, calc_expressed_attitude
)
from models.actions.speech_input_processor import broadcast_update_interpersonal_risk
from utils.risk_logger import log_interpersonal_risk
import pandas as pd
#main.py や simulate.py で次のようにインポート
import config.simulation_config as cfg

# 1. 初期設定
N_AGENTS = 5
N_STEPS = 500

# 仮のAgentクラス（本番は各自のAgent定義に置き換え）
class Agent:
    def __init__(self, id):
        self.id = id
        self.style = np.random.uniform(-1, 1)
        self.mood = np.random.uniform(-1, 1)
        self.mental_strength = np.random.uniform(-1, 1)
        self.attitude = np.random.uniform(-1, 1)
        self.agent_psychological_safety = np.random.uniform(-1, 1)
        self.trust, self.interpersonal_risk = init_trust_and_risk(N_AGENTS)
        self.speak_probability = 0.0
        self.reaction_strength = 0.0
        self.expressed_attitude = 0.0

# エージェント生成
agents = [Agent(id=i) for i in range(N_AGENTS)]

# 初期化
speak_p, reaction_s, expressed_a = init_behavior_tendency(N_AGENTS)
for i, agent in enumerate(agents):
    agent.speak_probability = speak_p[i]
    agent.reaction_strength = reaction_s[i]
    agent.expressed_attitude = expressed_a[i]

# ログ格納リスト
risk_log = []

# 2. シミュレーションループ
for step in range(N_STEPS):
    for agent in agents:
        # 発言するかを判定
        agent.speak_probability = calc_speak_probability(agent)
        if np.random.rand() < agent.speak_probability:
            agent.reaction_strength = calc_reaction_strength()
            agent.expressed_attitude = calc_expressed_attitude(agent)
            broadcast_update_interpersonal_risk(agent, agents)

    # ログ記録
    step_log = log_interpersonal_risk(step, agents)
    risk_log.append(step_log)

# 3. ログ出力（例：CSV保存）
all_logs = pd.concat(risk_log, ignore_index=True)
all_logs.to_csv("output/interpersonal_risk_log.csv", index=False)
