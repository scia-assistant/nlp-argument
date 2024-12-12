import os
from abc import ABC, abstractmethod

from openai import OpenAI


class ChatBotBase(ABC):

    @abstractmethod
    def generate_response(self, pre_prompt: str, question: str) -> str:
        pass


class GPTApi(ChatBotBase):

    def __init__(self):

        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        PROJECT_ID = os.getenv("PROJECT_ID")
        ORGANIZATION_ID = os.getenv("ORGANIZATION_ID")

        self.client = OpenAI(
            organization=ORGANIZATION_ID, project=PROJECT_ID, api_key=OPENAI_API_KEY
        )

    def generate_response(self, pre_prompt: str, question: str) -> str:

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": pre_prompt,
                },
                {"role": "user", "content": question},
            ],
            max_completion_tokens=100,
            temperature=0.3,
        )
        res = completion.choices[0].message.content
        assert res is not None
        return res
