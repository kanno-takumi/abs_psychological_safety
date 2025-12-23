# make_eventtree.py
# ============================================================
# 🎨 ABMログからイベントツリーを作成するモジュール
# ============================================================

import os
import re
import json
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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


def build_graph_path(file_name, param="event_tree", ext="png"):
    """
    グラフ出力先パスを返す
    → graphs/<base>/<stem>/<param>.png
    """
    file_name = Path(file_name).name
    stem = Path(file_name).stem
    m = re.match(r'^(.*?)(?:_\d+)?$', stem)
    base = m.group(1)
    out_dir = Path("graphs") / base / stem
    out_dir.mkdir(parents=True, exist_ok=True)
    return str(out_dir / f"{param}.{ext}")


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
        extra_rgb = [(r, g, b) for r, g, b in extra]
        color_list = base_colors + extra_rgb

    return {aid: color_list[i % len(color_list)] for i, aid in enumerate(agent_ids)}


# =========================== メイン描画関数 ===========================
def generate_event_tree(file_name):
    """
    ログファイルをもとにイベントツリーを生成し、グラフを保存する。
    """
    log_path = get_log_path(file_name)
    out_path = build_graph_path(file_name, "event_tree")

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
            "agent": ev["agent_id"],
            "type": ev["type"],
            "agree": ev.get("agree"),
            "attitude": ev.get("attitude"),
            "color": agent_color_map.get(ev["agent_id"], "gray")
        })

    # --- グラフ生成 ---
    plt.figure(figsize=(32, 32))
    ax = plt.gca()
    ax.set_box_aspect(1)
    ax.set_aspect('equal', adjustable='box')

    # 軸とグリッド設定
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.grid(which="major", linestyle=":", color="gray", alpha=0.5)
    ax.grid(which="minor", linestyle=":", color="gray", alpha=0.25)

    # --- ノード描画 ---
    for p in points:
        x, y = p["time2"], p["time1"]
        if p["type"] == "Speak":
            plt.scatter(x, y, c="white", edgecolors=p["color"], marker="s", s=70, zorder=3)
        elif p["type"] == "React":
            attitude_val = float(p["attitude"]) if p["attitude"] is not None else 0
            linewidth = 3.0 * attitude_val
            plt.scatter(x, y, c="white", edgecolors=p["color"], marker="o", s=70,
                        zorder=3, linewidths=linewidth)
            plt.text(x, y - 0.5, f"{attitude_val:.2f}",
                     fontsize=2, color="gray",
                     ha="center", va="top", zorder=4)
        plt.text(x, y, str(p["agent"]),
                 fontsize=8, color="black",
                 ha="center", va="center", zorder=4)

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
        dist = math.sqrt(dx**2 + dy**2)
        if dist == 0:
            continue

        ux, uy = dx / dist, dy / dist
        r = math.sqrt(70 / math.pi) / 10
        start_x, start_y = x1 + ux * r, y1 + uy * r
        end_x, end_y = x2 - ux * r, y2 - uy * r

        plt.arrow(start_x, start_y, end_x - start_x, end_y - start_y,
                  color=color, alpha=0.7, width=width,
                  head_width=head_width, head_length=0.1,
                  length_includes_head=True, zorder=1)
        plt.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.5, f"{agree_val:.2f}",
                 fontsize=2, color="gray", ha="center", va="bottom", zorder=5)

    # --- 軸装飾 ---
    plt.xlabel("time2 (Local loop)")
    plt.ylabel("time1 (Global time)")
    plt.title("Event Relations (Red=Agree, Blue=Disagree)")
    plt.gca().invert_yaxis()
    plt.grid(True, linestyle=":", alpha=0.5)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"✅ イベントツリーを保存しました: {out_path}")
