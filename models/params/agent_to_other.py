import numpy as np

def init_interpersonal_params(n_agents, init_value=0.0):
    """
    個人間パラメータ（信頼/諦め・対人リスク）を固定値で初期化。

    Parameters:
    ----------
    n_agents : int
        エージェント数（外部configから取得する想定）
    init_value : float
        初期値（デフォルトは0.5）

    Returns:
    -------
    trust_or_resignation : np.ndarray
        信頼 / 諦め行列（i→j）
    interpersonal_risk : np.ndarray
        対人リスク行列（i→j）
    simularity : np.ndarray
        類似度(i→j)
    """
    #full->指定した形状と値で配列を初期化する関数
    trust_or_resignation = np.full((n_agents, n_agents), init_value)
    interpersonal_risk = np.full((n_agents, n_agents), init_value)
    similarity = np.full((n_agents, n_agents), init_value)

    #fill_diagonal->特定の値を入れる
    np.fill_diagonal(trust_or_resignation, np.nan)
    np.fill_diagonal(interpersonal_risk, np.nan)
    np.fill_diagonal(similarity, np.nan)
    

    return trust_or_resignation, interpersonal_risk, similarity
