# ABS/models/metrics/faultline_calculator.py

import numpy as np
from sklearn.cluster import KMeans
from itertools import combinations

class FaultlineCalculator:
    def __init__(self, agents, n_clusters=3):
        """
        :param agents: List of agent objects
        :param n_clusters: Number of clusters used for faultline calculation
        """
        self.agents = agents
        self.n_clusters = min(n_clusters, len(agents))  # 人数未満にならないよう調整
        self.risk_matrix = self._compute_risk_matrix()

    def _compute_risk_matrix(self):
        n = len(self.agents)
        risk_matrix = np.zeros((n, n))
        for i, agent_i in enumerate(self.agents):
            for j, agent_j in enumerate(self.agents):
                if i != j:
                    # -1~1のリスクをそのまま格納
                    risk = agent_i.interpersonal_risk.get(agent_j.id, 0)
                    risk_matrix[i, j] = risk
        return risk_matrix

    def calculate_faultline(self):
        if len(self.agents) <= 1:
            return 0.0  # 人数が1人以下なら分断は発生しない

        model = KMeans(n_clusters=self.n_clusters, random_state=0)
        model.fit(self.risk_matrix)
        labels = model.labels_

        cluster_centers = []
        for label in set(labels):
            cluster_indices = np.where(labels == label)[0]
            sub_matrix = self.risk_matrix[cluster_indices][:, cluster_indices]
            cluster_centers.append(np.mean(sub_matrix))

        distances = [
            abs(c1 - c2)
            for c1, c2 in combinations(cluster_centers, 2)
        ]

        faultline_score = np.mean(distances)

        # 正規化：距離の最大値は 2.0（-1~1 の範囲で計算しているため）
        return faultline_score / 2

    def get_cluster_labels(self):
        if len(self.agents) <= 1:
            return [0]
        return KMeans(n_clusters=self.n_clusters, random_state=0).fit(self.risk_matrix).labels_
