import chromadb
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings


load_dotenv()

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "hr_policies"
EMBEDDING_MODEL = "gemini-embedding-2"
GROQ_MODEL = "openai/gpt-oss-120b"

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

embedding_model = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)


def retrieve_chunks(query: str, top_k: int = 4):
    query_embedding = embedding_model.embed_query(query)

    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    return results


def ask_policy_question(query: str, top_k: int = 4):
    retrieved = retrieve_chunks(query=query, top_k=top_k)
    # answer = generate_answer(query=query, retrieved_chunks=retrieved)
    return retrieved


if __name__ == "__main__":
    answer = ask_policy_question("What is the leave carry forward policy?")
    print(answer)
