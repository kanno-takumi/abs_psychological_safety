import os
import json

def get_log(log_path):
    # ファイルの存在チェック
        if not os.path.exists(log_path):
            print(f"Error: File '{log_path}' does not exist.")
            exit(1)

        # JSONログの読み込み
        log_entries = []
        with open(log_path, 'r') as f:
            for line in f:
                log_entries.append(json.loads(line))
        return log_entries
