#!/usr/bin/env python3
import subprocess
from Bio import Entrez
import pubchempy as pcp
import openai
from pinecone import Pinecone, ServerlessSpec
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI
from typing import List, Dict
from pinecone import Index
import numpy as np


#### change these and add in your own API keys

openai.api_key = "sk-proj-T0Oc*********TXAA"  # Your OpenAI key here
client = OpenAI(api_key = openai.api_key)
MODEL = "text-embedding-ada-002"
pc = Pinecone(api_key="pcsk_4bbPdM_*********D6TTk8sQB")  # Your Pinecone API key




def upsert_embeddings(index: Index, embeddings: List[List[float]], texts: List[str], name_integ: str, batch_size: int = 100):
    """Upserts embeddings into the Pinecone index in batches."""
    vectors = []
    for i, (embedding, text) in enumerate(zip(embeddings, texts)):
        vectors.append({
            "id": name_integ + f"chunk-{i}",
            "values": embedding,
            "metadata": {"text": text}
        })

    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        try:
            index.upsert(vectors=batch)
            print(f"Upserted batch {i // batch_size + 1} of {len(vectors) // batch_size + (1 if len(vectors) % batch_size != 0 else 0)}")
        except PineconeApiException as e:
            print(f"Error upserting batch {i // batch_size + 1}: {e}")
            # You might want to add more sophisticated error handling here,
            # like logging the failed batch or retrying.


def run_bash_script(script_path, args):
    try:
        process = subprocess.run(
            [script_path] + args,  # Combine script path and arguments
            check=True,           # Raise an exception for non-zero return codes
            capture_output=True,  # Capture stdout and stderr
            text=True             # Decode output as text (UTF-8 by default)
        )
        return process.returncode, process.stdout, process.stderr
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout, e.stderr
    except FileNotFoundError:
        return 1, "", f"Error: Script not found at {script_path}"

def pubmed_search_get_id(smiles,email):
    Entrez.email = email
    compounds = pcp.get_compounds(smiles, 'smiles')
    search_terms = compounds[0].synonyms #['Zileuton, (S)-', '(-)-zileuton']

    all_pmids = set()

    for term in search_terms:
        try:
            handle = Entrez.esearch(db="pubmed", term=term, retmax="100")  # Adjust retmax as needed
            record = Entrez.read(handle)
            handle.close()
            if record and 'IdList' in record:
                for pmid in record['IdList']:
                    all_pmids.add(pmid)
                print(f"Found {len(record['IdList'])} PMIDs for term: '{term}'")
            else:
                print(f"No PMIDs found for term: '{term}'")
        except Exception as e:
            print(f"Error searching PubMed for term '{term}': {e}")

    if all_pmids:
        print("\n Freely available papers for the search terms will be downloaded")
        # for pmid in sorted(list(all_pmids)):
        #     print(pmid)
    else:
        print("\nNo PubMed IDs found for any of the search terms.")
    return all_pmids

def search_n_download(term,email,script_path,percent_paper_download):

    pubmed_ids = pubmed_search_get_id(smiles = term, email = email)
    script_path = script_path  # Replace with the actual path
    number_papers = int((percent_paper_download/100)*len(pubmed_ids))  # Number of papers to download
    pubmed_ids = list(pubmed_ids)[0:number_papers]  # Example list of IDs

    return_code, stdout, stderr = run_bash_script(script_path, pubmed_ids)

    print(f"Return Code: {return_code}")
    if stdout:
        print("Standard Output:")
        print(stdout)
    if stderr:
        print("Standard Error:")
        print(stderr)

    if return_code == 0:
        print("Script executed successfully.")
    else:
        print("Script execution failed.")

# ----📄 Process PDF ----
def process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(pages)
    return [chunk.page_content for chunk in chunks]


def create_embeddings(texts):
    embeddings = []
    for text in texts:
        response = client.embeddings.create(
            input=text,
            model=MODEL,
        )
        embeddings.append(response.data[0].embedding)
    return embeddings

