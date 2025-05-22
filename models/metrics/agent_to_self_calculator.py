def calc_self_efficacy(agent, agents):
    """
    自己効力感 = （自分の能力合計 - チーム平均）を [-1, 1] に正規化
    """
    ability_attrs = [
        'energy',
        'transport',
        'building',
        'agriculture',
        'waste',
        'knowledge_system'
    ]

    my_score = sum(getattr(agent, attr) for attr in ability_attrs)

    team_total = sum(
        sum(getattr(other, attr) for attr in ability_attrs)
        for other in agents
    )
    avg_score = team_total / len(agents)

    # 正規化：最大差は ±12 と仮定（チーム全体30点 vs 最低6点）
    max_diff = 24
    normalized = (my_score - avg_score) / max_diff

    # 範囲外カット（安全策）
    return max(-1, min(1, normalized))

def calc_opinion_position(agent, agents, similarity_matrix):
    """
    agent: 自分自身（Agentオブジェクト）
    agents: チーム内の全エージェント（Agentオブジェクトのリスト）
    similarity_matrix: {(i_id, j_id): similarity} の辞書、値域 [-1, 1]
    """
    others = [a for a in agents if a.id != agent.id]
    if not others:
        return 0.0  # 1人チームのとき

    total_similarity = sum(similarity_matrix[(agent.id, other.id)] for other in others)
    return total_similarity / len(others)

