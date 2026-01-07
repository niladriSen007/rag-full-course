from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader

documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
]

# Reading a text file and creating Document objects:
sample_text_file = {
    "data/inngestion.txt": """
        Sir Ratan Naval Tata (1937-2024)

Sir Ratan Tata was one of India's most respected industrialists and philanthropists. He served as the Chairman of Tata Sons from 1991 to 2012 and interim chairman from October 2016 to February 2017.

Key Achievements:
- Led the Tata Group's global expansion, including landmark acquisitions like Tetley Tea (2000), Corus Steel (2007), and Jaguar Land Rover (2008)
- Transformed Tata Group into a multinational conglomerate with operations in over 100 countries
- Launched the Tata Nano, aimed at making car ownership accessible to middle-class Indians
- Championed innovation and entrepreneurship through Tata Group companies

Philanthropy:
- Approximately 65% of Tata Sons' equity is held by philanthropic trusts established by the Tata family
- Contributed significantly to education, healthcare, and rural development
- Supported initiatives in cancer research, arts, and disaster relief
- Personal donations to institutions like Harvard Business School, Cornell University, and IIT Bombay

Awards and Recognition:
- Padma Bhushan (2000) and Padma Vibhushan (2008), India's highest civilian honors
- Honorary Knight Grand Cross of the Order of the British Empire (2009)
- Numerous honorary doctorates from universities worldwide

Legacy:
Known for his humility, ethical leadership, and commitment to nation-building. His vision combined business excellence with social responsibility, setting standards for corporate governance and philanthropy in India.
    """
}
for filePath, content in sample_text_file.items():
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(content)

print("Sample text file created for ingestion.")

## load a single text file
loader = TextLoader("data/inngestion.txt", encoding="utf-8")
text_document = loader.load()

# print(type(documents))
# print(documents[0].page_content[:500])  # print first 500 characters


## load multiple text files
dir_loader = DirectoryLoader(
    "data/", glob="*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"}
)
documents = dir_loader.load()
# print(f"Loaded {len(documents)} documents from directory.")


## text splitting strategies
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
)
texts = text_splitter.split_text(text_document[0].page_content)
# print(f"Split into {len(texts)} chunks.")
# print(type(texts[0]))
