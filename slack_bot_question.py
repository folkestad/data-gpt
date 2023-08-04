import os
import re
from typing import Callable

# Use the package we installed
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import logging

from service.context import Context
from service import get, update
from service.util import is_true

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
        MODEL_TYPE=os.getenv("MODEL_TYPE"),
        MODEL_TYPE_API_KEY=os.getenv("MODEL_TYPE_API_KEY"),
        MODEL_TYPE_LLM_MODEL=os.getenv("MODEL_TYPE_LLM_MODEL"),
        MODEL_TYPE_EMBEDDING_MODEL=os.getenv("MODEL_TYPE_EMBEDDING_MODEL"),
        CHROMADB_COLLECTION=os.getenv("CHROMADB_COLLECTION"),
        CHROMADB_N_RESULTS=int(os.getenv("CHROMADB_N_RESULTS")),
        GCP_PROJECT_ID=os.getenv("GCP_PROJECT_ID"),
        GCP_DATASET_ID=os.getenv("GCP_DATASET_ID"),
        DEBUG=is_true(os.getenv("DEBUG", "False")),
        DRY_RUN=is_true(os.getenv("DRY_RUN", "False")),
    )

    update.index(ctx)
    response = get.question(ctx, question)

    say(response)


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
