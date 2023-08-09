from agents import bigquery_agents
from llm.models import embedding_model_default
from memory import chromadb_memory
from service.context import Context
from service.document import Document


def sql_in_bigquery(ctx: Context, sql: str) -> str:
    # Query BigQuery
    bigquery_client = bigquery_agents.client(ctx.GCP_PROJECT_ID)
    query_answer = bigquery_agents.query(bigquery_client, sql, dry_run=ctx.DRY_RUN)
    if ctx.DEBUG:
        print(f"{query_answer=}")

    if ctx.DRY_RUN:
        raise Exception("Dry run")

    return query_answer


def search_in_store(ctx: Context, search_text: str) -> list[Document]:
    chromadb_client = chromadb_memory.client()
    chromadb_collection = chromadb_memory.get_collection(
        chromadb_client,
        embedding_model_default(),
        ctx.CHROMADB_COLLECTION,
    )
    documents = chromadb_memory.query(
        chromadb_collection, search_text, n_results=ctx.CHROMADB_N_RESULTS
    )
    return documents
