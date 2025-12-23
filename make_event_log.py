# =========================== JSON 出力（★新規追加） ===========================

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

# ====================== イベントログ（JSON）出力 ======================
import os
import json
from pathlib import Path

def get_event_json_path(file_name):
    """
    file_name: "differentvalue4_9.jsonl" のようなログファイル名
    出力先: event_logs/differentvalue4/differentvalue4_9.json
    """

    name = Path(file_name).name             # "differentvalue4_9.jsonl"
    stem = Path(name).stem                  # "differentvalue4_9"
    agent_id = stem.split("_")[0]           # "differentvalue4"

    out_dir = Path("event_logs") / agent_id
    out_dir.mkdir(parents=True, exist_ok=True)

    return str(out_dir / f"{stem}.json")


def export_event_json_from_log(file_name):
    """
    logs/<agent>/<file_name>.jsonl を読み取り、
    event_log（nodesのみ）を event_logs/<agent>/<file_name>.json として保存する。
    """

    # 元ログのパスを取得
    log_path = get_log_path(file_name)

    # 出力先のパス
    out_path = get_event_json_path(file_name)

    if not os.path.exists(log_path):
        print(f"❌ 元ログが見つかりません: {log_path}")
        return

    nodes = []

    # JSONL を行ごとに読む
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except:
                continue

            # event ノードを抽出
            if "event" not in entry:
                continue
            ev = entry["event"]

            nodes.append({
                "time1": entry.get("time1"),
                "time2": entry.get("time2"),
                "agent": ev.get("agent_id"),
                "type": ev.get("type"),
                "attitude": ev.get("attitude"),
                "agree": ev.get("agree")
            })

    # JSON 配列として保存
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"nodes": nodes}, f, indent=2, ensure_ascii=False)

    print(f"✅ イベントログ JSON を保存しました: {out_path}")
