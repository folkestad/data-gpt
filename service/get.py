import json

from rich import print
from columnar import columnar

from agents import bigquery_agents
from llm.models import embedding_model_default
from memory import chromadb_memory
from llm import guidance_pipelines, models
from service.context import Context
from service.document import Document


def question(ctx: Context, question_text: str) -> str:
    model = models.llm_model(
        ctx.MODEL_TYPE, ctx.MODEL_TYPE_LLM_MODEL, ctx.MODEL_TYPE_API_KEY
    )

    chromadb_client = chromadb_memory.client()
    chromadb_collection = chromadb_memory.get_collection(
        chromadb_client,
        embedding_model_default(),
        ctx.CHROMADB_COLLECTION,
    )

    # Find relevant tables to the question
    most_relevant_tables = chromadb_memory.query(
        chromadb_collection, question_text, n_results=ctx.CHROMADB_N_RESULTS
    )
    if ctx.DEBUG:
        print(f"{most_relevant_tables=}")

    # Generate SQL
    session1 = guidance_pipelines.generate_sql(
        llm=model,
        question=question_text,
        most_relevant_table=most_relevant_tables,
        silent=not ctx.DEBUG,
    )
    generated_sql: str = session1["sql"]
    if ctx.DEBUG:
        print(f"{generated_sql=}")

    if not generated_sql.startswith("SELECT"):
        raise Exception("SQL query is not SELECT")

    # Query BigQuery
    bigquery_client = bigquery_agents.client(ctx.GCP_PROJECT_ID)
    query_answer = bigquery_agents.query(
        bigquery_client, generated_sql, dry_run=ctx.DRY_RUN
    )
    if ctx.DEBUG:
        print(f"{query_answer=}")

    if ctx.DRY_RUN:
        raise Exception("Dry run")

    # Format answer
    session2 = guidance_pipelines.format_answer(
        llm=model,
        question=question_text,
        sql=generated_sql,
        answer=query_answer,
        silent=not ctx.DEBUG
    )
    response = session2["answer"]
    if ctx.DEBUG:
        print(f"{question_text=}")

    return response


def search(ctx: Context, search_text: str) -> str:
    chromadb_client = chromadb_memory.client()
    chromadb_collection = chromadb_memory.get_collection(
        chromadb_client,
        embedding_model_default(),
        ctx.CHROMADB_COLLECTION,
    )
    documents = chromadb_memory.query(
        chromadb_collection, search_text, n_results=ctx.CHROMADB_N_RESULTS
    )
    return format_documents(documents)


def format_documents(documents: list[Document]) -> str:
    documents_string = "-------------------\n"
    headers = ["Column name", "type", "mode"]
    for document in documents:
        documents_string += f"Table name: {document.name}\n\n"
        documents_string += "Schema:\n"
        schema = json.loads(document.schema.replace("'", '"'))
        data = []
        for column in schema:
            data.append([column["name"], column["type"], column["mode"]])
        table = columnar(data, headers, no_borders=True)
        documents_string += table
        documents_string += "-------------------\n"
    return documents_string
