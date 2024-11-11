# Project name

## Team Member 1, …, Team Member n

## Project description (~400 words)

This part should describe the project in plain English, by introducing the context and explaining the specificity of the project (why is it something new/interesting?).
Describe a potential real-life use-case of your project. Explain the challenge you want to solve.

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
- **Implement (RAG)** (lea.margery)
	- **Chose Embedding Model**: Select an embedding model that can effectively convert text into dense vector representations, allowing for efficient similarity searches during retrieval.
	- **Set Up Retriever**: Configure a retrieval system that can search through indexed embeddings and return the most relevant documents based on an input.
	- **Chose Generation Model**: Choose an open-source, lightweight generative model capable of using the retrieved documents to generate coherent responses 
- **Develop Analytical Logic for Language Model (LLM) Optimization** (sacha.hibon)
	- **Create Custom Analytical Algorithms**: Implement logic that enhances the language model’s reasoning and output quality.
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
…
