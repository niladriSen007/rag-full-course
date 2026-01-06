from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader


## load the PDF file
try:
    # loader = PyPDFLoader("data/node.pdf")
    loader = PyMuPDFLoader("data/node.pdf")
    pdf_documents = loader.load()
    print(f"Loaded {len(pdf_documents)} pages from the PDF document.")
except Exception as e:
    print(f"Error loading PDF document: {e}")
