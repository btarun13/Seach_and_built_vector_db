# Build Vector DB and RAG(Will be updated)

Search and Download papers on specific smiles. Then building Pinecone vector database.

This was an idea when I was working on this dataset from: https://archive.ics.uci.edu/dataset/1104/drug_induced_autoimmunity_prediction

Suppose, You want to build my own database from all medical literature on a given molecule. With this project I try to extract all freely available papers on the molecule/term. After, The code automatically downloads pdfs on directory locally.

Research_papers directory which will have pdfs is translated into embeddings for vector database(Pinecone). Then pdfs are deleted, this is because you don't want to clog your system memory. Every thing is now on pinecone database. 

In final part we just use this index for answering queries and citing sources. In case, you ask about something that is not in database, it will tell you that you don't have any information. This is a rudimentary RAG, it is slow. In case you want to use it bigger projects you would need to parallelize the code.
