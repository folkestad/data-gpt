import chromadb
from chromadb.utils import embedding_functions


def client_and_collection(
    embedding_function: embedding_functions.OpenAIEmbeddingFunction,
    collection_name: str,
):
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(
        name=collection_name, embedding_function=embedding_function
    )
    return chroma_client, collection


def add(collection, documents):
    collection.add(documents=documents, ids=[str(i) for i in range(len(documents))])


def query(collection, query_texts, n_results) -> str:
    return collection.query(
        query_texts=query_texts,
        n_results=n_results,
    )
