nlp-argument Documentation
==========================

Welcome to the documentation for the **nlp-argument** project. This guide provides comprehensive details on each module, class, and function, with a focus on the data ingestion process, including loading, retrieving, and processing data.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   data_ingestion/index  # Including the data_ingestion module documentation
   faiss_index/index     # Optional if you have documentation for faiss_index
   rag/index             # Optional if you have documentation for rag
   other_modules         # Optional, for any other modules

Overview
--------

This project is organized into several main modules:

- **data_ingestion**: Handles data loading, retrieval, and processing.
- **faiss_index**: Manages the creation and storage of FAISS indexes for efficient similarity search.
- **rag**: Implements retrieval-augmented generation (RAG) for NLP tasks.
- **Test Modules**: Contains unit tests and linting scripts to ensure code quality and functionality.

Detailed Module Documentation
=============================

.. toctree::
   :maxdepth: 1
   :caption: Modules:

   data_ingestion.load
   data_ingestion.load_docs
   data_ingestion.retriever

data_ingestion Package
======================

The `data_ingestion` package provides functionalities to load, retrieve, and process documents. It includes the following submodules:

Submodules
----------

data_ingestion.load module
--------------------------

This module provides functions for loading data from various sources.

.. automodule:: data_ingestion.load
   :members:
   :undoc-members:
   :show-inheritance:

data_ingestion.load_docs module
-------------------------------

This module contains functions for loading documentation-specific data.

.. automodule:: data_ingestion.load_docs
   :members:
   :undoc-members:
   :show-inheritance:

data_ingestion.retriever module
-------------------------------

This module is responsible for retrieving data from specified sources.

.. automodule:: data_ingestion.retriever
   :members:
   :undoc-members:
   :show-inheritance:

Module Contents
---------------

Below is the full content of the `data_ingestion` package, including all classes, functions, and attributes.

.. automodule:: data_ingestion
   :members:
   :undoc-members:
   :show-inheritance:

Getting Started
---------------

Refer to the **Contents** section above to access the detailed documentation for each module. For an introduction to the project’s purpose and usage examples, see the **Overview** section.
