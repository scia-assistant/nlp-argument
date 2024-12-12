import json
import os
from typing import Dict, Optional, Tuple

from chatbot import ChatBotBase
from prolog_wrapper import PrologWrapper

DIR_PROLOG_CODE = "generated/"


class MaximumTriesReach(Exception):
    pass


class QueryBroken(Exception):
    pass


class Cot:
    def __init__(self, chatbot: ChatBotBase, pre_promt: str):
        self.chatbot = chatbot
        self.pre_prompt = pre_promt
        self.extract_code_and_query = Cot._extract_code_and_query
        self.log = print if True else lambda *_: None

    @staticmethod
    def _extract_code_and_query(content: str) -> Tuple[str, str]:
        res: Dict[str, str] = json.loads(content)
        assert "code" in res.keys()
        assert "query" in res.keys()
        return res["code"], res["query"]

    @staticmethod
    def _put_into_prolog_file(path_prolog_file: str, content: str) -> None:

        with open(path_prolog_file, mode="w", encoding="utf-16") as file_writer:
            file_writer.write(content)

    def run(self, problem: str) -> dict:

        prolog = PrologWrapper()
        max_number_of_try = 3

        path_prolog_file: str
        for i in range(1000):
            filename = f"{i}.pl"
            path_prolog_file = os.path.join(DIR_PROLOG_CODE, filename)
            if not os.path.exists(path_prolog_file):
                break

        self.log(f"Saving prolog file into '{path_prolog_file}'.")

        for i in range(max_number_of_try):
            # run LLM -> generate prolog code and prolog query
            content = self.chatbot.generate_response(
                pre_prompt=self.pre_prompt, question=problem
            )

            code, query = self.extract_code_and_query(content)

            # put the generated code into a file
            self.log("Saving prolog code.")
            self._put_into_prolog_file(path_prolog_file, code)

            # run the prolog code
            error_code = prolog.consult(pathfile=path_prolog_file)
            if error_code is not None:
                print(f"Error consulting : {error_code}")
                if i + 1 == max_number_of_try:
                    raise MaximumTriesReach(
                        f"The LLM did {max_number_of_try} tries to generate valid prolog code. He reached the maximum."
                    )
                continue

            # use the query -> retrieve the result
            res, error_query = prolog.query(query)
            if error_query is not None:
                raise QueryBroken("The query does not run")

            break

        return res[0]
