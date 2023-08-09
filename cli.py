import os

from dotenv import load_dotenv
import click

from llm.models import Models
from service.context import Context
from service import translate, store, execute, format
from service.util import is_true

load_dotenv()


@click.command()
@click.option(
    "--question",
    "-q",
    "question",
    default=None,
    help="".join(
        [
            "The question to ask of your data. \n",
            "Example: 'what is the largest country ",
            "by population and what is its total vaccinations?'",
        ]
    ),
)
@click.option(
    "--search",
    "-s",
    "search",
    default=None,
    help="".join(
        [
            "Search for tables containing the data that you are looking for. ",
            "Example: 'country population'",
        ]
    ),
)
@click.option("--project", "-p", "project", default=None, help="GCP project id")
@click.option("--dataset", "-d", "dataset", default=None, help="GCP dataset id")
@click.option(
    "--debug", "debug", default=None, help="Print debug information", is_flag=True
)
@click.option(
    "--dry-run",
    "dry_run",
    default=None,
    help="Dry run does not execute SQL after generation",
    is_flag=True,
)
@click.option(
    "--re-index",
    "re_index",
    default=None,
    help="Re-index the database. Must be added to the first command",
    is_flag=True,
)
def cli(question, search, project, dataset, debug, dry_run, re_index):
    ctx = Context(
        MODEL_TYPE=os.getenv("MODEL_TYPE", Models.NONE),
        MODEL_TYPE_API_KEY=os.getenv("MODEL_TYPE_API_KEY", Models.NONE),
        MODEL_TYPE_LLM_MODEL=os.getenv("MODEL_TYPE_LLM_MODEL", Models.NONE),
        MODEL_TYPE_EMBEDDING_MODEL=os.getenv("MODEL_TYPE_EMBEDDING_MODEL", Models.NONE),
        CHROMADB_COLLECTION=os.getenv("CHROMADB_COLLECTION"),
        CHROMADB_N_RESULTS=int(os.getenv("CHROMADB_N_RESULTS")),
        GCP_PROJECT_ID=project if project is not None else os.getenv("GCP_PROJECT_ID"),
        GCP_DATASET_ID=dataset if dataset is not None else os.getenv("GCP_DATASET_ID"),
        DEBUG=debug if debug is not None else is_true(os.getenv("DEBUG", "False")),
        DRY_RUN=dry_run
        if dry_run is not None
        else is_true(os.getenv("DRY_RUN", "False")),
    )

    if ctx.DEBUG:
        print(ctx)

    if re_index:
        store.index(ctx)
    elif question and not search:
        sql = translate.text_to_sql(ctx, question)
        answer = execute.sql_in_bigquery(ctx, sql)
        formatted_answer = format.answer_as_text(ctx, question, sql, answer)
        click.echo(formatted_answer)
    elif search and not question:
        documents = execute.search_in_store(ctx, question)
        formatted_documents = format.documents_as_text(ctx, documents)
        click.echo(formatted_documents)
    else:
        click.echo("Please provide a question or search term")


if __name__ == "__main__":
    cli()
