import os

from dotenv import load_dotenv
import click

from service.context import Context
from service.get import answer

load_dotenv()


@click.command()
@click.option(
    "--question",
    "-q",
    "question",
    help="".join(
        [
            "The question to ask about your data. ",
            "Example: 'what is the largest country ",
            "by population and what is its total vaccinations?'",
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
def cli(question, project, dataset, debug, dry_run):
    ctx = Context(
        OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
        OPENAI_LLM_MODEL=os.getenv("OPENAI_LLM_MODEL"),
        OPENAI_EMBEDDING_MODEL=os.getenv("OPENAI_EMBEDDING_MODEL"),
        CHROMADB_COLLECTION=os.getenv("CHROMADB_COLLECTION"),
        CHROMADB_N_RESULTS=int(os.getenv("CHROMADB_N_RESULTS")),
        GCP_PROJECT_ID=project if project is not None else os.getenv("GCP_PROJECT_ID"),
        GCP_DATASET_ID=dataset if dataset is not None else os.getenv("GCP_DATASET_ID"),
        DEBUG=debug if debug is not None else os.getenv("DEBUG"),
        DRY_RUN=dry_run if dry_run is not None else os.getenv("DRY_RUN"),
    )

    response = answer(question, ctx)
    click.echo(response)


if __name__ == "__main__":
    cli()
