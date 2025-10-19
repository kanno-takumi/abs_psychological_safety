# makegraph.py
import os, json
from pathlib import Path
from typing import Optional, Any, Dict, List
from collections import defaultdict
import re
import json
import matplotlib.pyplot as plt
import pandas as pd

# ===== ログ読み込み（JSONL） =====
# def load_jsonl(log_path: str):
#     if not os.path.exists(log_path):
#         raise FileNotFoundError(f"Log file not found: {log_path}")
#     entries = []
#     with open(log_path, "r", encoding="utf-8") as f:
#         for line in f:
#             line = line.strip()
#             if not line:
#                 continue
#             obj = json.loads(line)
#             if isinstance(obj, dict) and obj.get("type") == "meta":
#                 continue
#             entries.append(obj)
#     return entries

# # ===== 汎用：縦持ちデータを書き出す =====
# def _write_metric_long(entries, out_path: str, metric_key: str, transform=None, agent_label_prefix=""):
#     """
#     entries: load_jsonl の結果
#     metric_key: agent辞書から取り出すキー（例: "risk_mean", "efficacy", "hierarchies" など）
#     transform: 取得値に変換をかける関数。Noneならそのまま（例: psy = 1 - risk）
#     出力スキーマ(長い形式):
#     {
#       "meta": {"metric": "..."},
#       "data": [{"time": t, "agent_id": <id>, "value": <number or array>, "label": "Agent <id>"} ...]
#     }
#     """
#     rows = []
#     for entry in entries:
#         t = entry.get("time1")
#         for a in entry.get("agents", []):
#             val = a.get(metric_key, None)
#             if transform is not None:
#                 val = transform(val, agent=a, time=t)
#             rows.append({
#                 "time": t,
#                 "agent_id": a.get("id"),
#                 "value": val,
#                 "label": f"{agent_label_prefix}{a.get('id')}"
#             })

#     # 空ならスキップ
#     non_null = any(r["value"] is not None for r in rows)
#     if not non_null:
#         print(f"[WARN] No data for metric '{metric_key}'. Skip writing {out_path}")
#         return

#     out = {"meta": {"metric": metric_key}, "data": rows}
#     os.makedirs(os.path.dirname(out_path), exist_ok=True)
#     with open(out_path, "w", encoding="utf-8") as f:
#         json.dump(out, f, ensure_ascii=False, indent=2)
#     print(f"[SAVE] {out_path}")

# # ===== 各メトリクス =====
# def write_risk_mean_json(entries, out_path: str, agent_label_prefix=""):
#     # metric: risk_mean（0-1想定）
#     _write_metric_long(entries, out_path, metric_key="risk_mean", transform=None, agent_label_prefix=agent_label_prefix)

# def write_safety_mean_json(entries, out_path: str, agent_label_prefix=""):
#     # metric: psych_safety = 1 - risk_mean
#     _write_metric_long(entries, out_path, metric_key="safety_mean", transform=None, agent_label_prefix=agent_label_prefix)

# def write_efficacy_json(entries, out_path: str, agent_label_prefix=""):
#     # metric: efficacy
#     _write_metric_long(entries, out_path, metric_key="efficacy", transform=None, agent_label_prefix=agent_label_prefix)

# def write_hierarchy_mean_json(entries, out_path: str, agent_label_prefix=""):
#     # metric: hierarchies（配列/辞書でもOK。value にそのまま入れる）
#     _write_metric_long(entries, out_path, metric_key="hierarchy_mean", transform=None, agent_label_prefix=agent_label_prefix)






# ---------------------------グラフ------------------------------
# make_graphs_from_logs.py

# =========================== ログのパスの取得 ===========================

def get_log_path(file_name):
    """
    logs/{file_name の末尾の _数字 を除いたベース}/{file_name} を返す

    例:
      "newagent_5.json"        -> "logs/newagent/newagent_5.json"
      "newagent.json"          -> "logs/newagent/newagent.json"
      "configs/newagent_5.json"-> "logs/newagent/newagent_5.json"
    """
    name = Path(file_name).name           # 例: "newagent_5.json"
    stem = Path(name).stem                # 例: "newagent_5"
    m = re.match(r'^(.*?)(?:_\d+)?$', stem)
    base = m.group(1) if m else stem      # 例: "newagent"
    return str(Path("logs") / base / name)
    
# =========================== 読み込み ==================================
def get_log_entries(file_name):
    log_path = get_log_path(file_name)
    if not os.path.exists(log_path):
        print(f"Error: File '{log_path}' does not exist.")
        exit(1)

    log_entries = []
    with open(log_path, 'r') as f:
        for line in f:
            log_entries.append(json.loads(line))
    return log_entries

#=================== 出力されるパス ==================
def build_graph_path(file_name, param, i=None, ext="png"):
    # ファイル名と拡張子を分離
    file_name = Path(file_name).name           # 例: "newagent_5.json"
    stem = Path(file_name).stem                # 例: "newagent_5"
    m = re.match(r'^(.*?)(?:_\d+)?$', stem)
    # ベース部分（_で区切った最初の部分）
    base = m.group(1)              # "newagent"
    # 出力ディレクトリ
    out_dir = Path("graphs") / base / stem
    out_dir.mkdir(parents=True, exist_ok=True)
    
    
    # 出力ファイル
    fname = f"{param}_i{i}.{ext}" if i is not None else f"{param}.{ext}"
    return str(out_dir / fname)
    # return os.path.join(out_dir, f"{param}.png")
    

# =========================== グラフ ===========================

self_params = ("hierarchy_mean","efficacy_mean", "risk_mean", "safety_mean", "speak_probability_mean")
others_params = ("hierarchies", "efficacy", "risk", "safety", "reaction_probability", "agree_probability", "attitude_probability")

def plot_params_self(file_name):
    """file_name（例: logs/newagent/newagent_3.jsonl）からSELF_PARAMSだけ描画"""
    logs = get_log_entries(file_name)

    # 1つのDataFrameにまとめる（SELF_PARAMSだけ拾う）
    rows = []
    for e in logs:
        t = e["time1"]
        for a in e["agents"]:
            row = {"time": t, "agent_id": a["id"]}
            for k in self_params:
                if k in a:
                    row[k] = a[k]
            rows.append(row)
            #分岐してothers_paramsに対してforとifを回す、
    if not rows:
        return

    df = pd.DataFrame(rows)

    # パラメータごとに描画（存在しなければスキップ）
    for param in self_params:
        if param not in df:
            continue
        pivot = df.pivot(index="time", columns="agent_id", values=param).sort_index()
        if pivot.dropna(how="all").empty:
            continue
        ax = pivot.plot(figsize=(10,6), ylim=(0,1), grid=True, legend=True)
        ax.set_xlabel("Time Step (t1)")
        ax.set_ylabel(param)
        # ax.set_title(param)
        out_path = build_graph_path(os.path.basename(file_name), param)  # あなたの関数を使用
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()
        
        
def plot_params_others(file_name):
    """
    JSONLログ file_name から、others_params を
    i（主エージェント）ごとに1枚のグラフで出力する。
    各グラフには j（対エージェント）系列をまとめて描画。
    出力パスは build_graph_path(file_name, f"{param}_i{i}")。
    """
    logs = get_log_entries(file_name)
    rows = []
    for e in logs:
        t = e["time1"]
        for a in e["agents"]:
            row = {"time": t, "agent_id": a["id"]}
            for k in self_params:
                if k in a:
                    row[k] = a[k]
            rows.append(row)
            #分岐してothers_paramsに対してforとifを回す、
    if not rows:
        return

    df = pd.DataFrame(rows)

    for param in others_params:
        # --- rows 構築: time, i(主), j(相手), value ---
        rows = []
        for e in logs:
            t = e.get("time1")
            for a in e.get("agents", []):
                i_val = a.get("id")
                d = a.get(param)
                if not isinstance(d, dict):  # others_params は辞書を想定
                    continue
                for j_key, val in d.items():
                    rows.append({
                        "time": t,
                        "i": i_val,
                        "j": j_key,
                        "value": val
                    })

        if not rows:
            continue  # データが無ければ次へ

        df = pd.DataFrame(rows).dropna(subset=["value"])
        if df.empty:
            continue

        # --- i ごとに1枚、j を複数系列として描画 ---
        for i_val, df_i in df.groupby("i"):
            df_i = df_i.sort_values(["time", "j"])
            plt.figure(figsize=(10, 6))
            for j_val, df_ij in df_i.groupby("j"):
                df_ij = df_ij.sort_values("time")
                if df_ij["value"].isna().all():
                    continue
                plt.plot(df_ij["time"], df_ij["value"], label=f"j={j_val}")

            plt.xlabel("Time Step (t1)")
            plt.ylabel(param)
            plt.legend()
            plt.grid(True)
            plt.ylim(0, 1)
            plt.tight_layout()

            out_path = build_graph_path(os.path.basename(file_name), f"{param}_i{i_val}")
            plt.savefig(out_path)
            plt.close()