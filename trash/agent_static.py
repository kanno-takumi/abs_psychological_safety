class AgentStatic:
    def __init__(self, id, gender, age,
                 value_to_cn, attitude, style, mental_strength, atmosphere, mood,
                 knowledge_dict):
        self.id = id
        self.gender = gender
        self.age = age
        self.value_x = value_to_cn.x_axis #CNへの価値観のx軸
        self.value_y = value_to_cn.y_axis #CNへの価値観のy軸
        self.attitude = attitude
        self.style = style
        self.mental_strength = mental_strength
        self.atmosphere = atmosphere
        self.mood = mood

        # CNに関する知識スコア（辞書形式で保持）
        self.knowledge = knowledge_dict
        self.energy = knowledge_dict.energy
        self.transport = knowledge_dict.transportat
        self.industory = knowledge_dict.industory
        self.building = knowledge_dict.transport
        self.agriculture = knowledge_dict.agriculture
        self.waste = knowledge_dict.waste
        self.knowledge_system = knowledge_dict.system