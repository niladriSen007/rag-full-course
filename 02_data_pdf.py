from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List


## load the PDF file
try:
    # loader = PyPDFLoader("data/node.pdf")
    loader = PyMuPDFLoader("data/node.pdf")
    pdf_documents = loader.load()
    print(f"Loaded {len(pdf_documents)} pages from the PDF document.")
except Exception as e:
    print(f"Error loading PDF document: {e}")


class SmartPdfProcessor:
    """Advance PDF processing with proper error handling"""

    def __init__(self, chunk_size=1000, chunk_overlap=0):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.textSplitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""],
            length_function=len,
        )

    def clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # rremove extra whitespace
        text = " ".join(text.split())

        # Replace common ligatures
        text = text.replace("ﬁ", "fi")
        text = text.replace("ﬂ", "fl")
        text = text.replace("ﬀ", "ff")
        text = text.replace("ﬃ", "ffi")
        text = text.replace("ﬄ", "ffl")
        text = text.replace("ﬆ", "st")

        return text

    def process_pdf(self, file_path: str) -> List[Document]:
        """Process the PDFwith smart chunkingand metadata enhancement"""
        ## load the PDF file
        try:
            loader = PyMuPDFLoader(file_path)
            pdf_documents = loader.load()

            processed_documents = []

            for page_number, page in enumerate(pdf_documents):
                cleaned_text = self.clean_text(page.page_content)
                if len(cleaned_text) <= 50:
                    continue  # Skip empty pages
                chunks = self.textSplitter.create_documents(
                    texts=[cleaned_text],
                    metadatas=[
                        {
                            **page.metadata,
                            "source": f"{file_path}_page_{page_number + 1}",
                            "page_number": page_number + 1,
                            "total_pages": len(pdf_documents),
                            "char_count": len(cleaned_text),
                        }
                    ],
                )
                processed_documents.extend(chunks)
            return processed_documents
        except Exception as e:
            print(f"Error loading PDF document: {e}")
            return []


pdf_processor = SmartPdfProcessor(chunk_size=800, chunk_overlap=100)

try:
    processed_docs = pdf_processor.process_pdf("data/node.pdf")
    print(f"Processed {len(processed_docs)} document chunks from the PDF.")
except Exception as e:
    print(f"Error processing PDF document: {e}")
