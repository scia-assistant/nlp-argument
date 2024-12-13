# Fact and consistency checker for law.

<!-- TABLE OF CONTENTS -->

# 📗 Table of Contents
- [🚀 Description](#description)
- [🗂️ Project background](#background)
- [🪜 Project steps](#steps)
- [🔬 First results](#first_results)
- [⚙️ Setup](#setup)
- [👥 Authors](#authors)

## 🚀 Description <a name="description"></a>

In French law, judges and legal practitioners rely significantly on structured argumentation to resolve cases where legal provisions may be ambiguous, incomplete, or require contextual interpretation. The capacity to construct, analyze, and validate legal arguments is essential to ensure fair and just outcomes. Addressing these challenges requires decisions grounded not only in statutory law but also in logically sound and valid arguments.

Our goal is to develop a tool that helps checking the truthfulness of an assertion, an argument or even a speech in the law domain.
Checking the truthfulness relies on two main things, checking the facts and checking the consistency.

Thus, the project has two primary focuses:
- Combines an open-source language model (LLM) with a Retrieval-Augmented Generation (RAG) to retrieve relevant French jurisprudence and provide sourced examples.
- Combines an open-source language model (LLM) with a logic-based language/library to check the consistency of argument. This combination should be able to detect basic fallacious assertion and explain why an argument is consistent or not. LLM responses must be based on formal logic rules but convert it to human language for understanding purposes.


Both of these features will be easily accessible through a user-friendly chatbot interface making it simple and intuitive to use.

A practical use-case involves a legal practitioner faced with making a decision. In formulating a legal argument, the practitioner must have a thorough understanding of the law and the ability to structure the argument in a clear and logical manner. He would then use these models to be able to retrieve lawful information and be able to create a logical reasoning to construct his legal argument.
Another use-case involves an average person who would just want to get answers from truthful sources.
 
Current open-source LLMs demonstrate a reasonable ability to generate coherent text and provide relevant responses. However, they often struggle to deliver high-quality outputs in highly specialized technical domains. Additionally, their reasoning capabilities can be limited, depending on the specific LLM employed.
Our objective is to develop a model that either matches the performance of existing LLMs with a smaller architecture (thus reducing computational costs) or surpasses their performance altogether.

## 🗂️ Project background <a name="background"></a>
- **The Jurisprudence Assistance System**
	- Related works:
		- https://arxiv.org/pdf/2010.02559 - LEGAL-BERT: The Muppets straight out of Law School: LEGAL-BERT is a specialized adaptation of the Bidirectional Encoder Representations from Transformers (BERT) model, tailored specifically for the legal domain. This model aims to improve the model in the law domain without the use of RAG.
		- https://arxiv.org/abs/2306.05685 - Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena: They use a strong LLMs as judges to evaluate models on more open-ended questions.
	
	- Differences: 
		- Model Size: Focusing on open-source small language models can offer advantages in terms of computational efficiency and deployment feasibility, especially in resource-constrained environments.

		- Specialized Legal Corpus: Utilizing a unique dataset, such as French Jurisprudence case law, can provide tailored insights not covered by existing models. Jurisprudenca cases happen everyday so it is good to update our database withouth having to retrain or finetune the models

- **Develop Analytical Logic for Large Language Model (LLM)**
	- Related works :
		- https://github.com/ArgumentumGames/Argumentum/tree/semantic-kernel/Chatgpt-plugin : This is a project by an EPITA instructor who attempted to connect Chat-GPT4 to the "tweety" logic library implemented in Java. This project serves as the inspiration for our logic component. Our goal is similar—to enhance a language model’s understanding of rhetorical arguments by utilizing a logic-based language.
		- https://shchegrikovich.substack.com/p/use-prolog-to-improve-llms-reasoning : This focuses on solving various simpler logic problems, like mathematical challenges, with the aim of improving an LLM's reasoning abilities. The article details connections between the LLM and logic-based language, connections which we also intend to explore.
		- https://hackernoon.com/lang/fr/outil-d'exploration-raisonnement-int%C3%A9gr%C3%A9-innovation-ma%C3%AEtrise-des-math%C3%A9matiques-LLMs : This article presents open-source reasoning agents (TORA) and explains their operational methods.
	- Differences:
		- All of these articles rely on large models with many parameters (usually GPT-3 or GPT-4). Our work will focus on improving capacities of smaller LLMs.

## 🪜 Project steps <a name="steps"></a>
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

## 🔬 First results <a name="first_results"></a>
Initially, our project focused on developing a tool capable of analyzing arguments to determine whether they are fallacious and, if so, identifying the specific type of fallacy involved. The first part to achieve this, was utilizing a Retrieval-Augmented Generation (RAG) approach, combined with a comprehensive database of definitions and examples of various fallacious arguments.\
After creating the database, and implementing the RAG we quickly encountered a significant issue. The retrieved documents were not relevant at all. For example when giving to the model the argument "Katherine is a bad choice for mayor because she didn’t grow up in this town." which is a Ad hominem logical fallacy, the system retrieved documents solely based on surface-level keyword matches, such as those containing the word “mayor”. Since the retrieval search focus either on semantic or syntaxic similarities between the query and the documents, it revealed a critical gap in the model’s ability to understand and process the deeper logical structure of the argument, rather than merely focusing on superficial lexical overlaps.

We then began exploring alternative subjects and datasets where implementing a RAG system would be both contextually appropriate and capable of delivering meaningful and insightful results. Seeking a highly specific and structured domain, we turned our attention to the field of law, recognizing its potential for meaningful application, and more specifically French jurisprudence. After identifying our dataset, we then divided the project into main branches:
- **The Continuous Integration (CI)** which has been fully implemented in the environment. It enables automated checks for tests, workflow processes, and adherence to commit patterns. This ensures a streamlined and consistent development process, enhancing efficiency and reliability.
- **The Jurisprudence Assistance System**
	- For data storage, we have chosen FAISS as the indexing solution for effectively retrieving data in the RAG system. All indexes and corresponding text derived from our documents are stored in a MongoDB database, ensuring organized and accessible data management.
	- After an initial implementation of our RAG, we tested it by posing general questions about jurisprudence such as "Qu'est-ce qu'un litige?" (a question a student may have). The model successfully provided a correct answer, supported by examples of legal cases to enhance understanding and offer more depth in its explanation.
	- We have not yet conducted tests on the fact-checking component of our model.
- **Develop Analytical Logic for Large Language Model (LLM)**
	- Results were not promising. In fact, the first hypothesis was that LLM was good to translate logic problem formulated in natural language into logic based language. That is true for big LLM, not for small one (<2B parameters). It is already hard to generate a valid prolog (or even python) code of the problem "How much does 1+5 ?".
	- Fine-tuning may be a solution. Fine-tuning on a specific programming language might improve their capacities to translate natural language to this programming language.
	- Test were made on a local machine with few resources. A solution would be to use GPUs on google colab or azure resources to use bigger model (Llama with 7B parameters for example).  
- **The User Interface**, designed for interacting with the LLM, is currently in the prototype stage. At this point, it is not functional or ready for use, as further development and refinement are required.



## ⚙️ Setup <a name="setup"></a>

To download commit checker and requirement:
- `make dev-setup`

To check the unittest test suite:
- `make check`

### How to start





**To test the RAG locally**, do the following instructions:
If it is the first time you are running the project, go to the `src/test_rag.py` file and set the `create_faiss` boolean to `True`. Then run the following command:
```sh
$ python src/test_rag.py
```
This command takes a bit of time, but you just have to it once. This will create a directory `src/faiss_index`.
Then the code inside the `main` function will be executed (with the given query).

Before running it again with another query make sure you change back the `create_faiss` boolean to `False`.

**To test the RAG inside the chatbot**:
1. Make sure you have the `src/faiss_index` directory created (check the part "To test the RAG locally" for more instructions)
2. Loof at the `docker-compose.yml` file and check if the port of `nginx` is set up for local start
3. Run the following command
```sh
$ docker compose up
```
4.  Go to http://localhost:8085
5.  Connect with the following credentials:
    - Username: `contextor`
    - Password: `robot`
6.  Chat with the AI

### CI/CD Workflow Steps

#### Linting
- Perform code linting with the following checks:
    - flake8 for code style compliance.
    - mypy for type checking.
    - Allow lines up to 100 characters in length.

#### Testing
- Run tests on all Python files prefixed with test_ located in the tests folder.
- Ensure the testing environment is configured to use Python 3.10.

#### Deployment
- Deployment relies on GitHub Actions' Secret Variables for configuration:
    - SSH_HOST: Host address of the virtual machine (VM).
    - SSH_USER: Username for SSH connection to the VM.
    - SSH_PWD: Password for the SSH user.
- Pre-deployment Checks:
    - Verify that the VM is running. If the VM is not running, the CI pipeline skips the deployment process.

- Deployment Process:
    - The CI pipeline begins by copying the entire project to the VM in the nlp-argument folder using rsync.
    - Establish an SSH connection to the VM.
    - Stop the currently running Docker container for the project.
    - Restart the container with the updated project files, applying the necessary changes.

## 👥 Authors <a name="authors"></a>
- Dorian Penso
- Léa Margery
- Maxime Buisson
- Sacha Hibon