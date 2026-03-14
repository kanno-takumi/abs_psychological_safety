# make_paper_figure.py
import os
import json
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# ===== 論文用スタイル =====
plt.rcParams.update({
    "font.size": 12,
    "axes.labelsize": 14,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 300
})

def load_log(file_path):
    logs = []
    with open(file_path, "r") as f:
        for line in f:
            logs.append(json.loads(line))
    return logs

def plot_ps_level_for_paper(log_file, out_path):
    logs = load_log(log_file)

    rows = []
    for e in logs:
        t = e["time1"]
        for a in e["agents"]:
            rows.append({
                "Time Step": t,
                "Agent": a["id"],
                "Psychological Safety Level": a.get("safety_mean")
            })

    df = pd.DataFrame(rows)

    pivot = (
        df.pivot(index="Time Step",
                 columns="Agent",
                 values="Psychological Safety Level")
          .sort_index()
    )

    fig, ax = plt.subplots(figsize=(6, 4))  # 論文向け比率
    pivot.plot(ax=ax, linewidth=1)

    ax.set_xlabel("Time Step")
    ax.set_ylabel("Psychological Safety Level")
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path)
    plt.close()

# ===== 実行例 =====
plot_ps_level_for_paper(
    log_file="logs/differentvaluetwo/differentvaluetwo_1.jsonl",
    out_path="paper_figs/differentvaluetwo.pdf"
)
