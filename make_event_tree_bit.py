# make_event_tree_bit.py
# ============================================================
# 🎨 ABMログからイベントツリーを作成するモジュール
# （論文用：paper_fig に PDF 出力）
# ============================================================

import os
import re
import json
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# フォントを明示指定（見た目はデフォルトと同じ）
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans"],
    "pdf.fonttype": 42,   # PDFフォント埋め込み（論文用・安全）
})

import colorsys
from pathlib import Path


# =========================== パス操作関連 ===========================
def get_log_path(file_name):
    """
    logs/{file_name の末尾の _数字 を除いたベース}/{file_name} を返す
    """
    name = Path(file_name).name
    stem = Path(name).stem
    m = re.match(r'^(.*?)(?:_\d+)?$', stem)
    base = m.group(1) if m else stem
    return str(Path("logs") / base / name)


def build_graph_path(file_name, param="event_tree_bit", ext="pdf"):
    """
    出力先:
    paper_figs/<ログ名>_<param>.pdf
    例: paper_figs/case2_2_event_tree_bit.pdf
    """
    name = Path(file_name).stem  # case2_2
    out_dir = Path("paper_figs")
    out_dir.mkdir(parents=True, exist_ok=True)
    return str(out_dir / f"{name}_{param}.{ext}")


# =========================== 色設定関連 ===========================
def assign_agent_colors(agent_ids):
    """エージェントごとにパステルカラーを割り当てる"""
    base_colors = [
        "#AEC6CF", "#FFB347", "#77DD77", "#FF6961",
        "#F49AC2", "#CFCFC4", "#B39EB5",
    ]

    def generate_extra_colors(n_extra):
        return [colorsys.hsv_to_rgb(i / n_extra, 0.6, 0.9) for i in range(n_extra)]

    if len(agent_ids) <= len(base_colors):
        color_list = base_colors[:len(agent_ids)]
    else:
        extra = generate_extra_colors(len(agent_ids) - len(base_colors))
        color_list = base_colors + extra

    return {aid: color_list[i % len(color_list)] for i, aid in enumerate(agent_ids)}


# =========================== メイン描画関数 ===========================
def generate_event_tree(file_name):
    log_path = get_log_path(file_name)
    out_path = build_graph_path(file_name)

    if not os.path.exists(log_path):
        print(f"⚠️ ログファイルが見つかりません: {log_path}")
        return

    # --- データ読み込み ---
    events = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if not events:
        print(f"⚠️ ログが空です: {log_path}")
        return

    # --- エージェント情報と色マップ ---
    agent_ids = sorted({
        e["event"].get("agent_id")
        for e in events
        if "event" in e and e["event"].get("agent_id") is not None
    })
    agent_color_map = assign_agent_colors(agent_ids)

    # --- データ整形 ---
    points = []
    for e in events:
        if "event" not in e:
            continue
        ev = e["event"]
        if ev.get("agent_id") is None or ev.get("type") is None:
            continue
        points.append({
            "time1": e.get("time1", 0),
            "time2": e.get("time2", 0),
            "agent": ev.get("agent_id"),
            "type": ev.get("type"),
            "agree": ev.get("agree"),
            "attitude": ev.get("attitude"),
            "color": agent_color_map.get(ev["agent_id"], "gray")
        })

    # --- グラフ生成 ---
    plt.figure(figsize=(4, 4))
    ax = plt.gca()
    ax.set_box_aspect(1)
    ax.set_aspect("equal", adjustable="box")

    # --- グリッド ---
    ax.grid(which="major", linestyle=":", color="gray", alpha=0.5)
    ax.grid(which="minor", linestyle=":", color="gray", alpha=0.25)

    # --- ノード描画 ---
    for p in points:
        x, y = p["time2"], p["time1"]

        if p["type"] == "Speak":
            plt.scatter(
                x, y,
                c="white",
                edgecolors=p["color"],
                marker="s",
                s=70,
                zorder=3
            )

        elif p["type"] == "React":
            attitude_val = float(p["attitude"]) if p["attitude"] is not None else 0
            linewidth = 3.0 * attitude_val
            plt.scatter(
                x, y,
                c="white",
                edgecolors=p["color"],
                marker="o",
                s=70,
                linewidths=linewidth,
                zorder=3
            )

        # agent番号表示（0〜7 の範囲のみ）
        if 0 <= y <= 10:
            plt.text(
                x, y,
                str(p["agent"]),
                fontsize=8,
                color="black",
                ha="center",
                va="center",
                zorder=4
            )

    # --- 矢印描画 ---
    for i, p in enumerate(points):
        if p["type"] != "React" or p["agree"] is None or i == 0:
            continue

        prev = points[i - 1]
        agree_val = float(p["agree"])
        color = "red" if agree_val >= 0.5 else "blue"

        width = abs(agree_val - 0.5) * 0.5
        head_width = 0.05 + width * 1.4

        x1, y1 = p["time2"], p["time1"]
        x2, y2 = prev["time2"], prev["time1"]

        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy)
        if dist == 0:
            continue

        ux, uy = dx / dist, dy / dist
        r = math.sqrt(70 / math.pi) / 10

        plt.arrow(
            x1 + ux * r,
            y1 + uy * r,
            dx - ux * 2 * r,
            dy - uy * 2 * r,
            color=color,
            alpha=0.7,
            width=width,
            head_width=head_width,
            head_length=0.1,
            length_includes_head=True,
            zorder=1
        )

    # --- 軸装飾 ---
    plt.xlabel("Time2 (Local Loop Time)")
    plt.ylabel("Time1 (Global Time)")

    # 目盛り固定
    ax.set_xticks(range(0, 20))
    ax.set_yticks(range(0, 20))

    # 表示範囲
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(10.5, -0.5)

    # --- 保存 ---
    plt.savefig(out_path)
    plt.close()

    print(f"✅ イベントツリーを保存しました: {out_path}")


if __name__ == "__main__":
    generate_event_tree("attitude_check3_10.jsonl")