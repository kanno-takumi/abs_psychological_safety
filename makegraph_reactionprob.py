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

# Extract reaction_probability[i -> j] for all i, j over time
reaction_data = []
for entry in log_entries:
    time = entry["time1"]
    for agent in entry["agents"]:
        i = agent["id"]
        reaction_dict = agent.get("reaction_probability", {})
        for j_str, value in reaction_dict.items():
            try:
                j = int(j_str)
                reaction_data.append({
                    "time": time,
                    "from_agent": i,
                    "to_agent": j,
                    "reaction_prob": value
                })
            except ValueError:
                continue

# Create DataFrame
reaction_df = pd.DataFrame(reaction_data)

# Pivot table: each line is a (from_agent, to_agent) pair
reaction_pivot = reaction_df.pivot_table(
    index="time",
    columns=["from_agent", "to_agent"],
    values="reaction_prob",
    aggfunc='mean'
)

# Assign a color to each from_agent (i)
from_agents = reaction_df["from_agent"].unique()
color_palette = plt.cm.get_cmap("tab10", len(from_agents))  # 固定色セット
color_map = {agent_id: color_palette(i) for i, agent_id in enumerate(from_agents)}

# Plot
plt.figure(figsize=(12, 7))
for col in reaction_pivot.columns:
    from_i, to_j = col
    color = color_map.get(from_i, "black")  # fallback
    plt.plot(
        reaction_pivot.index,
        reaction_pivot[col],
        label=f"{from_i}→{to_j}",
        color=color
    )

plt.title("Reaction Probability Over Time (Agent i → Agent j)")
plt.xlabel("Time Step (t1)")
plt.ylabel("Reaction Probability")
plt.ylim(0, 1)
plt.legend(title="i → j", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()
