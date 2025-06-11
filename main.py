# ABS/main.py
import numpy as np
# from models.metrics.behavior_tendency_calculator import (
#     speak_probability_calculator, reaction_strength_calculator, expressed_attitude_calculator
# )
from models.actions.speech_input_processor import broadcast_update_interpersonal_risk
from utils.risk_logger import log_interpersonal_risk
import pandas as pd
#main.py や simulate.py で次のようにインポート
import config.simulation_config as cfg
import os
#JSON読み込み
import json
import numpy as np
from models.initializer.agent import Agent
from utils.utils_calc import calc_hierarchies
from utils.utils_calc import calc_hierarchy
from utils.utils_calc import calc_efficacy
from utils.utils_calc import calc_risk

# JSON読み込み
agents_file_data = "newagent.json"
agents_file_path = os.path.join("data", agents_file_data)
with open(agents_file_path, "r") as f:
    agents_data_list = json.load(f)

#agentsの作成
agents = []
N = len(agents_data_list)  # 人数に応じて自動設定
for agent_data in agents_data_list:
    agent = Agent(agent_data, agents)  #Agentクラスはdata(dict), num(人数)を受け取れるように
    agents.append(agent)
    
#agentの中にパラメータとしてhierarchy,hierarchiesという要素を追加
for agent in agents:
    agent.hierarchy = calc_hierarchy(0.5,0.5,agent.id,agents)
    agent.hierarchies = calc_hierarchies(0.5, 0.5, agent.id, agents)

#t=0の場合、動作確認済。
for agent in agents:
    agent.efficacy = calc_efficacy(0.5,0.5,agent.hierarchies,{},{},{},t=0)
# print("calc_efficacy:",calc_efficacy(0.5,0.5,agents[0].hierarchies,{},{},{},t=0))

#agentの中にパラメータとしてriskという要素を追加
for agent in agents:
    agent.risk = calc_risk(agent.efficacy,agent.toughness,{},t=0)
# 出力確認
# print("agent:",agent)

for agent in agents:
    print(agent)

#"metrics"の関数に代入
## 類似度計算
# from models.metrics.agent_to_other_calculator import calc_similarity
# similarity = calc_similarity(agents[0],agents[1])
# print(similarity)
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
