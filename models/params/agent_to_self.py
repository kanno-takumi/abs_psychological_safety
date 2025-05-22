class Agent:
    def __init__(self, id, initial_self_efficacy=0.5, initial_opinion_position=0.5):
        self.id = id
        self.self_efficacy = initial_self_efficacy
        self.opinion_position = initial_opinion_position
        # その他の属性や関係性マトリクスへのリンクなどもあり
