# inputs.py

from dataclasses import dataclass, field
from document import DocumentType


# UserInput
@dataclass
class UserInput:
    folder_path: str = ""
    allowed_doc_types: list[DocumentType] = field(default_factory=list)
