# document.py

from dataclasses import dataclass
from enum import Enum, auto


class DocumentType(Enum):
    PDF = auto()
    DOC = auto()
    DOCX = auto()
    PNG = auto()
    JPG = auto()


class Document:
    def __init__(self, file_path: str, doc_type: DocumentType):
        self.file_path = file_path
        self.doc_type = doc_type
        self.raw_string = None
