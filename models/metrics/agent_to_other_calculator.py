# models/metrics/agent_to_other.py
import math

def calc_similarity(agent_i, agent_j, max_age_diff=60):
    """
    agent_i と agent_j の類似度を [-1, 1] で返す。
    """
    # 1. 雰囲気（-1~1 の差 → -1~1）
    atmosphere_diff = abs(agent_i.atmosphere - agent_j.atmosphere) / 2
    atmosphere_sim = 1 - atmosphere_diff  # [0, 1]
    atmosphere_sim = atmosphere_sim * 2 - 1  # [-1, 1]

    # 2. スタイル（-1~1 の差 → -1~1）
    style_diff = abs(agent_i.style - agent_j.style) / 2
    style_sim = 1 - style_diff
    style_sim = style_sim * 2 - 1

    # 3. テーマ価値観（2次元距離 → -1~1）
    dx = agent_i.value_x - agent_j.value_x
    dy = agent_i.value_y - agent_j.value_y
    value_distance = math.sqrt(dx**2 + dy**2) / math.sqrt(8)
    value_sim = 1 - value_distance
    value_sim = value_sim * 2 - 1

    # 4. 年齢差（スケーリング）
    age_diff = abs(agent_i.age - agent_j.age) / max_age_diff
    age_sim = 1 - age_diff
    age_sim = age_sim * 2 - 1

    # 5. 分野スコア（CN知識：1〜5 → -1~1）
    fields = ["energy", "transport", "building", "agriculture", "waste", "knowledge_system"]
    total_field_diff = sum(abs(getattr(agent_i, f) - getattr(agent_j, f)) for f in fields)
    avg_field_diff = total_field_diff / len(fields)
    field_sim = 1 - (avg_field_diff / 4)  # 最大差は4
    field_sim = field_sim * 2 - 1

    # 類似度の平均（-1 ~ 1）
    similarity = (atmosphere_sim + style_sim + value_sim + age_sim + field_sim) / 5
    return max(-1, min(1, similarity))

def calc_trust_or_resignation(agent_j):
    """
    信頼/諦めスコア（-1〜1）を計算（対象は agent_j）
    """
    return (agent_j.attitude + agent_j.style) / 2

def calc_interpersonal_risk(agent_i, agent_j, similarity_ij):
    """
    対人リスク [-1, 1] を計算（i→j）
    - style, attitude は agent_j の特性
    - similarity_ij は precomputed similarity[i][j]
    """
    risk = (-agent_j.style - agent_j.attitude - similarity_ij) / 3
    return max(-1, min(1, risk))
