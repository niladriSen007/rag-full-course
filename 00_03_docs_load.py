from docx import Document as DocxDocument
from langchain_community.document_loaders import (
    Docx2txtLoader,
    UnstructuredWordDocumentLoader,
)
import os


try:
    docx_doc = Docx2txtLoader("data/para.docx")
    documents = docx_doc.load()
    print(f"Loaded {len(documents)} documents using Docx2txtLoader.")
    print(
        documents[0].page_content[:500]
    )  # Print first 500 characters of the first document
    print(f"Metadata: {documents[0].metadata}")
except Exception as e:
    print(f"Docx2txtLoader failed with error: {e}")
