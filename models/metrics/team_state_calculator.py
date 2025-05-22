# models/metrics/team_state_calculator.py

class TeamStateCalculator:
    def __init__(self, agents):
        self.agents = agents

    def calc_psych_safety(self):
        values = [a.agent_psychological_safety for a in self.agents]
        return sum(values) / len(values) if values else 0.0

    def calc_casual_atmosphere(self):
        values = [a.agent_casual_atmosphere for a in self.agents]
        return sum(values) / len(values) if values else 0.0

    def calc_faultline(self, n_clusters=3):
        from models.metrics.faultline_calculator import FaultlineCalculator
        return FaultlineCalculator(self.agents, n_clusters).calculate_faultline()
