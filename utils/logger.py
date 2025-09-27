import json
import os
from dataclasses import dataclass

def init(agents_folder_: str, agents_file_: str, log_folder_: str):
    global agents_folder, agents_file, agents_filepath, log_folder, log_filepath
    agent_folder = agents_folder_
    agents_file  = agents_file_
    agents_filepath = os.path.join(agents_folder_, agents_file_)
    log_folder = log_folder_
    log_filepath = os.path.join(log_folder_, agents_file_)

def log_step(time1, time2, agents, event_type=None, agent_id=None):
    log_entry = {
        "time1": time1,
        "time2": time2,
        "agents": [agent.__dict__ for agent in agents],
        "event": {
            "type": event_type,
            "agent_id": agent_id
        } if event_type else None
    }

    with open(log_filepath, mode='a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
