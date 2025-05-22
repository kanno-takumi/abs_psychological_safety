# ABM Project for Group Work Simulation

This project simulates group dynamics and psychological safety using Agent-Based Modeling (ABM), with a focus on team composition, knowledge diversity, and interaction rules.

## 🏁 Project Purpose

To explore how interpersonal trust, psychological safety, and individual traits affect idea generation and behavior in group work, especially in the context of Carbon Neutrality (CN) brainstorming.

---

## 🗂️ Project Structure

```bash
abm_project/
│
├── config/                  
│   └── agent_config.py        # Agent initialization: traits, skills, CN knowledge
│   └── env_config.py          # Global simulation settings: team size, number of rounds
│
├── models/
│   └── agent_model.py         # Agent class: state, actions, internal variables
│   └── interaction_rules.py   # Rules for speaking, reacting, psychological state updates
│   └── trust_dynamics.py      # Trust and risk update mechanisms
│
├── data/
│   └── initial_data.csv       # Optional: manually set initial values
│   └── simulation_log.csv     # Output logs of each simulation run
│
├── utils/
│   └── math_utils.py          # Similarity, normalization, score calculations
│   └── visualization.py       # Network plots, skill radar charts, etc.
│
├── main.py                    # Simulation runner: executes simulation steps
└── README.md                  # Project documentation (this file)
```

## ⛽️ Parameter Definition Overview

Parameters are organized into five modules based on their roles in the simulation.

---

### ① `agent_static.py` – Individual Static Traits (Non-Updating)

These parameters are initialized at the beginning of the simulation and remain fixed unless externally modified.

| Parameter          | Description                                         |
|--------------------|-----------------------------------------------------|
| `id`               | Agent identifier                                    |
| `gender`, `age`    | Basic demographic attributes                        |
| `value_x`, `value_y` | Agent's value orientation toward carbon neutrality (2D axes) |
| `attitude`         | Attitudinal stance (e.g., passive/active)          |
| `style`            | Interaction style (e.g., cooperative/conflictual)  |
| `mental_strength`  | Mental resilience or tolerance                      |
| `atmosphere`       | The kind of atmosphere the agent projects           |
| `mood`             | Current emotional state                             |
| `knowledge_dict`   | Dictionary of knowledge levels related to CN fields |
| └ `energy`, `transport`, `building`, `agriculture`, `waste`, `system` | Domain-specific CN knowledge scores |

---

### ② `agent_to_other.py` – Perceptions Toward Others (Dict Format)

These parameters represent each agent's feelings toward every other agent.

| Parameter                   | Description                                        |
|-----------------------------|----------------------------------------------------|
| `trust_or_resignation[id]` | Level of trust or resignation toward another agent |
| `interpersonal_risk[id]`   | Perceived interpersonal risk when interacting      |

---

### ③ `agent_to_self.py` – Internal Self-Evaluation

These parameters reflect how each agent perceives their own standing and capabilities.

| Parameter           | Description                                         |
|---------------------|-----------------------------------------------------|
| `self_efficacy`     | Belief in one’s own ability to contribute           |
| `opinion_position`  | Perceived relative minority/majority status of opinion |

---

### ④ `agent_to_team.py` – Perceptions of the Team

These parameters represent an agent’s subjective experience of the team context.

| Parameter                   | Description                                  |
|-----------------------------|----------------------------------------------|
| `agent_psychological_safety` | Individual's psychological safety within the team |
| `agent_casual_atmosphere`    | Perceived informality/casualness of the team atmosphere |

---

### ⑤ `team_state.py` – Aggregated Team-Level States

These parameters summarize emergent states at the team level.

| Parameter                  | Description                                          |
|----------------------------|------------------------------------------------------|
| `team_psychological_safety` | Overall team psychological safety (e.g., average)   |
| `team_casual_atmosphere`   | Overall team atmosphere                             |
| `team_faultline`           | Structural faultlines or subgroup divisions          |

---

## ⏳ Update Timing

- State updates occur **at each round**, based on input conditions and interaction rules.
- Parameter influences are described using **causal relations** (e.g., `value_x → opinion_position`) and are implemented in separate logic modules.

---

For more detailed configuration and parameter initialization, see the `config/` directory and relevant `.py` modules.
