# ABS/main.py
import numpy as np
# from models.metrics.behavior_tendency_calculator import (
#     speak_probability_calculator, reaction_strength_calculator, expressed_attitude_calculator
# )
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
from utils.utils_calc import calc_risk_mean
from utils.utils_calc import calc_speak_probability
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
# from utils.logger import log_step




#JSON読み込み
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
    agent.speak_probability_mean = calc_speak_probability(1,1,1,agent.assertiveness,agent.extraversion,agent.risk_mean)
    agent.reaction_probability = calc_reaction_probability(1,1,1,agent.id,agents)
    agent.agree_probability = calc_agree_probability(agent.id,agents)
    agent.attitude_probability = calc_attitude_probability(1,1,agent.id,agents)

# logs = []
run_outer_loop(agents,10) 
# speak_dict = {}    
# for agent in agents:
#     speak = speak_decision(agent.speak_probability_mean)
#     speak_dict[agent.id] = speak #agent.idをキーに発言を格納
#     print(f"Agent{agent.id} ：{speak}")

#agent中身の出力
# for agent in agents:
    # print(agent)

# speaker_id = speaker_decision(speak_dict)
# print(f"speaker：agent{speaker_id}")

# reaction_dict = {}
# agree_dict = {}
# attitude_dict = {}


# for agent in agents:
#     agree = agree_to_speaker(agent,speaker_id,0.1)
#     agree_dict[agent.id] = agree
#     reaction = reaction_decision(agent,speaker_id,agree)
#     reaction_dict[agent.id] = reaction
#     attitude = attitude_result(agent.attitude_probability,speaker_id)
#     attitude_dict[agent.id] = attitude
    
#     print("agent",agent.id,":agree",agree)
#     print("agent",agent.id,":reaction",reaction)
#     print("agent",agent.id,"attitude", attitude)
    
# reactor_id = reactor_decision(reaction_dict)
# print(f"reaction_dict:{reaction_dict}")
# print(f"agree_dict:{agree_dict}")

# print(f"reactor_id：{reactor_id}")
# reactor_agree = list(agree_dict[reactor_id].values())[0]
# reactor_attitude = list(attitude_dict[reactor_id].values())[0]
# print(f"reactor agree: {reactor_agree}")
# speaker = next(agent for agent in agents if agent.id == speaker_id)
# reactor = next(agent for agent in agents if agent.id == reactor_id)
# old_efficacy, updated_efficacy = update_efficacy(speaker,reactor,reactor_agree,0.5,0.5)
# print(f"old_efficacy:{old_efficacy},new_efficacy:{updated_efficacy}")

# old_risk, updated_risk = update_risk(speaker,reactor,reactor_attitude,0.5,0.5,0.5)
# print(f"old_risk:{old_risk},updated_risk:{updated_risk}")

# print(run_inner_loop(agents))
# log,t = 

# print(t)
# print(log)
# print(run_outer_loop(agents,1000))