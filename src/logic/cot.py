import json
import os
from enum import Enum
from json.decoder import JSONDecodeError
from typing import Dict, List, Optional, Tuple

from chatbot import ChatBotBase
from prolog_wrapper import PrologWrapper

DIR_PROLOG_CODE = "generated/"


class LLM_Fails(Enum):
    FORMAT = 1
    CODE = 2
    QUERY = 3
    MAX_TRY = 4


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
    def _extract_code_and_query(
        content: str,
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        try:
            res: Dict[str, str] = json.loads(content)
        except JSONDecodeError as e:
            return None, None, str(e)
        assert "code" in res.keys()
        assert "query" in res.keys()

        code, query = res["code"], res["query"]
        if query.startswith("?-"):
            query = query[2:]

        return code, query, None

    @staticmethod
    def _put_into_prolog_file(path_prolog_file: str, content: str) -> None:

        with open(path_prolog_file, mode="w", encoding="utf-16") as file_writer:
            file_writer.write(content)

    @staticmethod
    def get_prolog_path() -> str:
        path_prolog_file: str
        for i in range(1000):
            filename = f"{i}.pl"
            path_prolog_file = os.path.join(DIR_PROLOG_CODE, filename)
            if not os.path.exists(path_prolog_file):
                break
            break  # always write in the same for now

        return path_prolog_file

    def run(
        self, problem: str
    ) -> Tuple[Optional[str], Optional[str], Optional[dict], List[LLM_Fails]]:

        prolog = PrologWrapper()
        max_number_of_try = 3

        path_prolog_file = self.get_prolog_path()
        query_result: Optional[dict] = None

        self.chatbot.begin_conversation(pre_prompt=self.pre_prompt)

        fails: List[LLM_Fails] = []

        for _ in range(max_number_of_try):
            # run LLM -> generate prolog code and prolog query
            content = self.chatbot.generate_response(
                question=problem, reset_conversation=False
            )

            code, query, error = self.extract_code_and_query(content)
            if error is not None:
                mess = f"Error format : {error}"
                print(mess)
                self.chatbot.add_message(mess)
                fails.append(LLM_Fails.FORMAT)
                continue
            assert code is not None
            assert query is not None

            # put the generated code into a file
            # self.log(f"Saving prolog file into '{path_prolog_file}'.")
            code = code.replace("\\n", "\n")
            self.log(f"Code : '{code}'")
            self.log(f"Query : '{query}'")

            self._put_into_prolog_file(path_prolog_file, code)

            # run the prolog code
            error_code = prolog.consult(pathfile=path_prolog_file)
            if error_code is not None:
                mess = f"Error in code : '{error_code}'"
                print(mess)
                self.chatbot.add_message(mess)
                fails.append(LLM_Fails.CODE)
                continue

            # use the query -> retrieve the result
            query_result, error_query = prolog.query(query)
            if error_query is not None:
                mess = f"Error in query : {error_query}"
                print(mess)
                self.chatbot.add_message(mess)
                fails.append(LLM_Fails.QUERY)
                continue

            break

        if query_result is None:
            fails.append(LLM_Fails.MAX_TRY)

        print(f"query_result : {query_result}")
        return code, query, query_result, fails
