import dataclasses


@dataclasses.dataclass(frozen=True)
class Document:
    name: str
    schema: str
