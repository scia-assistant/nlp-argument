# French jurisprudence RAG

<!-- TABLE OF CONTENTS -->

# 📗 Table of Contents
- [🚀 Description](#description)
- [👥 Authors](#authors)

## 🚀 Description <a name="description"></a>

French jurisprudence plays a critical role in interpreting and applying legal principles within the framework of the civil law system. Judges and legal practitioners rely on jurisprudence to navigate areas where statutes may be ambiguous, silent, or require contextual interpretation. In contemporary legal practice, jurisprudence is increasingly essential for addressing complex and evolving societal issues, such as digital rights, environmental law, and international disputes. With the proliferation of legal rulings across various courts, including the Cour de cassation and Conseil d’État, accessing and synthesizing relevant case law has become a challenge.\
To address this challenge, this project aims to create a tool that not only efficiently retrieves relevant case law but also leverages this contextual data to generate accurate and comprehensive answers to user queries. By combining advanced retrieval techniques with contextualized response generation, the model ensures precise, actionable insights tailored to the complexities of French jurisprudence.\
This tool will have a wide range of use cases across the legal ecosystem. Legal professionals, such as lawyers and judges, can use it to quickly identify relevant precedents and obtain summaries or explanations of case law tailored to specific legal arguments. Academics and students can leverage the system for research, enabling them to explore legal principles, analyze historical trends, or understand nuanced judicial decisions in depth. Finally, it can also empower citizens by offering transparent and easy-to-understand explanations of legal matters, fostering greater access to justice.

The project has two primary focuses:
- It will combine an open-source language model (LLM) with a Retrieval-Augmented Generation (RAG) to retrieve relevant French jurisprudence and provide sourced examples. This feature will be easily accessible through a user-friendly chatbot interface making it simple and intuitive to use.
<!-- - It will enhance the logical reasoning abilities of the model through a logic-based language or library, which can also enhance the explainability of the model's results.
This functionality can be divided into two sub-tasks:
	- Decomposing natural language sentences into basic logical elements.
	- Representing the logical structure of sentences or answering logical questions based on this structure. -->

Current open-source LLMs are more or less capable in generating coherent text and providing relevant responses. However, they often fall short when tasked with producing high-quality outputs in highly specific technical domains.
Our project seeks to tackle this limitation by equipping the model with highly relevant contextual information, enabling them to generate significantly improved and more accurate text.
Our goal is to develop a model that either has the same performance of current LLMs (such as GPT-4) with a smaller model (reducing computational costs) or exceeds their performance. 
So by integrating Retrieval-Augmented Generation with French jurisprudence, we aim to create a powerful and cost-effective solution that revolutionizes access to legal knowledge, bringing clarity, efficiency, and precision to the complexities of case law analysis.

## Project background (~400 words)
	This part explores what has been done by other people in the line of work of the project from a technical / industrial / research point of view. Stress out how your project is different/similar to these other works.

- **Develop Analytical Logic for Large Language Model (LLM)**
	- Related works :
		- https://github.com/ArgumentumGames/Argumentum/tree/semantic-kernel/Chatgpt-plugin : This is a project by an EPITA instructor who attempted to connect Chat-GPT4 to the "tweety" logic library implemented in Java. This project serves as the inspiration for our logic component. Our goal is similar—to enhance a language model’s understanding of rhetorical arguments by utilizing a logic-based language.
		- https://shchegrikovich.substack.com/p/use-prolog-to-improve-llms-reasoning : This focuses on solving various simpler logic problems, like mathematical challenges, with the aim of improving an LLM's reasoning abilities. The article details connections between the LLM and logic-based language, connections which we also intend to explore.
		- https://hackernoon.com/lang/fr/outil-d'exploration-raisonnement-int%C3%A9gr%C3%A9-innovation-ma%C3%AEtrise-des-math%C3%A9matiques-LLMs : This article presents open-source reasoning agents (TORA) and explains their operational methods.
	- Differences:
		- All of these articles rely on large models with many parameters (usually GPT-3 or GPT-4). Our work will focus on improving capacities of smaller LLMs.

## Project steps
- **Setting Up Continuous Integration (CI)** (dorian.penso)
	- **Set Up Workflow Checks**: Use GitHub Actions to create workflows that automatically check the consistent code style and quality.
	- **Automate Tests**: Configure GitHub Actions to run automated tests on every commit or pull request to ensure code reliability.
	- **Enforce Commit Patterns**: Implement commit message guidelines to maintain consistency across the project.
- **Data Storage Strategy** (dorian.penso && maxime.buisson)
	- **Define Data Requirements**: Identify the types and sources of data to be stored (static or dynamic data).
	- **Select Storage Solutions and Frameworks**: Choose the appropriate storage technology (e.g., SQL, NoSQL, cloud storage, datalake) and framework based on project needs.
	- **Implement Data Storage**: Set up the chosen storage solution and integrate it with the project.
	- **Prepare Data for Retrieval-Augmented Generation (RAG)**: Organize and format data to be compatible with RAG requirements for efficient retrieval and processing.
- **Implement (RAG)** (lea.margery && maxime.buisson)
	- **Chose Embedding Model**: Select an embedding model that can effectively convert text into dense vector representations, allowing for efficient similarity searches during retrieval.
	- **Set Up Retriever**: Configure a retrieval system that can search through indexed embeddings and return the most relevant documents based on an input.
	- **Chose Generation Model**: Choose an open-source, lightweight generative model capable of using the retrieved documents to generate coherent responses 
- **Develop Analytical Logic for Large Language Model (LLM)** (sacha.hibon)
	- **Structure pipeline** : Connect LLM to a logic based language.
	- **Simple logic problem** : Test on simple math problem or problem with many variables...
	- **Logic argument**: Test on simple and hard argument. The final model must be able to deduce the structure of the argument and test its truthfulness.
	- **(Optional) Fine-tuning** : Fine-tune the used LLM on logic syntax. It may improve the LLM translation of natural language to logic language.
- **Evaluate Language Model (LLM) Performance** (lea.margery)
	- **Test Performance with RAG**: Conduct tests to assess how well the LLM performs when using RAG, measuring factors like accuracy and response time.
	- **Test Performance without RAG**: Run parallel tests without RAG to establish a baseline and compare performance metrics.
	- **Benchmark Analysis**: Evaluate our MVP model against the highest-performing LLMs with significantly larger parameter counts.
- **Develop a User Interface (UI) for LLM Interaction** (dorian.penso)
	- **Design the Interface Layout**: Sketch the layout for an intuitive user experience that facilitates interaction with the LLM.
	- **Choose the Technology Stack**: Decide on the frontend technology (e.g., React, Angular, Vue) and backend framework (e.g., Node.js, Django) for the UI.
	- **Develop the Interface**: Build and integrate the UI, ensuring it communicates seamlessly with the LLM and backend.
	- **Model Deployment**: Integrate the model with the UI, ensuring efficient loading and data handling.

## First results (min. 200 words)
	This part presents the first results of the project. It can be negative results (“we made the whole pipeline and it does not work, we have errors X and problems Y”) or issues with a first version (“we made our application and it is slow / it does not solve problem X”). If your project is more R&D-like, it can be reproducing the results of a paper + a first experiment in the direction you would like to explore. Please include problems you faced with / are facing and ideas about how to tackle them.

- **Develop Analytical Logic for Large Language Model (LLM)**
	- Results were not promising. In fact, the first hypothesis was that LLM was good to translate logic problem formulated in natural language into logic based language. That is true for big LLM, not for small one (<2B parameters). It is already hard to generate a valid prolog (or even python) code of the problem "How much does 1+5 ?".
	- Fine-tuning may be a solution. Fine-tuning on a specific programming language might improve their capacities to translate natural language to this programming language.
	- Test were made on a local machine with few resources. A solution would be to use GPUs on google colab or azure resources to use bigger model (Llama with 7B parameters for example).  


## Additional content (optional)
Github repo:
Project demo:

## 👥 Authors <a name="authors"></a>
- Dorian Penso
- Léa Margery
- Maxime Buisson
- Sacha Hibon

## Setup

To download commit checker and requirement:
- `make dev-setup`

## Check Test

To check the unittest test suite:
- `make check`
