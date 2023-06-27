import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings

from agents.bigquery_agents import Document


def client() -> chromadb.Client:
    chromadb_client = chromadb.Client(
        Settings(chroma_db_impl="duckdb+parquet", persist_directory=".chroma_persist")
    )
    return chromadb_client


def create_collection(
    chromadb_client: chromadb.Client,
    embedding_function: embedding_functions.EmbeddingFunction,
    collection_name: str,
):
    collection = chromadb_client.create_collection(
        name=collection_name, embedding_function=embedding_function
    )
    return collection


def get_collection(
    chromadb_client: chromadb.Client,
    embedding_function: embedding_functions.EmbeddingFunction,
    collection_name: str,
):
    collection = chromadb_client.get_collection(
        name=collection_name, embedding_function=embedding_function
    )
    return collection


def add(collection, documents: list[Document]):
    collection.add(
        documents=[document.schema for document in documents],
        ids=[document.name for document in documents],
    )


def query(collection, query_texts, n_results) -> list[Document]:
    result = collection.query(
        query_texts=query_texts,
        n_results=n_results,
    )
    ids = result["ids"][0]
    documents = result["documents"][0]
    mapped_documents = []
    for _id, document in zip(ids, documents):
        mapped_documents.append(Document(_id, document))
    return mapped_documents
