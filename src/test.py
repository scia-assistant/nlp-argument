import faiss
import time
import os
import ssl
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import GPTNeoXForCausalLM, GPTNeoXTokenizerFast


ssl._create_default_https_context = ssl._create_stdlib_context


# # arr=["https://en.wikipedia.org/wiki/Insensitivity_to_sample_size",
# #      "https://en.wikipedia.org/wiki/Recapitulation_theory",
# #      "https://en.wikipedia.org/wiki/Simpson%27s_paradox"]

# documents = []
# directory_path = "../data"
# # Iterate over each .html file in the directory and load it
# for filename in os.listdir(directory_path):
#     if filename.endswith(".html"):
#         file_path = os.path.join(directory_path, filename)
#         print(f"Loading file: {file_path}")
        
#         # Use UnstructuredHTMLLoader to load the HTML file
#         loader = UnstructuredHTMLLoader(file_path)
#         document = loader.load()
        
#         # Append the loaded document to the documents list
#         documents.extend(document)  # extend in case `load()` returns a list of documents

# # Now `documents` contains all loaded HTML documents
# print(f"Loaded {len(documents)} documents.")

# loader=UnstructuredHTMLLoader()
# docs = loader.load()

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=500,   # Set chunk size based on your model's token limit
#     chunk_overlap=50  # Set overlap to retain context across chunks
# )
# split_documents = text_splitter.split_documents(documents)

# for idx, doc in enumerate(split_documents):
#     print(f"Chunk {idx + 1}:\n{doc.page_content}\n---\n")


embeddings = GPT4AllEmbeddings()
# # #embeddings = HuggingFaceEmbeddings()

# model_name = "sentence-transformers/all-mpnet-base-v2"
# model_kwargs = {'device': 'cpu'}
# encode_kwargs = {'normalize_embeddings': False}
# embeddings = HuggingFaceEmbeddings(
#                 model_name=model_name,
#                 model_kwargs=model_kwargs,
#                 encode_kwargs=encode_kwargs
#             )
print("----------LOADING FAISS----------\n")
# start_time = time.time()
# vectorstore = FAISS.from_documents(split_documents, embeddings)
# end_time = time.time()
# elapsed_time = end_time - start_time
# vectorstore.save_local("faiss_index")
vectorstore = FAISS.load_local(
    "faiss_index", embeddings, allow_dangerous_deserialization=True
)


model = GPTNeoXForCausalLM.from_pretrained("EleutherAI/gpt-neox-20b")
tokenizer = GPTNeoXTokenizerFast.from_pretrained("EleutherAI/gpt-neox-20b")

# print(f"Command took {elapsed_time:.2f} seconds")
print("----------DONE LOADING FAISS----------\n")
prompt = "Katherine is a bad choice for mayor because she didn’t grow up in this town."
retireved_results=vectorstore.similarity_search(prompt, k=3)
second_prompt = f"Is this an correct or fallacious argument and if it is fallacious what type is it? {retireved_results}"
print("----------PROMPT----------\n")
print(second_prompt)
print("----------RESULT----------\n")

input_ids = tokenizer(prompt, return_tensors="pt").input_ids

inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")

gen_tokens = model.generate(
    input_ids,
    do_sample=True,
    temperature=0.9,
)
gen_text = tokenizer.batch_decode(gen_tokens)[0]

print(gen_text)

# print("----------RESULTS----------\n")
# for el in retireved_results:
#     print(el)
#     print("--------------------\n")


# import os
# import requests
# from time import sleep
# from bs4 import BeautifulSoup


# # List of URLs from the CSV file
# links = [
#     "https://en.wikipedia.org/wiki/Fallacy",
#     "https://en.wikipedia.org/wiki/Argument_from_ignorance",
#     "http://philosophy.lander.edu/logic/ignorance.html",
#     "https://www.logicallyfallacious.com/tools/lp/Bo/LogicalFallacies/182/Willed-Ignorance",
#     "http://www.ditext.com/fearnside/28.html",
#     "http://skepdic.com/truebeliever.html",
#     "https://en.wikipedia.org/wiki/Taboo",
#     "http://rationalwiki.org/wiki/Appeal_to_mystery",
#     "http://rationalwiki.org/wiki/Science_doesn%27t_know_everything",
#     "http://rationalwiki.org/wiki/Argument_from_incredulity"
#     # Add more links here if needed
# ]

# import re
# def sanitize_filename(name):
#     return re.sub(r'[\\/*?:"<>|]', "", name)


# os.makedirs("data", exist_ok=True)

# # Download each page and save only the main content as an HTML file
# for idx, url in enumerate(links, start=1):
#     try:
#         print(f"Downloading {url}")
#         response = requests.get(url)
#         response.raise_for_status()  # Check for HTTP errors

#         # Parse the HTML content
#         soup = BeautifulSoup(response.text, "html.parser")
        
#         # Extract the main content area (adjust per website structure)
#         title_tag = soup.find("title")
#         title_text = title_tag.get_text() if title_tag else "untitled"

#         main_content = soup.find(id="bodyContent") or soup.find("body")
        
#         # Get the HTML from the main content area or fallback to full page if not found
#         main_content_html = main_content.prettify() if main_content else soup.prettify()

#         # Save content as a plain HTML file
#         file_name = os.path.join("data", f"{sanitize_filename(title_text)}.html")
#         with open(file_name, "w", encoding="utf-8") as file:
#             file.write(main_content_html)

#         print(f"Saved main content to {file_name}")

#         # Optional: Pause to avoid overwhelming the server
#         sleep(1)

#     except requests.exceptions.RequestException as e:
#         print(f"Failed to download {url}: {e}")
#     except Exception as e:
#         print(f"Error processing {url}: {e}")


# from data_ingestion.load_docs import LoadDocuments

# loadDoc = LoadDocuments(data_path="../data", url_file="data_ingestion/link_urls.txt")
# loadDoc.load_documents()