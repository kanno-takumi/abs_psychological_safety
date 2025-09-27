# Re-import for clean execution
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load JSON data again
file_path = "result/log.json"
log_entries = []

with open(file_path, 'r') as f:
    for line in f:
        log_entries.append(json.loads(line))

# Helper function to extract and plot any i→j parameter (e.g., reaction_probability)
def extract_and_plot_parameter(log_entries, param_name, title, ylabel):
    data = []
    for entry in log_entries:
        time = entry["time1"]
        for agent in entry["agents"]:
            i = agent["id"]
            param_dict = agent.get(param_name, {})
            for j_str, value in param_dict.items():
                try:
                    j = int(j_str)
                    data.append({
                        "time": time,
                        "from_agent": i,
                        "to_agent": j,
                        "value": value
                    })
                except ValueError:
                    continue

    df = pd.DataFrame(data)
    pivot = df.pivot_table(index="time", columns=["from_agent", "to_agent"], values="value", aggfunc='mean')

    from_agents = df["from_agent"].unique()
    color_palette = plt.cm.get_cmap("tab10", len(from_agents))
    color_map = {agent_id: color_palette(i) for i, agent_id in enumerate(from_agents)}

    plt.figure(figsize=(12, 7))
    for col in pivot.columns:
        from_i, to_j = col
        color = color_map.get(from_i, "black")
        plt.plot(pivot.index, pivot[col], label=f"{from_i}→{to_j}", color=color)

    plt.title(title)
    plt.xlabel("Time Step (t1)")
    plt.ylabel(ylabel)
    plt.ylim(0, 1)
    plt.legend(title="i → j", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Plot each parameter
extract_and_plot_parameter(log_entries, "reaction_probability", "Reaction Probability Over Time (Agent i → Agent j)", "Reaction Probability")
extract_and_plot_parameter(log_entries, "agree_probability", "Agree Probability Over Time (Agent i → Agent j)", "Agree Probability")
extract_and_plot_parameter(log_entries, "attitude_probability", "Attitude Probability Over Time (Agent i → Agent j)", "Attitude Probability")
