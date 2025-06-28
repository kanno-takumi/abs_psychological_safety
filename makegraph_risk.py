import json
import pandas as pd
import matplotlib.pyplot as plt

# Load the JSON log data
file_path = "result/log.json"
log_entries = []

# Read line-delimited JSON
with open(file_path, 'r') as f:
    for line in f:
        log_entries.append(json.loads(line))

# Extract risk_mean for each agent over time
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

# Pivot data for plotting
df_pivot = df.pivot_table(index="time", columns="agent_id", values="risk_mean", aggfunc='mean')

# Plot risk_mean over time for each agent
plt.figure(figsize=(10, 6))
for agent_id in df_pivot.columns:
    plt.plot(df_pivot.index, df_pivot[agent_id], label=f"Agent {agent_id}")

plt.title("Risk Mean Over Time per Agent")
plt.xlabel("Time Step (t1)")
plt.ylabel("Risk Mean")
plt.ylim(0, 1)  # Set y-axis to show from 0 to 1
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()