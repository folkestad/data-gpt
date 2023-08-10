import json
import logging
import os
from typing import Callable

from dotenv import load_dotenv

# Use the package we installed
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from service import translate, store, format, execute
from service.context import Context
from service.util import is_true, remove_slack_mentions

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
)


@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    return next()


@app.event("app_mention")
def handle_mentions(body: dict, say: Callable, logger):
    text = body["event"]["text"]
    question = remove_slack_mentions(text)

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

    store.index(ctx)
    sql = translate.text_to_sql(ctx, question)
    answer = execute.sql_in_bigquery(ctx, sql)

    answer_with_explanation = format.answer_as_text(ctx, question, sql, answer)
    say(answer_with_explanation, mrkdwn=True)

    visualization_url = format.answer_as_visualization(ctx, answer)
    visualization_url_bar_chart = visualization_url.replace("type:'pie'", "type:'bar'")
    say("*VISUALIZATION*", mrkdwn=True)
    say(f"<{visualization_url}|Pie Chart>", mrkdwn=True)
    say(f"<{visualization_url_bar_chart}|Bar Chart>", mrkdwn=True)


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
