import json

from llm import models, queries
from service.context import Context
from service.document import Document
from columnar import columnar

from service.util import encode_url


def answer_as_text(
    ctx: Context, question_text: str, generated_sql: str, query_answer: str
) -> str:
    model = models.llm_model(
        ctx.MODEL_TYPE, ctx.MODEL_TYPE_LLM_MODEL, ctx.MODEL_TYPE_API_KEY
    )

    session = queries.format_answer(
        llm=model,
        question=question_text,
        sql=generated_sql,
        answer=query_answer,
        silent=not ctx.DEBUG,
    )
    answer = session["answer"]
    if ctx.DEBUG:
        print(f"{question_text=}")

    return answer


def answer_as_visualization(ctx: Context, answer: str) -> str:
    model = models.llm_model(
        ctx.MODEL_TYPE, ctx.MODEL_TYPE_LLM_MODEL, ctx.MODEL_TYPE_API_KEY
    )

    # Visualize answer
    session = queries.generate_pie_chart_img_link(
        llm=model,
        data=answer,
        silent=not ctx.DEBUG,
    )
    img_link = session["img_link"]
    if ctx.DEBUG:
        print(f"{img_link=}")

    encoded_url = encode_url(img_link)

    return encoded_url


def documents_as_text(ctx: Context, documents: list[Document]) -> str:
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
