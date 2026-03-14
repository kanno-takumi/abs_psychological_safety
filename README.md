# Psychological Safety Agent-Based Simulation

This repository implements an **Agent-Based Model (ABM)** designed to reproduce and analyze the **dynamics of psychological safety in team discussions**.

The simulation models conversational interactions among agents. Psychological safety is treated as a **dynamic variable that evolves through interpersonal interactions**, rather than as a static team property.

The model records interaction events and provides tools for reconstructing and visualizing the dynamics of group discussions.

---

# Project Structure

```
abs_psychological_safety/

agents/
models/
utils/

event_logs/
logs/
graphs/
paper_figs/

main.py

make_event_log.py
make_event_tree.py
make_event_tree_bit.py

make_graphs.py
makegraph_3prob.py
makegraph_reactionprob.py
makegraph_speakprob.py

make_paper_figure.py
manage_log.py

trash/
```

---

# Directory Description

## agents/

Contains definitions and initialization of agents used in the simulation.

Agents represent participants in a discussion and maintain internal psychological states as well as interpersonal states toward other agents.

Agent-related parameters are initialized here.

---

## models/

Contains the behavioral logic used in the simulation.

This includes rules that determine:

- speaking probability  
- reaction probability  
- state updates after interactions  
- psychological safety updates  

These rules define how agent states evolve through interactions.

---

## utils/

Utility functions used throughout the project.

Typical functionality includes:

- probability calculations  
- normalization functions  
- helper operations used by simulation modules  

---

## event_logs/

Stores structured interaction logs generated from simulation runs.

These logs contain detailed records of agent interactions and are used for later analysis.

---

## logs/

Stores raw logs generated during simulation execution.

These logs may contain debugging information or intermediate outputs.

---

## graphs/

Stores visualizations generated from simulation data.

Examples include:

- speaking probability distributions  
- reaction probability changes  
- psychological safety trajectories  

---

## paper_figs/

Contains figures generated specifically for academic papers.

These figures are typically created from processed simulation outputs.

---

## trash/

Temporary or experimental scripts that are not part of the main simulation pipeline.

---

# Main Scripts

## main.py

Entry point of the simulation.

Responsibilities:

- initialize simulation parameters  
- initialize agents  
- run simulation steps  
- record interaction data  

Run the simulation with:

```bash
python main.py
```

---

## make_event_log.py

Processes raw simulation outputs and generates structured event logs.

The event logs typically contain records such as:

- simulation step  
- speaker  
- interaction target  
- reaction  
- psychological safety  

These logs are stored in:

```
event_logs/
```

---

## make_event_tree.py  
## make_event_tree_bit.py

These scripts reconstruct the **structure of conversational interactions** from event logs.

They represent discussions as interaction trees where:

- nodes represent events  
- edges represent causal interaction relationships  

These structures help analyze conversational dynamics.

---

## make_graphs.py

Generates general visualizations from simulation logs.

Outputs are stored in:

```
graphs/
```

---


## manage_log.py

Provides utilities for organizing and managing simulation logs.

Typical tasks include:

- merging log files  
- cleaning log directories  
- preparing datasets for analysis  

---

# Agent Parameters

The simulation models agents using a set of psychological and behavioral parameters.

These parameters influence how agents behave in interactions and how psychological safety evolves.

---

## Agent Attributes

Agent properties in the simulation are organized into three categories: **personal traits**, **interpersonal impressions**, and **behaviors**.

---

### Personal Traits

These attributes represent the internal characteristics of an agent.

| Attribute | Description |
|---|---|
| Skill | Capability of the agent in different domains |
| Level of Pressure | Degree of psychological pressure experienced by the agent |
| Values | Value orientation of the agent |
| Assertiveness | Tendency to express opinions actively |
| Toughness | Psychological resilience when facing disagreement or criticism |
| Extraversion | Degree of social outgoingness |

---

### Interpersonal Impressions

These variables represent how one agent perceives another agent.

| Attribute | Description |
|---|---|
| Hierarchy | Perceived status or hierarchy relative to another agent |
| Efficacy | Perceived competence of another agent |
| Interpersonal Risk | Perceived risk in interacting with another agent |
| Psychological Safety | Degree of safety felt when interacting with another agent |

---

### Behaviors

These variables represent observable actions during interactions.

| Behavior | Description |
|---|---|
| Speech | Whether an agent speaks or remains silent |
| Reaction | Whether an agent reacts to another agent's speech |
| Agreement | Degree of agreement or disagreement |
| Attitude | Emotional or evaluative stance toward another agent |

# Output Data

The simulation produces several types of outputs.

---

## Event Logs

```
event_logs/
```

Contain structured interaction records.

Example fields:

```
step
speaker
target
reaction
psychological_safety
```

---

## Graph Outputs

```
graphs/
```

Visual representations of simulation dynamics.

Examples include:

- speaking probability distribution  
- reaction probability changes  
- psychological safety trajectories  

---

## Paper Figures

```
paper_figs/
```

Figures used for academic publications.

---

# Research Objective

This simulation framework is designed to reproduce and analyze the **dynamics of psychological safety in group discussions**.

By modeling conversational interactions among agents, the system allows researchers to explore:

- how psychological safety emerges  
- how interpersonal interactions affect team dynamics  
- what behavioral patterns arise in group discussions  

---

# Author

Takumi Kanno  
Graduate School of Systems Engineering  
Shibaura Institute of Technology