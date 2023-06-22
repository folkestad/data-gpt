import guidance
from chromadb.utils import embedding_functions


def openai_llm_model(api_key: str, llm_model: str, embedding_model: str):
    openai_model = guidance.llms.OpenAI(llm_model)
    openai_embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        api_key=api_key, model_name=embedding_model
    )
    return openai_model, openai_embedding_function
