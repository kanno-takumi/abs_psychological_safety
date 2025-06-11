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
    print(agent_id)
    print(agents)
    # agent_id に対応するエージェントを探す
    agent_i = next(agent for agent in agents if agent.id == agent_id)

    skill_score_list = [agent.skill_score for agent in agents]
    age_list = [agent.age for agent in agents]
    print("skill_score_list")
    print(skill_score_list)
    skill_range = max(skill_score_list) - min(skill_score_list)
    age_range = max(age_list) - min(age_list)
    
    #分母が0になるのを防ぐ。
    skill_range = skill_range if skill_range != 0 else 1e-6
    age_range = age_range if age_range != 0 else 1e-6
    
    hierarchies = {}
    
    for agent_j in agents:
        if agent_j.id == agent_id:
            continue
        print(agent_i.skill_score)
        print(agent_j.skill_score)
        print(skill_range)
        delta_skill = (agent_i.skill_score - agent_j.skill_score) / skill_range
        print(delta_skill)
        delta_age = (agent_i.age - agent_j.age) / age_range
        hierarchy = (w1 * delta_skill + w2 * delta_age) / (w1 + w2)    
        
        hierarchies[agent_j.id] = hierarchy    
    return hierarchies

def calc_efficacy(w1, w2, hierarchies, efficacy, reaction, agree, t):
    if t == 0:
        efficacy = hierarchies
    if t > 0:
        #辞書と辞書を足し算、掛け算
        reaction_agree = {key: reaction[key] * (1- agree[key]) for key in reaction}
        efficacy = {key: efficacy[key] * w1 + reaction_agree[key] * w2 for key in reaction_agree}
        # efficacy = w1 * efficacy + w2 * reaction * (1 - agree)
    return efficacy
    
def calc_risk(efficacy, toughness):
    #行列で用意。
    risk = (1- toughness) * (1 - efficacy)
    return risk