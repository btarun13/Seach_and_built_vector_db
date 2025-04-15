# Build Vector DB and RAG(Will be updated)

Building a Vector Database of Research Papers from SMILES Strings

This idea originated while I was working with a dataset from the UCI Machine Learning Repository:
Drug-Induced Autoimmunity Prediction Dataset

The goal of this project is to build a custom knowledge base from medical literature for any given molecule, using its SMILES (Simplified Molecular Input Line Entry System) representation. Here's how the process works:

1. Search and Download Research Papers
Given a SMILES string (or a related keyword), the program automatically searches for and downloads all freely available research papers related to that molecule or term. These PDFs are saved locally in a directory called Research_papers.


2. Convert Papers to Embeddings
The downloaded PDFs are processed and converted into text embeddings. These embeddings are then uploaded to a Pinecone vector database, enabling efficient similarity-based search and retrieval.


3. Clean-Up
Once the embeddings are stored in Pinecone, the local PDF files are deleted to save disk space. This ensures the system doesn't become overloaded with files.


4. Querying the Database (RAG System)
The final component allows users to query the Pinecone index. The system retrieves relevant information and provides citations from the indexed papers. If a query doesn't match any data in the index, it will simply inform you that there’s no relevant information available.
This is a basic Retrieval-Augmented Generation (RAG) setup. While functional, it’s not highly optimized—it can be slow. For larger-scale applications, the code would need to be parallelized for better performance.