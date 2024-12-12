import json
import os
from typing import Any, Dict, Union

import pandas as pd
from chatbot import ChatBotBase, GPTApi
from cot import Cot

DIR_REPORTS = "reports/"


def llm_alone_response(chatbot: ChatBotBase, pre_prompt: str, question: str) -> dict:
    response = chatbot.generate_response(pre_prompt=pre_prompt, question=question)
    return json.loads(response)


def check_solution(
    actual: Dict[str, Any], expected_original: Union[int, float, dict]
) -> bool:

    expected: Dict[str, Any]
    if isinstance(expected_original, dict):
        expected = expected_original
    elif isinstance(expected_original, int) or isinstance(expected_original, float):
        if len(actual) > 1:
            print(f"WARNING : expected one answer but {len(actual)} were given")
        if len(actual) == 0:
            return False
        expected = {list(actual.keys())[0]: expected_original}
    else:
        raise Exception(f"Type '{tye(expected_original)}' not handled.")

    return expected == actual


def benchmark(dataset: pd.DataFrame) -> None:

    pre_prompt_cot = """
        Generate prolog code that formalize the problem. Generate the prolog query that will give the result.
        When the question is a constrained problem, use the library 'clpq'. Remember contrained problem is solved with '{'.
        Format should be : {"code": <code>, "query": <query>}.
    """

    pre_prompt_alone = "Answer to the problem given by a dictinnaory {'<var 1>' : <result 1>, '<var 2>' : <result 2>}"

    chatbot = GPTApi()
    cot = Cot(chatbot=chatbot, pre_promt=pre_prompt_cot)

    save_problems = []

    for _, row in dataset.iterrows():
        print(row)
        problem = row["problem"]
        expected_solution = row["solution"]

        # use LLM with COT
        actual_solution_cot = cot.run(problem)

        cot_good = check_solution(
            actual=actual_solution_cot, expected_original=expected_solution
        )

        # use LLM without COT
        actual_solution_alone = llm_alone_response(
            chatbot=chatbot, pre_prompt=pre_prompt_alone, question=problem
        )
        alone_good = check_solution(
            actual=actual_solution_alone, expected_original=expected_solution
        )

        save_problems.append(
            {
                "problem": problem,
                "cot solution": actual_solution_cot,
                "alone solution": actual_solution_alone,
                "cot good": cot_good,
                "alone good": alone_good,
            }
        )
        break

    # save report
    report = {
        "pre_prompt_cot": pre_prompt_cot,
        "pre_prompt_alone": pre_prompt_alone,
        "problems": save_problems,
        "score cot": sum(e["cot good"] for e in save_problems),
        "score alone": sum(e["alone good"] for e in save_problems),
    }

    path_report: str
    for i in range(1000):
        path_report = os.path.join(DIR_REPORTS, f"{i}.json")
        if not os.path.exists(path_report):
            break
        break

    print(f"Saving report in '{path_report}'")
    with open(path_report, mode="w", encoding="utf-16") as file_writer:
        json.dump(obj=report, fp=file_writer)


if __name__ == "__main__":
    df = pd.read_csv("dataset/mine.csv")
    benchmark(df)
