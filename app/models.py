from typing import Tuple, List
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

import re
import os
from collections import Counter

matcher = re.compile(r"([1-9 １-９]+)班_(\w+)")

def dissaemble_scores(scores: Counter) -> Tuple[List[str], List[int]]:
    list_score_and_numbers = sorted(list(scores.items()), key=lambda x: x[0])
    score, numbers = [], []
    for s, n in list_score_and_numbers:
        score.append(s)
        numbers.append(n)
    return score, numbers

def analysis(df: pd.DataFrame) -> None:
    row_names = df.columns.values
    for row_name in row_names: # 最後の一個はアドバイスが入っていると仮定する
        if row_name == row_names:
            break
        else:
            match_groups = matcher.match(row_name).groups()
            group_name, evaluates = match_groups(0), match_groups(1)
            counter = Counter(df[row_name])
            scores, scored_numbers = dissaemble_scores(counter)
            plt.clf()
            plt.pie(scored_numbers, labels=scores, counterclock=False, startangle=90, widgeprops={"linewidth": 3, "edgecolor": "white"})
            plt.title(evaluates)
            plt.savefig(f"{evaluates}.jpg")
            


def analysis_form(filename: os.PathLike, n_group: int) -> None:
    df = pd.read_excel(filename)
