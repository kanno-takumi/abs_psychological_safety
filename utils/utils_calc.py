import numpy as np


#平均と比較した相対的な自分のヒエラルキー
def calc_hierarchy(w1, w2, agent_id, agents):
    agent_i = next(agent for agent in agents if agent.id == agent_id)
    
    age_list = [agent.age for agent in agents]
    skill_score_list = [agent.skill_score for agent in agents]
    
    skill_range = max(skill_score_list) - min(skill_score_list)
    age_range = max(age_list) - min(age_list)
    
    skill_score_mean = np.mean(skill_score_list)
    age_score_mean = np.mean(age_list)
    agent_i_skill_level = (agent_i.skill_score - skill_score_mean) / skill_range
    agent_i_age_level = (agent_i.age - age_score_mean) / age_range
    
    hierarchy = w1 * agent_i_skill_level + w2 * agent_i_age_level
    return hierarchy

#to j に向けたヒエラルキー
def calc_hierarchies(w1, w2, agent_id, agents):
    """
    agent_id: 対象のエージェントのID（int）
    agents: 全エージェント（list of Agent）
    w1,w2：重み
    """
    # print(agent_id)
    # print(agents)
    # agent_id に対応するエージェントを探す
    agent_i = next(agent for agent in agents if agent.id == agent_id)

    skill_score_list = [agent.skill_score for agent in agents]
    age_list = [agent.age for agent in agents]
    # print("skill_score_list")
    # print(skill_score_list)
    skill_range = max(skill_score_list) - min(skill_score_list)
    age_range = max(age_list) - min(age_list)
    
    #分母が0になるのを防ぐ。
    skill_range = skill_range if skill_range != 0 else 1e-6
    age_range = age_range if age_range != 0 else 1e-6
    
    hierarchies = {}
    
    for agent_j in agents:
        if agent_j.id == agent_id:
            continue
        # print(agent_i.skill_score)
        # print(agent_j.skill_score)
        # print(skill_range)
        delta_skill = (agent_i.skill_score - agent_j.skill_score) / skill_range
        # print(delta_skill)
        delta_age = (agent_i.age - agent_j.age) / age_range
        hierarchy = (w1 * delta_skill + w2 * delta_age) / (w1 + w2)    
        
        hierarchies[agent_j.id] = hierarchy    
    return hierarchies

def calc_efficacy(w1, w2, hierarchies, efficacy, reaction, agree, t):
    # print("hierarchies",hierarchies)
    if t == 0:
        efficacy = hierarchies.copy()
    if t > 0:
        #辞書と辞書を足し算、掛け算
        reaction_agree = {key: reaction[key] * (1- agree[key]) for key in reaction}
        efficacy = {key: efficacy[key] * w1 + reaction_agree[key] * w2 for key in reaction_agree}
        # efficacy = w1 * efficacy + w2 * reaction * (1 - agree)
    return efficacy
    
def calc_risk(efficacy, toughness, pressure, t):
    #行列で用意。
    if t == 0:
        risk = {key: (1 - toughness) * (1- efficacy[key]) for key in efficacy}
    if t > 0:
        print("t>0")
    return risk

def calc_speak_probability(w1,w2,w3,assertiveness,extraversion,risk_mean):
    speak_probability = (w1 * assertiveness + w2 * extraversion + w3 * risk_mean) / (w1+ w2 + w3)
    return speak_probability

def calc_reaction_probability(w1,w2,w3,agent_id,agents):
    agent_i = next(agent for agent in agents if agent.id == agent_id)
    assertiveness = agent_i.assertiveness
    extraversion = agent_i.extraversion
    risk = agent_i.risk
    reaction_probabilities = {}
    for agent_j in agents:
        if agent_id == agent_j.id:
            continue
        risk_ij = agent_i.risk.get(agent_j.id)
        reaction_probability =(w1 * assertiveness + w2 * extraversion + w3 * risk_ij)/(w1 + w2 + w3)
        reaction_probabilities[agent_j.id] = reaction_probability
    return reaction_probabilities

def calc_agree_probability(agent_id,agents):
    agent_i = next(agent for agent in agents if agent.id == agent_id)
    agree_probabilities = {}
    for agent_j in agents:
        if agent_id == agent_j.id:
            continue
        dx = agent_i.value_to_cn['x_axis'] - agent_j.value_to_cn['x_axis']
        dy = agent_i.value_to_cn['y_axis'] - agent_j.value_to_cn['y_axis']
        distance = np.sqrt(dx**2 + dy**2)
        agree_probability = 1 - (distance / np.sqrt(8))
        agree_probabilities[agent_j.id] = agree_probability
            
    return agree_probabilities

def calc_attitude_probability(w1,w2,θ,agent_id,agents):
    agent_i = next(agent for agent in agents if agent.id == agent_id)
    attitude_probabilities = {}
    for agent_j in agents:
        if agent_id == agent_j.id:
            continue
        risk_ij = agent_i.risk.get(agent_j.id)
        attitude_probability = (w1 * agent_i.pressure + w2 * risk_ij) / (w1+w2)
        attitude_probabilities[agent_j.id] = attitude_probability
            
    return attitude_probabilities