# ABS/main.py
import numpy as np
from models.metrics.behavior_tendency_calculator import (
    speak_probability_calculator, reaction_strength_calculator, expressed_attitude_calculator
)
from models.actions.speech_input_processor import broadcast_update_interpersonal_risk
from utils.risk_logger import log_interpersonal_risk
import pandas as pd
#main.py や simulate.py で次のようにインポート
import config.simulation_config as cfg
import os
#JSON読み込み
import json
import numpy as np
from models.params.agent import Agent

# JSON読み込み
agent_file_data = "agent1.json"
agent_file_path = os.path.join("data", agent_file_data)
with open(agent_file_path, "r") as f:
    data = json.load(f)

# numは1人でもとりあえず仮で2以上（他者用の配列を持たせるため）
agent = Agent(data, num=2)


# 出力確認
# print("agent:",agent)
print(f"ID: {agent.id}, Gender: {agent.gender}, Age: {agent.age}")
print(f"Value to CN: ({agent.value_x}, {agent.value_y})")
print(f"Knowledge: {agent.knowledge}")
print(f"Trust shape: {agent.trust_or_resignation.shape}")



# # 2. シミュレーションループ
# for step in range(N_STEPS):
#     for agent in agents:
#         # 発言するかを判定
#         agent.speak_probability = speak_probability_calculator(agent)
#         if np.random.rand() < agent.speak_probability:
#             agent.reaction_strength = reaction_strength_calculator()
#             agent.expressed_attitude = expressed_attitude_calculator(agent)
#             broadcast_update_interpersonal_risk(agent, agents)

#     # ログ記録
#     step_log = log_interpersonal_risk(step, agents)
#     risk_log.append(step_log)

# # 3. ログ出力（例：CSV保存）
# all_logs = pd.concat(risk_log, ignore_index=True)
# all_logs.to_csv("output/interpersonal_risk_log.csv", index=False)
