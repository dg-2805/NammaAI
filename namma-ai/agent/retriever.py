"""
NammaAI Retrieval System - RAG Implementation

Purpose: Implements the Retrieval-Augmented Generation (RAG) system for NammaAI.
This module handles the ChromaDB vector store creation, document chunking, embeddings,
and semantic search functionality for the Bangalore City Guide PDF.

Key Components:
- ChromaDB vector store with HuggingFace embeddings
- Document chunking with RecursiveCharacterTextSplitter
- Semantic search for relevant content retrieval
- Integration with PDF text extraction

Tech Stack:
- ChromaDB for vector storage
- HuggingFace sentence-transformers for embeddings
- LangChain for document processing
"""

import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from agent.utils import extract_pdf_to_txt

load_dotenv()

# Always extract PDF to text at startup
extract_pdf_to_txt()

def load_vector_store():
    """
    Load or create ChromaDB vector store from the Bangalore guide text.
    Returns the vector database for semantic search.
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        txt_path = os.path.normpath(os.path.join(base_dir, '../data/bangalore_guide.txt'))
        
        if not os.path.exists(txt_path):
            raise FileNotFoundError(f"Text file not found: {txt_path}")
            
        loader = TextLoader(txt_path, encoding='utf-8')
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectordb = Chroma.from_documents(
            chunks, 
            embedding=embeddings, 
            persist_directory=os.path.normpath(os.path.join(base_dir, '../data/vector_store'))
        )
        return vectordb
    except Exception as e:
        print(f"Error loading vector store: {e}")
        print("Make sure the Bangalore guide text file exists and is readable.")
        raise

def query_guide(query: str, vectordb, k=5):
    """
    Query the vector database for relevant content from the Bangalore guide.
    
    Args:
        query: The search query
        vectordb: ChromaDB vector store
        k: Number of similar chunks to retrieve
        
    Returns:
        Combined text content from relevant chunks
    """
    try:
        results = vectordb.similarity_search(query, k=k)
        return "\n".join([r.page_content for r in results])
    except Exception as e:
        print(f"Error querying guide: {e}")
        return ""
