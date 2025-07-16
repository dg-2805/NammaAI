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
    base_dir = os.path.dirname(os.path.abspath(__file__))
    txt_path = os.path.normpath(os.path.join(base_dir, '../data/bangalore_guide.txt'))
    loader = TextLoader(txt_path, encoding='utf-8')
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=750, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=os.path.normpath(os.path.join(base_dir, '../data/vector_store')))
    return vectordb

def query_guide(query: str, vectordb, k=5):
    results = vectordb.similarity_search(query, k=k)
    return "\n".join([r.page_content for r in results])
