import json
import os
import re

# 既存互換のグローバル
agents_folder = None
agents_file = None
agents_filepath = None
log_folder = None
log_filepath = None  # ← ここに1行ずつ追記

def _safe_agent_id(filename: str) -> str:
    name, _ = os.path.splitext(os.path.basename(filename))
    return re.sub(r"[^0-9A-Za-z_\-]", "_", name)

def _next_run_index(log_dir: str, agent_id: str) -> int:
    """logs/<agent> 内の <agent>_N.jsonl を走査して N+1 を返す（なければ1）。"""
    if not os.path.isdir(log_dir):
        return 1
    pat = re.compile(rf"^{re.escape(agent_id)}_(\d+)\.jsonl$")
    max_n = 0
    for fn in os.listdir(log_dir):
        m = pat.match(fn)
        if m:
            n = int(m.group(1))
            if n > max_n:
                max_n = n
    return max_n + 1 if max_n > 0 else 1

def init(agents_folder_: str, agents_file_: str, log_folder_: str):
    """
    既存シグネチャのまま使用。
    - agents_folder_: エージェント定義のフォルダ（例 'agents'）
    - agents_file_:   エージェントファイル名（例 'aaa.json'）
    - log_folder_:    ログのルート（例 'logs'）
    """
    global agents_folder, agents_file, agents_filepath, log_folder, log_filepath

    agents_folder = agents_folder_
    agents_file = agents_file_
    agents_filepath = os.path.join(agents_folder_, agents_file_)

    agent_id = _safe_agent_id(agents_file_)
    agent_log_dir = os.path.join(log_folder_, agent_id)  # logs/<agent>
    os.makedirs(agent_log_dir, exist_ok=True)

    run_id = _next_run_index(agent_log_dir, agent_id)
    log_folder = agent_log_dir
    log_filepath = os.path.join(agent_log_dir, f"{agent_id}_{run_id}.jsonl")  # 1行=1タイムステップ

    # ファイルを事前作成（空でOK）
    if not os.path.exists(log_filepath):
        with open(log_filepath, "w", encoding="utf-8") as f:
            pass  # 何も書かない

def log_step(time1, time2, agents, event_type=None, agent_id=None):
    """
    タイムステップごとに1行追記（JSON Lines）。
    出力サイズを抑えるために compact（余計な空白なし）で書き込み。
    """
    if not log_filepath:
        raise RuntimeError("logger.init() を先に呼んでください")

    entry = {
        "time1": time1,
        "time2": time2,
        "agents": [a.__dict__ for a in agents],
        "event": {"type": event_type, "agent_id": agent_id} if event_type else None
    }

    # 1行追記（compactにするため separators を指定）
    with open(log_filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")
