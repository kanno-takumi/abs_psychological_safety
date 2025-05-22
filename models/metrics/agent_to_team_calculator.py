def calc_agent_psychological_safety(agent):
    """
    agent_psychological_safety = 自己効力感 + 意見スコア
    """
    return agent.self_efficacy + agent.opinion_score


def calc_agent_casual_atmosphere(agent, agents):
    """
    agent_casual_atmosphere = 雰囲気 + (信頼 - リスク)の平均
    """
    others = [a for a in agents if a.id != agent.id]
    n = len(others)

    avg_trust = sum(agent.trust[other.id] for other in others) / n
    avg_risk = sum(agent.risk[other.id] for other in others) / n

    return agent.atmosphere + (avg_trust - avg_risk)
