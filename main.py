# ABS/main.py
import os, re, json
import numpy as np
import pandas as pd

from models.agent import Agent
from utils.utils_calc import (
    calc_hierarchies, calc_hierarchy_mean, calc_efficacy, calc_efficacy_mean,
    calc_risk, calc_risk_mean, calc_safety, calc_safety_mean, calc_speak_probability_mean,
    calc_reaction_probability, calc_agree_probability, calc_attitude_probability,
    speak_decision, speaker_decision, agree_to_speaker,
    reaction_decision, attitude_result, reactor_decision,
    update_efficacy, update_risk
)
from models.simulation import run_outer_loop
import utils.logger as logger
import make_graphs


# ----------------------------
# 入力
# ----------------------------
agents_file = input("エージェントファイル名：")  # 例: newagent.json

AGENTS_DIR  = "agents"
LOGS_ROOT   = "logs"
GRAPHS_ROOT = "graphs"
os.makedirs(AGENTS_DIR, exist_ok=True)
os.makedirs(LOGS_ROOT, exist_ok=True)
os.makedirs(GRAPHS_ROOT, exist_ok=True)

# ----------------------------
# エージェント読込と初期化
# ----------------------------
agents_file_path = os.path.join(AGENTS_DIR, agents_file)
with open(agents_file_path, "r", encoding="utf-8") as f:
    agents_data_list = json.load(f)

agents = [Agent(data, []) for data in agents_data_list]
for agent in agents:
    agent.hierarchies    = calc_hierarchies(0, 1, agent.id, agents)
    agent.hierarchy_mean = calc_hierarchy_mean(agent.hierarchies)
    agent.efficacy       = calc_efficacy(agent.hierarchies)
    agent.efficacy_mean  = calc_efficacy_mean(agent.efficacy)
    agent.risk           = calc_risk(agent.efficacy, agent.toughness, {}, t=0)
    agent.risk_mean      = calc_risk_mean(agent.risk)
     # safety = 1 - risk
    agent.safety    = calc_safety(agent.risk)
    agent.safety_mean = calc_safety_mean(agent.risk_mean)  
    agent.speak_probability_mean = calc_speak_probability_mean(1,1,1,agent.assertiveness,agent.extraversion,agent.risk_mean)
    agent.reaction_probability   = calc_reaction_probability(1,1,1,agent.id,agents)
    agent.agree_probability      = calc_agree_probability(agent.id,agents)
    agent.attitude_probability   = calc_attitude_probability(1,1,agent.id,agents)

# ----------------------------
# ロガー初期化 → シミュレーション実行（逐次 .jsonl に出力）
# ----------------------------
logger.init(agents_folder_='agents', agents_file_=agents_file, log_folder_='logs')
run_outer_loop(agents, 1000)  # run_outer_loop 内で utils.logger.log_step が呼ばれます

# ----------------------------
# ログパス取得（.jsonl）→ グラフJSONを書き出し
# ----------------------------
log_path = logger.log_filepath  # 例: logs/newagent/newagent_1.jsonl

# agent_id / run_id を抽出して graphs/<agent>/<agent>_<n>_*.json を作る
agent_dir = os.path.basename(os.path.dirname(log_path))          # newagent
file_base = os.path.splitext(os.path.basename(log_path))[0]      # newagent_1
m = re.match(rf"^{re.escape(agent_dir)}_(\d+)$", file_base)
run_id = int(m.group(1)) if m else 1

graph_dir = os.path.join(GRAPHS_ROOT, agent_dir)
os.makedirs(graph_dir, exist_ok=True)
graph_base_path = os.path.join(graph_dir, f"{agent_dir}_{run_id}")

# JSONL を読み込んでメトリクスを書き出し
# entries = make_graphs.load_jsonl(log_path)
# make_graphs.write_risk_mean_json(entries,         f"{graph_base_path}_risk_mean.json")
# make_graphs.write_safety_mean_json(entries, f"{graph_base_path}_psychological_safety_mean.json")
# make_graphs.write_efficacy_json(entries,     f"{graph_base_path}_efficacy.json")
# make_graphs.write_hierarchy_mean_json(entries,  f"{graph_base_path}_hierarchy_mean.json")

make_graphs.plot_params_self(f"{agent_dir}_{run_id}.jsonl")
make_graphs.plot_params_others(f"{agent_dir}_{run_id}.jsonl")