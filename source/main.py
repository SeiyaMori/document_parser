# main.py

from ui import UIManager
from importer import ImportManager
from inputs import UserInput
from exceptions import *


if __name__ == "__main__":

    # User input
    user_input = UserInput()

    # UI show
    ui_manager = UIManager(user_input)
    ui_manager.show_ui()

    # Import documents
    import_manager = ImportManager(user_input)
    documents = import_manager.import_docs()

    # Parse each document
    for doc in documents:
        print(doc)

    # Export results

    # UI close
    ui_manager.close_ui()
