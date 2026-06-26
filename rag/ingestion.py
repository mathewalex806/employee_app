from dataclasses import dataclass
from pypdf import PdfReader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import chromadb
import uuid


@dataclass
class RawDocument:
    source: str
    file_type: str
    text: str


ALLOWED_SUFFIX = [".txt", ".pdf", ".md"]
EMBEDDING_MODEL = "gemini-embedding-2"


def ingest_pdf(path: str) -> RawDocument:
    reader = PdfReader(path)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text
    return RawDocument(source=path, file_type="PDF", text=full_text)


def ingest_text(path: str) -> RawDocument:
    with open(path, "r") as file:
        full_text = ""
        for line in file:
            full_text += line.strip()
        return RawDocument(source=path, file_type="TEXT/MD", text=full_text)


def ingest_policies_directory(path: str = "hr_policies"):
    directory = Path(path)
    raw_document = []
    for file_path in directory.rglob("*"):
        if file_path.suffix in ALLOWED_SUFFIX:
            print(file_path)
            if file_path.suffix == ".pdf":
                raw_document.append(ingest_pdf(path=file_path))
            elif file_path.suffix in (".txt", ".md"):
                raw_document.append(ingest_text(path=file_path))
    return raw_document


def ingest_file(path: str):
    file_path = Path(path)
    if file_path.suffix not in ALLOWED_SUFFIX:
        print("Failed to load document: Unsupported type")
        return
    if file_path.suffix == ".pdf":
        return [ingest_pdf(path=file_path)]
    elif file_path.suffix == ".txt" or file_path.suffix == ".md":
        return [ingest_text(path=file_path)]


def load_file(path: str):
    ingested_file = ingest_file(path=path)
    chunks = chunk_documents(ingested_file)
    embeddings = embed_chunks(chunks=chunks)
    store_in_chroma(chunks=chunks, embeddings=embeddings)


def chunk_documents(raw_documents: list[RawDocument]):
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=50)
    documents = [
        Document(
            page_content=doc.text,
            metadata={"source": str(doc.source), "file_type": doc.file_type},
        )
        for doc in raw_documents
    ]
    return splitter.split_documents(documents)


def embed_chunks(chunks: list[Document]):
    embedding_model = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    texts = [chunk.page_content for chunk in chunks]
    return embedding_model.embed_documents(texts)


def store_in_chroma(chunks: list[Document], embeddings: list[list[float]]):
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="hr_policies")
    ids = [chunk.metadata["source"] + str(uuid.uuid4()) for chunk in chunks]
    documents = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    collection.add(
        ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas
    )


raw_docs = ingest_policies_directory()
chunks = chunk_documents(raw_docs)
embeddings = embed_chunks(chunks)
store_in_chroma(chunks, embeddings)
