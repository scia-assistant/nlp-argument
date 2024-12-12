import subprocess
from typing import List, Optional, Tuple

from pyswip import Prolog
from pyswip.prolog import PrologError


class PrologWrapper:

    def __init__(self):
        self.prolog = Prolog()

    def consult(self, pathfile: str) -> Optional[str]:
        # Execute a shell command
        result = subprocess.run(
            ["swipl", "-s", pathfile, "-g", "true", "-t", "halt."],
            capture_output=True,
            text=True,
            check=False,
        )

        return result.stderr

    def query(self, query: str) -> Tuple[List[dict], Optional[str]]:
        try:
            query_result = list(self.prolog.query(query))
            return (query_result, None)
        except PrologError as e:
            return ([], str(e))
