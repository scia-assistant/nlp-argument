import os
from abc import ABC, abstractmethod
from typing import List, Optional

from openai import OpenAI
from transformers import pipeline


class ChatBotBase(ABC):

    def __init__(self):
        super().__init__()
        self.pre_prompt: Optional[str] = None
        self.conversation_history: List[dict] = []

    def generate_response(self, question: str, reset_conversation: bool) -> str:

        if reset_conversation:
            self.reset_conversation()

        self.conversation_history.append({"role": "user", "content": question})
        return self._generate_response_from_conversation()

    @abstractmethod
    def _generate_response_from_conversation(self) -> str:
        pass

    def reset_conversation(self) -> None:
        self.conversation_history = []

        if self.pre_prompt is not None:
            self.conversation_history.append(
                {"role": "system", "content": self.pre_prompt}
            )

    def add_message(self, content: str) -> None:
        self.conversation_history.append({"role": "user", "content": content})

    def begin_conversation(self, pre_prompt: Optional[str]) -> None:
        self.pre_prompt = pre_prompt
        self.reset_conversation()


class GPTApi(ChatBotBase):

    def __init__(self):
        super().__init__()

        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        PROJECT_ID = os.getenv("PROJECT_ID")
        ORGANIZATION_ID = os.getenv("ORGANIZATION_ID")

        self.client = OpenAI(
            organization=ORGANIZATION_ID, project=PROJECT_ID, api_key=OPENAI_API_KEY
        )

    def _generate_response_from_conversation(self) -> str:

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.conversation_history,
            max_completion_tokens=300,
            temperature=0.3,
            n=1,
        )
        assistant_reply = completion.choices[0].message.content
        assert assistant_reply is not None

        self.conversation_history.append(
            {"role": "assistant", "content": assistant_reply}
        )

        return assistant_reply


class TinyLLama(ChatBotBase):
    def __init__(self):
        super().__init__()
        self.pipe = pipeline(
            "text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        )

    def _generate_response_from_conversation(self) -> str:
        res = self.pipe(
            self.conversation_history,
            max_new_tokens=300,
            temperature=0.3,
            do_sample=True,
        )
        self.conversation_history = res[0]["generated_text"]

        return self.conversation_history[-1]["content"]


def _main() -> None:
    chatbot = TinyLLama()

    pre_prompt = """
        You are asked to answer the question only by the solution of the problem.
        You must not add anyting else.
    """

    chatbot.begin_conversation(pre_prompt="You are a human called sabrina.")
    answer = chatbot.generate_response(
        "Solve 1 + 2 by generating prolog code.", reset_conversation=True
    )
    print(answer)


if __name__ == "__main__":
    _main()
