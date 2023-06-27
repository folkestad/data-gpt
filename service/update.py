from agents import bigquery_agents
from memory import chromadb_memory
from llm import models
from service.context import Context


def index(ctx: Context):
    chroma_client = chromadb_memory.client()
    chroma_client.reset()

    chroma_collection = chromadb_memory.create_collection(
        chroma_client,
        models.embedding_model_default(),
        ctx.CHROMADB_COLLECTION,
    )

    bigquery_client = bigquery_agents.client(ctx.GCP_PROJECT_ID)
    schemas = bigquery_agents.schemas(
        bigquery_client, ctx.GCP_PROJECT_ID, ctx.GCP_DATASET_ID
    )

    if ctx.DEBUG:
        print(f"{schemas=}")

    chromadb_memory.add(chroma_collection, schemas)
    chroma_client.persist()
