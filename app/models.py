import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import japanize_matplotlib
import pandas as pd

matcher = re.compile(r"([1-9 １-９]+)班_(\w+)")


def transpose_counter(scores: Counter) -> Tuple[List[str], List[int]]:
    list_score_and_numbers = reversed(sorted(list(scores.items()), key=lambda x: x[0]))
    score, numbers = [], []
    for s, n in list_score_and_numbers:
        score.append(s)
        numbers.append(n)
    return score, numbers


def analysis(df: pd.DataFrame) -> None:
    img_dir = Path(__file__).parent / "static" / "img"
    row_names = df.columns.values
    ext = ".png"
    for row_name in row_names:    # 最後の一個はアドバイスが入っていると仮定する
        if row_name == row_names[-1]:
            break
        else:
            match_groups = matcher.match(row_name).groups()
            group_name, evaluates = match_groups
            counter = Counter(df[row_name])
            scores, scored_numbers = transpose_counter(counter)
            plt.clf()
            plt.pie(scored_numbers,
                    labels=scores,
                    counterclock=False,
                    startangle=90,
                    wedgeprops={
                        "linewidth": 3,
                        "edgecolor": "white"
                    },
                    autopct="%.1f%%")
            plt.title(evaluates)
            dst = str(img_dir / row_name) + ext
            plt.savefig(dst, bbox_inches="tight", pad_inches=0.1)

    with open(img_dir.parent / "messages" / (group_name + ".json"), "w") as f:
        json.dump(
            {
                "images": [x + ext for x in row_names[:-1]],
                "messages": list(
                    map(lambda x: x.replace("\n", "<br>"), df[row_names[-1]])),
            },
            f,
            ensure_ascii=False)


def analysis_form(filename: os.PathLike, n_group: int) -> None:
    print(filename)
    df = pd.read_excel(filename)
    n_index = 5    # 左側の使わない列数
    n_each = (len(df.columns) - 4) // n_group
    for i in range(n_group):
        start = n_index + i * n_each
        end = n_index + (i + 1) * n_each
        analysis(df.iloc[:, start:end])


def is_allowed_file(filename: str, allowd_ext: set) -> bool:
    return filename.rsplit(".", 1)[1].lower() in allowd_ext

def make_sublist(l: list, len_sublist:int) -> list:
    return [l[i:i+len_sublist] for i in range(0, len(l), len_sublist)]
