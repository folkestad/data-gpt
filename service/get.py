from rich import print

from agents import bigquery_agents
from memory import chromadb_memory
from llm import guidance_pipelines, models
from service.context import Context


def answer(question: str, env: Context) -> str:
    openai_api_key = env.OPENAI_API_KEY
    openai_llm_model = env.OPENAI_LLM_MODEL
    openai_embedding_model = env.OPENAI_EMBEDDING_MODEL
    chromadb_collection = env.CHROMADB_COLLECTION
    chromadb_n_results = env.CHROMADB_N_RESULTS
    gcp_project_id = env.GCP_PROJECT_ID
    gcp_dataset_id = env.GCP_DATASET_ID
    debug = env.DEBUG
    dry_run = env.DRY_RUN

    model, embedding_function = models.openai_llm_model(
        openai_api_key, openai_llm_model, openai_embedding_model
    )

    _, chroma_collection = chromadb_memory.client_and_collection(
        embedding_function, chromadb_collection
    )

    bigquery_client = bigquery_agents.client(gcp_project_id)
    schemas = bigquery_agents.schemas(bigquery_client, gcp_project_id, gcp_dataset_id)
    if debug:
        print(f"{schemas=}")

    chromadb_memory.add(chroma_collection, schemas)

    # Find relevant tables to the question
    most_relevant_tables = chromadb_memory.query(
        chroma_collection, question, n_results=chromadb_n_results
    )
    if debug:
        print(f"{most_relevant_tables=}")

    # Generate SQL
    session1 = guidance_pipelines.generate_sql(
        llm=model,
        question=question,
        most_relevant_table=most_relevant_tables,
        silent=True,
    )
    generated_sql: str = session1["sql"]
    if debug:
        print(f"{generated_sql=}")

    if not generated_sql.startswith("SELECT"):
        return generated_sql

    # Query BigQuery
    query_answer = bigquery_agents.query(
        bigquery_client, generated_sql, dry_run=dry_run
    )
    if debug:
        print(f"{query_answer=}")

    if dry_run:
        return generated_sql

    # Format answer
    session2 = guidance_pipelines.format_answer(
        llm=model, question=question, sql=generated_sql, answer=query_answer
    )
    answer = session2["answer"]
    if debug:
        print(f"{answer=}")

    return answer
