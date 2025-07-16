import os
from langchain_community.document_loaders import PyMuPDFLoader

def extract_pdf_to_txt():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.normpath(os.path.join(base_dir, '../data/bangalore_guide.pdf'))
    txt_path = os.path.normpath(os.path.join(base_dir, '../data/bangalore_guide.txt'))
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()
    with open(txt_path, 'w', encoding='utf-8') as f:
        for doc in docs:
            f.write(doc.page_content + '\n')
