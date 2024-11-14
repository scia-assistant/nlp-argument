# Project name

<!-- TABLE OF CONTENTS -->

# 📗 Table of Contents
- [🚀 Description](#description)
- [👥 Authors](#authors)

## 🚀 Description <a name="description"></a>

This project aims to create a tool that enhances understanding and analysis of arguments by improving comprehension of both their structure and content. Ultimately, this would
offer a way to assess the quality and validity of an argument in a more efficient and reliable way. \
In a world where we are constantly exposed to huge amounts of information and persuasive arguments, it can be challenging to determine their validity in a reasonable amount of time.
This tool could help fight misinformation by providing a quick, detailed and well-sourced analysis of any argument. This way it could identify inconsistencies, rhetorical manipulation
and other misleading tactics in arguments across various fields such as politics, media and public discourse empowering users to critically assess the credibility and reliability of any
information they encounter.

In order to provide this detailed analysis, the project has two primary focuses:

- It will combine an open-source language model (LLM) with a Retrieval-Augmented Generation (RAG) to detect fallacious arguments. This combination will precisely categorize fallacies, explain
their underlying basic and provide sourced examples of similar arguments. This feature will be easily accessible through a user-friendly chatbot interface making it simple and intuitive to use.
- It will enhance the logical reasoning abilities of the model through a logic-based language or library, which can also enhance the explainability of the model's results.
This functionality can be divided into two sub-tasks:
	- Decomposing natural language sentences into basic logical elements.
	- Representing the logical structure of sentences or answering logical questions based on this structure.

Current LLMs, while highly capable in generating coherent text and providing contextually relevant responses, often struggle with logical reasoning and structured argument analysis. They may
sometimes produce convincing yet logically flawed responses or fail to detect subtleties in complex arguments. Our project aims to address this gap by providing an alternative approach.
Our goal is to develop a model that either has the same performance of current LLMs with fewer parameters (reducing computational costs) or exceeds their performance. So by combining RAG
with advanced logic tools, we aim to create a powerful, cost-effective solution that brings more rigorous logical understanding to argument analysis.

## Project background (~400 words)
	This part explores what has been done by other people in the line of work of the project from a technical / industrial / research point of view. Stress out how your project is different/similar to these other works.

## Project steps (Bullet points)
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
	- **Benchmark Analysis **: Evaluate our MVP model against the highest-performing LLMs with significantly larger parameter counts.
- **Develop a User Interface (UI) for LLM Interaction** (dorian.penso)
	- **Design the Interface Layout**: Sketch the layout for an intuitive user experience that facilitates interaction with the LLM.
	- **Choose the Technology Stack**: Decide on the frontend technology (e.g., React, Angular, Vue) and backend framework (e.g., Node.js, Django) for the UI.
	- **Develop the Interface**: Build and integrate the UI, ensuring it communicates seamlessly with the LLM and backend.
	- **Model Deployment**: Integrate the model with the UI, ensuring efficient loading and data handling.

## First results (min. 200 words)
	This part presents the first results of the project. It can be negative results (“we made the whole pipeline and it does not work, we have errors X and problems Y”) or issues with a first version (“we made our application and it is slow / it does not solve problem X”). If your project is more R&D-like, it can be reproducing the results of a paper + a first experiment in the direction you would like to explore. Please include problems you faced with / are facing and ideas about how to tackle them.


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
