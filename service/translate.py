from rich import print

from llm import queries, models
from llm.models import embedding_model_default
from memory import chromadb_memory
from service.context import Context


def text_to_sql(ctx: Context, question_text: str) -> str:
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
    session1 = queries.generate_sql(
        llm=model,
        question=question_text,
        most_relevant_table=most_relevant_tables,
        silent=not ctx.DEBUG,
    )
    generated_sql: str = session1["sql"]
    if ctx.DEBUG:
        print(f"{generated_sql=}")

    return generated_sql
