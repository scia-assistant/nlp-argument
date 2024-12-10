from langchain_community.document_loaders import UnstructuredHTMLLoader
from load_llm.load_llm import LLMPretrained, LLMWrapper
from langchain.docstore.document import Document
from transformers import pipeline


class RAG:
    def __init__(self, vector_store, model, tokenizer=None) -> None:
        self.vector_store = vector_store
        self.model = model

        if tokenizer is None:
            self.tokenizer = self.model.tokenizer
        else:
            self.tokenizer = tokenizer

    def retrieve_k_top(self, k: int, query: str):
        return self.vector_store.similarity_search(query=query, k=k)

    def get_formatted_prompt(self, query: str, retrieved_texts: list[str]):
        PROMPT_TEMPLATE = """
Vous êtes un chatbot. En utilisant les informations contenues dans le contexte, donnez une réponse complète à la question.\n
Contexte:\n
{context}\n
Réponds à la question suivante.\n
Question: {question}\n
Réponse:"""
        context = ""
        context += "".join(
            [
                f"Document {str(i)}:\n" + doc + "\n"
                for i, doc in enumerate(retrieved_texts)
            ]
        )

        return PROMPT_TEMPLATE.format(question=query, context=context)

    # def generate_answer(self, k:int, query: str):
    #     retrieved_docs = self.retrieve_k_top(k, query)
    #     retrieved_docs_text = [doc.page_content for doc in retrieved_docs]
    #     prompt = self.get_formatted_prompt(query=query, retrieved_texts=retrieved_docs_text)
    #     print('===========PROMPT=============')
    #     print(prompt)
    #     res = self.model.generate_text(prompt=prompt, max_length=1000)
    #     print('===========RESULT=============')
    #     print(res)

    def generate_answer(self, k: int, query: str):

        READER_LLM = pipeline(
            model=self.model.model,
            tokenizer=self.tokenizer,
            task="text-generation",
            # do_sample=True,
            # temperature=0.3,
            repetition_penalty=1.2,
            return_full_text=False,
            max_new_tokens=500,
            device='cpu'
        )

        prompt_in_chat_format = [
            {
                "role": "system",
                "content": "Vous êtes un chatbot.",
            },
            {
                "role": "user",
                "content": "Bonjour est-ce que tu vas bien?",
            },
        ]

        retrieved_docs = self.retrieve_k_top(k, query)
        result = [
        {
            'title': doc.page_content.split()[0],  # Using the first word of page_content as title
            'text': doc.page_content
        }
        for doc in retrieved_docs
        ]
        
        # self.tokenizer.chat_template = "{% for message in messages %}\n{% if message['role'] == 'user' %}\n{{ '<|user|>\n' + message['content'] + eos_token }}\n{% elif message['role'] == 'system' %}\n{{ '<|system|>\n' + message['content'] + eos_token }}\n{% elif message['role'] == 'assistant' %}\n{{ '<|assistant|>\n'  + message['content'] + eos_token }}\n{% endif %}\n{% if loop.last and add_generation_prompt %}\n{{ '<|assistant|>' }}\n{% endif %}\n{% endfor %}"
        print(self.tokenizer.chat_template)
        conversation = prompt_in_chat_format

        template_str = """
{% if messages[0]['role'] == 'system' %}
  {{ messages[0]['content'] }}
  {% set messages = messages[1:] %}
{% endif %}

{% for message in messages %}
  {% if message['role'] == 'user' %}
    User: {{ message['content'] }}
  {% elif message['role'] == 'assistant' %}
    Assistant: {{ message['content'] }}
  {% endif %}
{% endfor %}

{% if documents %}
  Context:
  {% for doc in documents %}
    - {{ doc }}
  {% endfor %}
{% endif %}
Assistant:
"""

        print(retrieved_docs)
        retrieved_docs_text = [doc.page_content for doc in retrieved_docs]
        # RAG_PROMPT_TEMPLATE = self.tokenizer.apply_chat_template(
        #     conversation=conversation, tokenize=True, add_generation_prompt=True, documents=result, return_tensors='pt', chat_template = template_str
        # )

        RAG_PROMPT_TEMPLATE = self.get_formatted_prompt("Qu'est-ce qu'un litige?", retrieved_docs_text)
        print(RAG_PROMPT_TEMPLATE)
        # RAG_PROMPT_TEMPLATE.to('cpu')

        self.model.model.to('cpu')
        context = "\nExtracted documents:\n"
        context += "".join(
            [
                f"Document {str(i)}:::\n" + doc
                for i, doc in enumerate(retrieved_docs_text)
            ]
        )

        # final_prompt = RAG_PROMPT_TEMPLATE.format(question=query, context=context)
        print("===========PROMPT=============")
        # print(RAG_PROMPT_TEMPLATE)
        # tokens = self.tokenizer(RAG_PROMPT_TEMPLATE, return_tensors='pt').input_ids
        answer = READER_LLM(RAG_PROMPT_TEMPLATE)
        res = answer[0]["generated_text"]
        # answer = self.model.model.generate(tokens, max_new_tokens=100, repetition_penalty=1.3, return_full_text=False)
        # res = self.tokenizer.decode(answer[0])

        print("===========RESULT=============")
        # print(answer)
        print(res)
        print("TOTOTOTO")



# {
                # "role": "user",
                # "content": """
# {context}
# Now here is the question you need to answer.

# Question: {question}""",
            # }