# import.py

from abc import ABC, abstractmethod
from inputs import UserInput
from document import Document, DocumentType
from exceptions import *


# Import manager
class ImportManager:
    def __init__(self, user_input: UserInput):
        try:
            self.user_input = user_input
            self.importer = UniversalImporter()
        except Exception as e:
            # Log error
            msg = "An unexpected error occurred when instantiating the \
                import manager."
            raise ImportError(msg)

    def import_docs(self) -> list[Document]:
        try:
            return self.importer.import_docs(self.user_input.folder_path)
        except Exception as e:
            # Log error
            msg = "An unexpected error occurred when attempting to import \
                the documents."
            raise ImportError(msg)


# Importer interface - abstract class
class BaseImporter(ABC):
    @abstractmethod
    def import_docs(self, folder_path: str) -> list[Document]:
        pass


# Universal importer
class UniversalImporter(BaseImporter):
    def import_docs(self, folder_path: str) -> list[Document]:
        print("Folder path: ", folder_path)
        documents = [
            Document("test", DocumentType.PDF),
            Document("test2", DocumentType.JPG)
        ]
        return documents


# PDF importer

# Word importer

# Image importer
