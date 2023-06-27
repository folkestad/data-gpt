import dataclasses


@dataclasses.dataclass(frozen=True)
class Context:
    MODEL_TYPE: str
    MODEL_TYPE_API_KEY: str
    MODEL_TYPE_LLM_MODEL: str
    MODEL_TYPE_EMBEDDING_MODEL: str
    CHROMADB_COLLECTION: str
    CHROMADB_N_RESULTS: int
    GCP_PROJECT_ID: str
    GCP_DATASET_ID: str
    DEBUG: bool
    DRY_RUN: bool
