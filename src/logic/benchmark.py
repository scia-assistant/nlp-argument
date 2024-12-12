import json
import os
from json.decoder import JSONDecodeError
from typing import Any, Dict, List, Optional, Tuple, Union

import data_loader
import pandas as pd
from chatbot import ChatBotBase, GPTApi, TinyLLama
from cot import Cot, LLM_Fails
from plot_report import build_plots
from tqdm import tqdm

DIR_REPORTS = "reports/"


def llm_alone_response(
    chatbot: ChatBotBase, pre_prompt: str, question: str
) -> Tuple[Optional[dict], List[LLM_Fails]]:

    chatbot.begin_conversation(pre_prompt=pre_prompt)

    max_number_of_try = 3
    fails: List[LLM_Fails] = []

    obj = None
    for _ in range(max_number_of_try):

        response = chatbot.generate_response(question=question, reset_conversation=True)
        print("response :", response)
        try:
            obj = json.loads(response)
            break
        except JSONDecodeError as e:
            print(str(e))
            chatbot.add_message(content=str(e))
            fails.append(LLM_Fails.FORMAT)
            continue

    return obj, fails


def dict_key_lower(d: Dict[str, Any]):
    return {k.lower(): o for k, o in d.items()}


def check_solution(
    actual: Optional[Dict[str, Any]], expected_original: Union[int, float, dict]
) -> bool:

    if actual is None:
        return False

    expected: Dict[str, Any]
    if isinstance(expected_original, dict):
        expected = expected_original
    elif isinstance(expected_original, int) or isinstance(expected_original, float):
        if len(actual) > 1:
            print(f"WARNING : expected one answer but {len(actual)} were given")
        # the anwer must be somewhere (no matter if it gives too much answers)
        return expected_original in actual.values()
    else:
        raise ValueError(
            f"Type '{type(expected_original)}', value '{expected_original}' not handled."
        )

    return dict_key_lower(expected) == dict_key_lower(actual)


def print_banner(s: str) -> None:
    print("------------------------------------------------")
    print(">", s)
    print("--------------------------------")


def save_report(pre_prompt_cot, pre_prompt_alone, save_problems, dir_report):
    # save report
    report = {
        "pre_prompt_cot": pre_prompt_cot,
        "pre_prompt_alone": pre_prompt_alone,
        "problems": save_problems,
        "score cot": sum(e["cot good"] for e in save_problems),
        "score alone": sum(e["alone good"] for e in save_problems),
    }

    print(f"Saving report in '{dir_report}'")

    # saving raw json
    with open(
        os.path.join(dir_report, "row.json"), mode="w", encoding="utf-16"
    ) as file_writer:
        json.dump(obj=report, fp=file_writer)

    # build plots
    build_plots(report, dir_to_save=dir_report)


def benchmark(dataset: pd.DataFrame, chatbot: ChatBotBase, name_report: str) -> None:

    pre_prompt_cot = """
        Generate prolog code that formalize the problem. Generate the prolog query that will give the result.
        Never use '#' operator.
        Try to use the 'is' operator.
        Never write comments.
        Format should be : {"code": <code>, "query": <query>}.
    """

    pre_prompt_alone = """
        Answer to the problem given by a dictinnaory {"<var 1>" : <result 1>, "<var 2>" : <result 2>}.
        You must ONLY give this dictionnary.
    """

    cot = Cot(chatbot=chatbot, pre_promt=pre_prompt_cot)

    save_problems = []

    dir_report: str
    for i in range(1000):
        dir_report = os.path.join(DIR_REPORTS, f"report_{name_report}{i}")
        if not os.path.exists(dir_report):
            break
    os.mkdir(path=dir_report)

    for i, row in tqdm(dataset.iterrows(), total=dataset.shape[0]):

        problem = row["problem"]
        expected_solution = row["solution"]
        print_banner(problem)
        print("solution :", expected_solution)

        # use LLM with COT
        cot_good = False
        code, query, actual_solution_cot, cot_fails = cot.run(problem)

        if actual_solution_cot is not None:
            cot_good = check_solution(
                actual=actual_solution_cot, expected_original=expected_solution
            )

        # use LLM without COT
        actual_solution_alone, alone_fails = llm_alone_response(
            chatbot=chatbot, pre_prompt=pre_prompt_alone, question=problem
        )
        alone_good = check_solution(
            actual=actual_solution_alone, expected_original=expected_solution
        )

        save_problems.append(
            {
                "problem": problem,
                "solution": expected_solution,
                "cot solution": actual_solution_cot,
                "alone solution": actual_solution_alone,
                "cot good": cot_good,
                "alone good": alone_good,
                "cot fails": [e.name for e in cot_fails],
                "alone fails": [e.name for e in alone_fails],
                "code": code,
                "query": query,
            }
        )

        if i % 10 == 0:
            save_report(pre_prompt_cot, pre_prompt_alone, save_problems, dir_report)


if __name__ == "__main__":
    df = data_loader.load_gsm8k()
    # df = df[df["nature"] == "equations"]
    df = df.iloc[:2]
    chatbot = TinyLLama()
    benchmark(dataset=df, chatbot=chatbot, name_report="tinyllama_gsm8k")
