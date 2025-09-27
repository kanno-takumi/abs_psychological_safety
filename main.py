# ABS/main.py
import numpy as np
# from models.metrics.behavior_tendency_calculator import (
#     speak_probability_calculator, reaction_strength_calculator, expressed_attitude_calculator
# )
import pandas as pd
#main.py や simulate.py で次のようにインポート
import os
#JSON読み込み
import json
import numpy as np
from models.agent import Agent
from utils.utils_calc import calc_hierarchies
from utils.utils_calc import calc_hierarchy_mean
from utils.utils_calc import calc_efficacy
from utils.utils_calc import calc_risk
from utils.utils_calc import calc_risk_mean
from utils.utils_calc import calc_speak_probability_mean
from utils.utils_calc import calc_reaction_probability
from utils.utils_calc import calc_agree_probability
from utils.utils_calc import calc_attitude_probability
from utils.utils_calc import speak_decision
from utils.utils_calc import speaker_decision
from utils.utils_calc import agree_to_speaker
from utils.utils_calc import reaction_decision
from utils.utils_calc import attitude_result
from utils.utils_calc import reactor_decision
from utils.utils_calc import update_efficacy
from utils.utils_calc import update_risk
from models.simulation import run_inner_loop
from models.simulation import run_outer_loop
import utils.logger as logger
import makegraph




#JSON読み込み
# 入力を促す
agents_file = input("エージェントファイル名：")  # 例: 5agents_ver4.json
agents_folder = "agents_data"
agents_file_path = os.path.join(agents_folder, agents_file)

log_folder = "simulate_log"
log_file_path = os.path.join(log_folder,agents_file)

graph_folder = "simulate_graph"
graph_path_tmp = os.path.join(graph_folder,agents_file)
name, ext = graph_path_tmp.rsplit(".", 1)
graph_path = f"{name}.pdf"

with open(agents_file_path, "r") as f:
    agents_data_list = json.load(f)
    
#出力パスの設定
logger.init(agents_folder_=log_folder, agents_file_=agents_file, log_folder_=log_folder)  

#agentsの作成
agents = []
N = len(agents_data_list)  # 人数に応じて自動設定
for agent_data in agents_data_list:
    agent = Agent(agent_data, agents)  #Agentクラスはdata(dict), num(人数)を受け取れるように
    agents.append(agent)
    
#agentの中にパラメータとしてhierarchy,hierarchiesという要素を追加
for agent in agents:
    agent.hierarchy_mean = calc_hierarchy_mean(0,1,agent.id,agents)
    agent.hierarchies = calc_hierarchies(0, 1, agent.id, agents)

#t=0の場合、動作確認済。
for agent in agents:
    agent.efficacy = calc_efficacy(agent.hierarchies)
# print("calc_efficacy:",calc_efficacy(0.5,0.5,agents[0].hierarchies,{},{},{},t=0))

#agentの中にパラメータとしてriskという要素を追加
for agent in agents:
    agent.risk = calc_risk(agent.efficacy,agent.toughness,{},t=0)
    agent.risk_mean = calc_risk_mean(agent.risk)

"""
ここまでは初期値。
ここからはループを使う？はず。
まずはループなしで動くか試す。
"""

for agent in agents:
    agent.speak_probability_mean = calc_speak_probability_mean(1,1,1,agent.assertiveness,agent.extraversion,agent.risk_mean)
    agent.reaction_probability = calc_reaction_probability(1,1,1,agent.id,agents)
    agent.agree_probability = calc_agree_probability(agent.id,agents)
    agent.attitude_probability = calc_attitude_probability(1,1,agent.id,agents)

# logs = []
run_outer_loop(agents,1000) 
 
log_entries = makegraph.get_log_entries(log_file_path)
makegraph.plot_risk(log_entries,graph_path)
makegraph.plot_psychological_safety(log_entries,graph_path)
makegraph.plot_hierarchy(log_entries,graph_path)

# print(log_entries[0]["agents"][0])