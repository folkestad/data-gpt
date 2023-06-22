import dataclasses


@dataclasses.dataclass(frozen=True)
class Context:
    OPENAI_API_KEY: str
    OPENAI_LLM_MODEL: str
    OPENAI_EMBEDDING_MODEL: str
    CHROMADB_COLLECTION: str
    CHROMADB_N_RESULTS: int
    GCP_PROJECT_ID: str
    GCP_DATASET_ID: str
    DEBUG: bool
    DRY_RUN: bool
