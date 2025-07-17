"""
NammaAI Utility Functions

Purpose: Contains utility functions for the NammaAI system, primarily for PDF processing.
This module handles the extraction and conversion of the Bangalore City Guide PDF 
into text format for use in the RAG (Retrieval-Augmented Generation) system.

Key Functions:
- extract_pdf_to_txt(): Converts PDF guide to text with error handling and optimization
"""

import os
from langchain_community.document_loaders import PyMuPDFLoader

def extract_pdf_to_txt():
    """
    Extract text from Bangalore guide PDF and save to text file.
    This ensures the text version is always available for processing.
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.normpath(os.path.join(base_dir, '../data/bangalore_guide.pdf'))
        txt_path = os.path.normpath(os.path.join(base_dir, '../data/bangalore_guide.txt'))
        
        # Skip if text file already exists and is newer than PDF
        if os.path.exists(txt_path) and os.path.exists(pdf_path):
            if os.path.getmtime(txt_path) > os.path.getmtime(pdf_path):
                return
        
        loader = PyMuPDFLoader(pdf_path)
        docs = loader.load()
        
        with open(txt_path, 'w', encoding='utf-8') as f:
            for doc in docs:
                f.write(doc.page_content + '\n')
                
    except Exception as e:
        print(f"Warning: Could not extract PDF to text: {e}")
        print("Make sure bangalore_guide.pdf exists in the data folder.")
