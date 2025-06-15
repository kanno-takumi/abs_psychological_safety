import numpy as np
import random
import math


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

def calc_attitude_probability(w1,w2,agent_id,agents):
    agent_i = next(agent for agent in agents if agent.id == agent_id)
    attitude_probabilities = {}
    for agent_j in agents:
        if agent_id == agent_j.id:
            continue
        risk_ij = agent_i.risk.get(agent_j.id)
        attitude_probability = (w1 * agent_i.pressure + w2 * risk_ij) / (w1+w2)
        attitude_probabilities[agent_j.id] = attitude_probability
            
    return attitude_probabilities


# def speak_decision(speak_probability):
#     #発言するかどうかを確率的に決定する。
#     if random.uniform(0,1) < speak_probability:
#     # if 0.8 < speak_probability:
#         speak_boolean = 1
#     else:
#         speak_boolean = 0
#     return speak_boolean

import random

def speak_decision(speak_probability, sigma=0.1,temperature=0.1):
    """
    正規分布に基づいて確率値を生成し、それを使って0/1を確率的に決定する。
    
    Parameters:
    - speak_probability: 平均発言確率（0〜1）
    - sigma: 標準偏差（デフォルトは0.1）

    Returns:
    - 1（発言）または 0（非発言）
    """
    # 正規分布から一時的な確率値を生成し、0〜1にクリップ
    sampled = random.normalvariate(speak_probability, sigma)
    clipped = max(0.0, min(1.0, sampled))
    
    # 確率を滑らかに二値化（ロジスティック関数を通す）
    # 0.5 を中心に温度パラメータで鋭さを調整
    logit = (clipped - 0.5) / temperature
    prob = 1 / (1 + math.exp(-logit))
    
    # その確率に基づいて発言するかどうかを決定
    return 1 if random.random() < prob else 0

        
def speaker_decision(speaks_dict):
    candidates = [agent_id for agent_id, speak in speaks_dict.items() if speak ==1]
    
    if candidates:
        return random.choice(candidates)
    else:
        return None
    
    
def agree_to_speaker(agent,speaker_id,sigma=0.1):
    #agent_id == speaker_id の時はagent_prob = 0を返す
    print(agent.id)
    print(speaker_id)
    
    if agent.id == speaker_id:
        agree_prob = 0.0
        raw = 0.0
    else:
        agree_prob = agent.agree_probability.get(speaker_id)
        raw = random.normalvariate(agree_prob,sigma)
    clipped = max(0.0,min(1.0, raw))
    return {speaker_id: clipped}

import random

def reaction_decision(agent_i, speaker_id, agree_to_speaker, alpha1=0.5, alpha2=0.5):
    """
    agent_i: リアクションする側のエージェント（i）
    speaker_id: 発言者のID（j）
    
    return: reaction_ij を {speaker_id: 1 or 0} の辞書で返す
    """
    key = f"ito{speaker_id}"

    if agent_i.id == speaker_id:
        return {speaker_id: 0}  # 自分自身にはリアクションしない

    reaction_prob = agent_i.reaction_probability.get(key, 0.5)
    agree_deviation = abs(0.5 - agree_to_speaker[speaker_id])
    combined_prob = (alpha1 * reaction_prob + alpha2 * agree_deviation) / (alpha1 + alpha2)

    reaction = 1 if random.random() < combined_prob else 0
    return {speaker_id: reaction}

def reactor_decision(reaction_dict):
    candidates = []
    for agent_id, reaction in reaction_dict.items():
        value = list(reaction.values())[0]
        if value ==1:
            candidates.append(agent_id)
    if candidates:
        return random.choice(candidates)
    else:
        return None
    

def attitude_result(attitude_probability, to_id):
    attitude = attitude_probability.get(to_id, None)#基本的にはattitude_probabilityのto_id番目を取得。なければ0
    return {to_id:attitude}



#学習モデル
##risk
def update_risk(agent_id, agents, attitude, alpha1, alpha2):
    """
    agent_i が持つ他者に対する risk_ijを更新。
    """
    agent_i = next(agent for agent in agents if agent.id == agent_id)
    for agent_j in agents:
        if agent_i.id == agent_j.id:
            continue
    
        #risk_ij
        old_risk = agent_i.risk.get(agent_j.id)
        att_ji = list(attitude.values())[0]
        agent_i.risk[agent_j.id] = alpha1 * old_risk + alpha2 * att_ji
    return agent_i.risk

##efficacy
def update_risk(agent_id, agents, agree, reaction, alpha1, alpha2):
    """
    agent_i が持つ他者に対する efficacy_ijを更新。
    """
    agent_i = next(agent for agent in agents if agent.id == agent_id)
    for agent_j in agents:
        if agent_i.id == agent_j.id:
            continue
    # ---efficacy_ij ---
        old_eff = agent_i.efficacy.get(agent_j.id, 0.5)
        agree_ji = agree_to_speaker(agent_j, agent_i.id, weight=0.1)
        reaction_ji_dict = reaction_decision(agent_j, agent_i.id, agree_ji)
        reaction_ji = list(reaction_ji_dict.values())[0]
        new_eff = alpha1 * old_eff + alpha2 * reaction_ji * (1 - agree_ji)
        agent_i.efficacy[agent_j.id] = new_eff
    return agent_i.efficacy