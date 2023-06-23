import os
import re
from typing import Callable

# Use the package we installed
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import logging

from service.context import Context
from service.get import answer

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
)


@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    return next()


def remove_mentions(text: str) -> str:
    return re.sub("<@.*>", "", text)


@app.event("app_mention")
def handle_mentions(body: dict, say: Callable, logger):
    text = body["event"]["text"]
    question = remove_mentions(text)

    ctx = Context(
        OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
        OPENAI_LLM_MODEL=os.getenv("OPENAI_LLM_MODEL"),
        OPENAI_EMBEDDING_MODEL=os.getenv("OPENAI_EMBEDDING_MODEL"),
        CHROMADB_COLLECTION=os.getenv("CHROMADB_COLLECTION"),
        CHROMADB_N_RESULTS=int(os.getenv("CHROMADB_N_RESULTS")),
        GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID"),
        GCP_DATASET_ID=os.getenv("GCP_DATASET_ID"),
        DEBUG=bool(os.getenv("DEBUG")),
        DRY_RUN=bool(os.getenv("DRY_RUN")),
    )

    response = answer(question, ctx)

    say(response)


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
