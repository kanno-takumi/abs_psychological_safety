import json
import os

def log_step(time1, time2, agents, event_type=None, agent_id=None):
    filename="result/log.json"
    log_entry = {
        "time1": time1,
        "time2": time2,
        "agents": [agent.__dict__ for agent in agents],
        "event": {
            "type": event_type,
            "agent_id": agent_id
        } if event_type else None
    }

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, mode='a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
