#single agentを初期化し保管するファイル
#agentの複数の種類のクラスを持つ。
import numpy as np
from utils.utils_calc import calc_hierarchy 
import pprint

class Agent:
    def __init__(self, data, agents):
     # #staticで初期値はメンバー依存
    # #Nの配列[id, gender, age...]
        self.id = data["id"]
        self.age = data["age"]
        self.skill = data["skill"] #この中にさらに4つある
        self.skill_score = np.mean(list(self.skill.values()))
        self.value_to_cn = data["value_to_cn"]
        self.pressure = data["pressure"]
        self.assertiveness = data["assertiveness"]
        self.toughness = data["toughness"]
        self.extraversion = data["extraversion"]
        
    def __str__(self):
        return pprint.pformat(self.__dict__, indent=2, sort_dicts=False)
        
        # self.efficacy = calc_hierarchy(0.5,0.5,self.skill,self.age)
        # self.risk = calc_risk()

        # #個人がチームに対してもつパラメータ    
        # #Nの配列[agent_psychological_safety, agent_casual_atmmosphere]
        # self.agent_psychological_safety = 0
        # self.agent_casual_atmosphere = 0

        #個人の行動傾向（ーしそうを判定するための関数）
        # self.speak_probability = 0
        # self.reaction_strength = 0
        # self.expressed_attitude = 0
        
   
    # def __init__(self,data,num):
    #     self.id = data.id
    #     self.gender = data.gender
    #     self.age = data.age
    #     self.value_x = data.value_to_cn.x_axis #CNへの価値観のx軸
    #     self.value_y = data.value_to_cn.y_axis #CNへの価値観のy軸
    #     self.attitude = data.ttitude
    #     self.style = data.style
    #     self.mental_strength = data.ental_strength
    #     self.atmosphere = data.atmosphere
    #     self.mood = data.mood

    #     # CNに関する知識スコア（辞書形式で保持）
    #     self.knowledge = data.knowledge
    #     #knowledge配列は以下の6要素を含む。
    #     
        
    # #対人に対するパラメータ
    # #N*Nの配列[trust[to1人目,to2人目,to3人目,...], interpersonal_risk[to1人目,to2人目,to3人目,...]]
    # #def init_interpersonal_params(n_agents, init_value=0.0):
    #     #full->指定した形状と値で配列を初期化する関数
    #     length = num - 1
    #     self.trust_or_resignation = np.zeros(length)
    #     self.interpersonal_risk = np.zeros(length)
    #     self.similarity = np.zeros(length)
        
    # 
    #     self.self_efficacy = data.initial_self_efficacy
    #     self.opinion_position = data.initial_opinion_position
    #     # その他の属性や関係性マトリクスへのリンクなどもあり
    
    # #個人がチームに対してもつパラメータ    
    # #Nの配列[agent_psychological_safety, agent_casual_atmmosphere]
    #     self.agent_psychological_safety = 0
    #     self.agent_casual_atmosphere = 0
    

    # #個人の行動傾向（ーしそうを判定するための関数）
    # #Nの配列[speak_probability,reaction_strength]
    # # def init_behavior_tendency(n_agents, init_value=0.0):
    #     self.speak_probability = 0
    #     self.reaction_strength = 0
    #     self.expressed_attitude = 0
    