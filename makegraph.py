import os, json
import pandas as pd
import matplotlib.pyplot as plt

SUPPORTED_EXTS = {'.eps', '.jpeg', '.jpg', '.pdf', '.pgf', '.png', '.ps', '.raw', '.rgba', '.svg', '.svgz', '.tif', '.tiff'}

def get_log_entries(log_path):
    if not os.path.exists(log_path):
        print(f"Error: File '{log_path}' does not exist.")
        exit(1)

    log_entries = []
    with open(log_path, 'r') as f:
        for line in f:
            log_entries.append(json.loads(line))
    return log_entries


def _make_out_path(base_in, suffix, preferred_ext=".pdf"):
    base, ext = os.path.splitext(base_in)
    # 入力の拡張子が画像保存として不適なら preferred_ext に差し替え
    out_ext = ext if ext.lower() in SUPPORTED_EXTS else preferred_ext
    return f"{base}{suffix}{out_ext}"


def plot_risk(log_entries, base_path_for_out):
    # 出力先（例: simulate_log/5agents_ver4_risk.pdf）
    out_path = _make_out_path(base_path_for_out, "_risk")

    # データ抽出
    data = []
    for entry in log_entries:
        time = entry["time1"]
        for agent in entry["agents"]:
            data.append({
                "time": time,
                "agent_id": agent["id"],
                "risk_mean": agent.get("risk_mean", None)
            })
    df = pd.DataFrame(data)

    # データ整形
    df_pivot = df.pivot_table(index="time", columns="agent_id",
                              values="risk_mean", aggfunc='mean')

    # グラフ描画
    plt.figure(figsize=(10, 6))
    for agent_id in df_pivot.columns:
        plt.plot(df_pivot.index, df_pivot[agent_id], label=f"Agent {agent_id}")

    plt.xlabel("Time Step (t1)")
    plt.ylabel("Average Perceived Risk per Agent")
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.show()


def plot_psychological_safety(log_entries, base_path_for_out):
    # 出力先（例: simulate_log/5agents_ver4_psy.pdf）
    out_path = _make_out_path(base_path_for_out, "_psy")

    # データ抽出 & 変換
    data = []
    for entry in log_entries:
        time = entry["time1"]
        for agent in entry["agents"]:
            risk = agent.get("risk_mean", None)
            psy = 1 - risk if risk is not None else None
            data.append({
                "time": time,
                "agent_id": agent["id"],
                "psychological_safety_mean": psy
            })
    df = pd.DataFrame(data)

    # データ整形
    df_pivot = df.pivot_table(index="time", columns="agent_id",
                              values="psychological_safety_mean", aggfunc='mean')

    # グラフ描画
    plt.figure(figsize=(10, 6))
    for agent_id in df_pivot.columns:
        plt.plot(df_pivot.index, df_pivot[agent_id], label=f"Agent {agent_id}")

    plt.xlabel("Time Step (t1)")
    plt.ylabel("Average Psychological Safety per Agent")
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.show()

# def plot_hierarchy(log_entries, base_path_for_out):
#     out_path = _make_out_path(base_path_for_out, "_hierarchy_mean")

#     # --- 抽出 ---
#     rows = []
#     for entry in log_entries:
#         t = entry.get("time1")
#         for a in entry.get("agents", []):
#             rows.append({
#                 "time": t,
#                 "agent_id": a.get("id"),
#                 "hierarchy_mean": a.get("hierarchy_mean")
#             })
#     df = pd.DataFrame(rows)

#     # --- ここがポイント：型揃え＋欠損除去 ---
#     df = df.dropna(subset=["hierarchy_mean"])
#     df["agent_id"] = df["agent_id"].astype(int)
#     df["time"] = df["time"].astype(int)

#     # デバッグ（必要なら残してOK）
#     print(df.head())
#     print("unique agent_ids:", df["agent_id"].unique())
#     print(df.groupby("agent_id")["hierarchy_mean"].count())

#     # --- ピボット ---
#     df_pivot = df.pivot_table(index="time", columns="agent_id",
#                               values="hierarchy_mean", aggfunc="mean").sort_index()

#     # --- 描画 ---
#     plt.figure(figsize=(10, 6))
#     for agent_id in df_pivot.columns:
#         series = df_pivot[agent_id]
#         if series.notna().any():  # 全欠損の列はスキップ
#             plt.plot(df_pivot.index, series, label=f"Agent {agent_id}")

#     plt.xlabel("Time Step (t1)")
#     plt.ylabel("Average Perceived Hierarchy per Agent")
#     plt.ylim(0, 1)
#     plt.legend()
#     plt.grid(True)
#     plt.tight_layout()
#     plt.savefig(out_path)
#     plt.show()

def plot_hierarchy(log_entries, base_path_for_out):
    out_path = _make_out_path(base_path_for_out, "_hierarchy_mean")

    # データ抽出
    data = []
    for entry in log_entries:
        time = entry["time1"]
        for agent in entry["agents"]:
            data.append({
                "time": time,
                "agent_id": agent["id"],
                "hierarchy_mean": agent.get("hierarchy_mean", None)
            })
    df = pd.DataFrame(data)

    # データ整形
    df_pivot = df.pivot_table(index="time", columns="agent_id",
                              values="hierarchy_mean", aggfunc='mean').sort_index()
    
    print("pivot columns:", df_pivot.columns)
    print("pivot head:\n", df_pivot.head())

    # 線スタイルを交互に設定
    # styles = ['-', '--', '-.', ':']
    plt.figure(figsize=(10, 6))
    for i, agent_id in enumerate(df_pivot.columns):
        plt.plot(
            df_pivot.index,
            df_pivot[agent_id],
            label=f"Agent {agent_id}",
        )

    plt.xlabel("Time Step (t1)")
    plt.ylabel("Average Perceived Hierarchy per Agent")
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.show()

    
    
if __name__ == "__main__":
    log_filename = input("ファイル名：")  # 例: 5agents_ver4.json
    log_path = os.path.join("simulate_log", log_filename)
    graph_path = os.path.join("simulate_graph", log_filename)
    # graph_path = os.path.join("simulate_graph", log_filename)

    # ログ読み込み
    log_entries = get_log_entries(log_path)  # ← ここに直す

    # ここでは「ログファイルのパス」を“ベース名”として渡すだけで、
    # 関数内で *_risk.pdf / *_psy.pdf に自動変換して保存します
    plot_risk(log_entries, graph_path)
    plot_psychological_safety(log_entries, graph_path)
    plot_hierarchy(log_entries, graph_path)