import pandas as pd
import numpy as np

def csv_to_pairwise_dict(csv_path, value_column='value', default_value=None, symmetric=False):
    """
    任意の source-target-value 形式のCSVを、(i, j): value の辞書に変換します。

    Parameters
    ----------
    csv_path : str
        CSVファイルへのパス。source, target, value の3列が必要。
    value_column : str
        どの列をvalueとするか。デフォルトは 'value'
    default_value : Any
        初期化されていない (i, j) にデフォルト値を補完する場合に指定
    symmetric : bool
        True にすると (i, j) と (j, i) の両方を同じ値で登録する

    Returns
    -------
    dict
        (i, j): value 形式の辞書
    """
    df = pd.read_csv(csv_path)
    pair_dict = {}

    for _, row in df.iterrows():
        i = int(row['source'])
        j = int(row['target'])
        v = row[value_column]
        pair_dict[(i, j)] = v
        if symmetric and (j, i) not in pair_dict:
            pair_dict[(j, i)] = v

    if default_value is not None:
        all_ids = set(df['source']).union(df['target'])
        for i in all_ids:
            for j in all_ids:
                if i != j and (i, j) not in pair_dict:
                    pair_dict[(i, j)] = default_value

    return pair_dict