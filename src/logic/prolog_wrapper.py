import subprocess
from typing import List, Optional, Tuple

from pyswip import Prolog
from pyswip.prolog import PrologError


class PrologWrapper:

    def __init__(self):
        self.prolog = Prolog()

    def consult(self, pathfile: str) -> Optional[str]:
        # Execute a shell command to check errors
        result = subprocess.run(
            ["swipl", "-s", pathfile, "-g", "true", "-t", "halt."],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.stderr != "":
            return result.stderr

        self.prolog.consult(pathfile)
        return None

    def query(self, query: str) -> Tuple[Optional[dict], Optional[str]]:
        try:
            query_result = list(self.prolog.query(query))
            if len(query_result) == 0:
                return None, "Wrong query"
            return (query_result[0], None)
        except (PrologError, KeyError) as e:
            return (None, str(e))
