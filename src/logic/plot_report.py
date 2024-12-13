import json
import os

import matplotlib.pyplot as plt
import pandas as pd
from cot import LLM_Fails


def save_fig(dir_to_save: str, filename: str) -> None:
    plt.tight_layout()
    plt.savefig(os.path.join(dir_to_save, filename))
    plt.clf()


def success(df: pd.DataFrame, dir_to_save: str):
    s = df[["alone good", "cot good"]].sum(axis=0) / df.shape[0] * 100
    s["100"] = 100
    s.plot(kind="bar")
    save_fig(dir_to_save, "sucess_rate.png")


def fails_count(df: pd.DataFrame, dir_to_save: str) -> None:
    def to_num_fail(col: str) -> pd.Series:
        s = df.explode(col).groupby(by=col).size()
        for fail in LLM_Fails:
            f = fail.name
            if f not in s:
                s[f] = 0
        return s

    data = [to_num_fail("alone fails"), to_num_fail("cot fails")]
    pd.DataFrame(
        data=data,
        index=["alone", "cot"],
    ).T.plot(kind="bar")
    save_fig(dir_to_save, "fails_count.png")


def max_try_reached(df: pd.DataFrame, dir_to_save: str) -> None:

    def percent_fail(col: str, fail: str):
        df2 = df.explode(col)
        return df2[df2[col] == fail].shape[0] / df.shape[0] * 100

    pd.Series(
        data={
            "cot max try reached": percent_fail("cot fails", fail="MAX_TRY"),
            "alone max try reached": percent_fail("alone fails", fail="MAX_TRY"),
            "100": 100,
        }
    ).plot(kind="bar")
    save_fig(dir_to_save, "max_try_reached.png")


def build_plots(report: dict, dir_to_save: str) -> None:
    df = pd.DataFrame(data=report["problems"])
    success(df, dir_to_save)
    fails_count(df, dir_to_save)
    max_try_reached(df, dir_to_save)


def _main():
    pathfile = "reports/report_gsm8k3/row.json"
    with open(pathfile, mode="r", encoding="utf-16") as file_reader:
        report = json.load(fp=file_reader)

    build_plots(report, "reports/report_gsm8k3")


if __name__ == "__main__":
    _main()
