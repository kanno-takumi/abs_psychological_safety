# utils/math_utils.py
#2軸で取得したテーマへの価値観の類似度を取得
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ベクトルの類似度（コサイン類似度）を計算
# 入力：2つの1次元ベクトル（リストまたはnp.array）
def compute_cosine_similarity(vec1, vec2):
    v1 = np.array(vec1).reshape(1, -1)
    v2 = np.array(vec2).reshape(1, -1)
    return cosine_similarity(v1, v2)[0][0]


# 0〜10の値を0〜1に正規化
# ※もともと0〜10のスコアを使用していた場合に便利
def normalize_score(score):
    return score / 10.0


# スカラー値のクリッピング（0〜1に制限）
def clip_score(value):
    return max(0.0, min(1.0, value))


# 類似度を信頼スコアに変換（例：線形）
def similarity_to_trust(sim, base=0.5, weight=0.5):
    return clip_score(base + weight * (sim - 0.5))
