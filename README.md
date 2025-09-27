# ABM Project for Group Work Simulation

## ⭐️ Outline
This project simulates dynamics of psychological safety using Agent-Based Modeling (ABM), with a focus on individual traits, actions, and interaction.
By defining agents with individual traits and incorporating their behaviors and team interactions into an Agent-Based Modeling, we dynamically simulate how psychological safety evolves over time.
Distinctive features of this model are its ability to capture the fluctuations of psychological safety depending on the situation rather than treating it as a simple condition-dependent factor and simplified experimental environmental as an alternative to social experiments, which are often difficult to conduct as preliminary studies. In this way, the model supports the exploration of appropriate team compositions and management interventions.

本研究は，ビジネスアイデア構想におけるアイデア発想フェーズにおいて，個人特性・行動・相互作用が心理的安全性に与えるダイナミクスを再現・分析することを目的とする．
個人特性を持つエージェントを設定し，行動やチーム内の相互作用を組み込んだABM(Agent-Baased Modeling) を構築することで，心理的安全性が時間とともに変化する過程を動的にシミュレーションする．
本モデルは，単純な条件依存ではなく，状況に応じて揺らぐ心理的安全性を表現できる点，さらに予備実験が行いづらい社会実験に代わり簡易的な実験環境を提供できる点に特徴がある．
これにより，適切なチーム編成やマネジメント介入の検討を支援する．

## 🏁 Project Purpose
This study aims to reenact and analyze dynamics of psychological safety in the idea generation phase on business ideation, focusing on how individual traits, behaviors, and interactions influenece these dynamics using Agent-Based Modeling

ビジネスアイデア構想におけるアイデア発想フェーズにおいて，個人特性・行動・相互作用が心理的安全性に与えるダイナミクスをABMにより再現・分析することを目的とする．

## 🗂️ Project Structure

```bash
abm_project/
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
