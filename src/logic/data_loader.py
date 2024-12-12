import json
import os

import pandas as pd

DIR_DATASET = "dataset/"


def load_mine() -> pd.DataFrame:
    path = os.path.join(DIR_DATASET, "mine.csv")
    df = pd.read_csv(filepath_or_buffer=path)

    casters = [int, float, json.loads]

    # cast each solution to its real type (string -> ?)

    for i in range(df.shape[0]):
        value = df.loc[i, "solution"].replace("'", '"')
        new_value = None
        for c in casters:
            try:
                new_value = c(value)  # type: ignore
                break
            except ValueError:
                continue

        if new_value is None:
            print(
                f"Value '{value}' is now castable to any of those types : '{casters}'"
            )
            continue

        df.at[i, "solution"] = new_value

    return df


def load_gsm8k() -> pd.DataFrame:
    splits = {
        "train": "main/train-00000-of-00001.parquet",
        "test": "main/test-00000-of-00001.parquet",
    }
    df = pd.read_parquet("hf://datasets/openai/gsm8k/" + splits["train"])

    df.rename(columns={"question": "problem"}, inplace=True)
    df["solution"] = (
        df["answer"].str.split("#### ").str[1].str.replace(",", "").astype(dtype=int)
    )

    return df


def _main():

    load_gsm8k()


if __name__ == "__main__":
    _main()
