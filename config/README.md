# 🛠️ config/sim_config.py の使い方

このファイルは、ABMシミュレーションにおける**アルゴリズムや実行条件の制御パラメータ**を定義するための設定スクリプトです。

---

## ✅ sim_config.py とは？

`sim_config.py` は「どのようなルール・構成でシミュレーションを動かすか？」を設定するためのPythonファイルです。

実験データ（エージェントの初期状態）は `data/initial_data.csv` に保存されますが、**このファイルでは「どのルールを適用するか」「何ラウンド繰り返すか」などの設定**を行います。

---

## 🧩 典型的な設定項目（例）

```python
# シミュレーション設定
NUM_AGENTS = 5
NUM_ROUNDS = 10 #シミュレーション回数
USE_TRUST_DYNAMICS = True
USE_PSYCH_SAFETY_FEEDBACK = True

# 出力設定
LOG_LEVEL = "INFO"
SAVE_LOG = True
