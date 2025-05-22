def __init__(n_agents):
    """
    チーム全体の状態を初期化する関数。

    Parameters:
    ----------
    init_informal_climate : float
        雑談が許される雰囲気の初期値（0〜1）
    init_psych_safety : float
        チーム全体の心理的安全性の初期値（0〜1）

    Returns:
    -------
    team_state : dict
        チーム状態を表す辞書
    """
    team_pyschological_safety = None
    team_casual_atmosphere = None
    team_faultline = None
    
    return team_pyschological_safety,team_casual_atmosphere,team_faultline
    
    