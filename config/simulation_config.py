# config/sim_config.py

# ========================
# シミュレーション基本設定
# ========================

# エージェント数（initial_data.csv の人数と一致させること）
NUM_AGENTS = 5

# グループワークのラウンド数（＝発言〜反応までの繰り返し回数）
NUM_ROUNDS = 10

# ========================
# 使用ルールのON/OFFスイッチ
# ========================

# 信頼（Trust）とリスク（Risk）が発言や反応によって変動するか
USE_TRUST_DYNAMICS = True

# 心理的安全性が発言や反応によって変動するか（Falseなら固定）
USE_PSYCH_SAFETY_FEEDBACK = True

# 意見の一致・不一致によって信頼度に影響を与えるか
USE_VALUE_ALIGNMENT = True

# 発言の履歴を蓄積し、将来の行動に影響させるか
USE_MEMORY_EFFECT = False

# ========================
# 出力・ログ関連の設定
# ========================

# ログレベル（"INFO", "DEBUG", "ERROR" など）
LOG_LEVEL = "INFO"

# ログファイルを保存するか（Trueで simulation_log.csv に出力）
SAVE_LOG = True

# 各エージェントのラウンドごとの状態も保存するか
SAVE_AGENT_STATE = True

# ========================
# 実験ID（結果の識別用）
# ========================

EXPERIMENT_ID = "exp01_baseline"
