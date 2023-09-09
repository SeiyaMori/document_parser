# ui.py

import tkinter as tk
from abc import ABC, abstractmethod
from inputs import UserInput
from document import DocumentType
from exceptions import *


# UI manager
class UIManager:
    def __init__(self, user_input: UserInput):
        try:
            self.ui = TkinterUI(user_input)
        except Exception as e:
            # Log error
            msg = "An unexpected error occurred when instantiating the UI \
                manager."
            raise UIError(msg)

    def show_ui(self):
        try:
            self.ui.show()
        except Exception as e:
            # Log error
            msg = "An unexpected error occurred when attempting to show the \
                UI."
            raise UIError(msg)
    
    def close_ui(self):
        try:
            self.ui.close()
        except Exception as e:
            # Log error
            msg = "An unexpected error occurred when attempting to close the \
                UI."
            raise UIError(msg)


# UI interface - abstract class
class BasicUI(ABC):
    def __init__(self, user_input: UserInput):
        self.user_input = user_input

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def close(self):
        pass


# Terminal UI implementation
class TerminalUI(BasicUI):
    def show(self):
        print("UI show")
        self.user_input.folder_path = input("Input folder address: ")
        self.user_input.allowed_doc_types = [DocumentType.PDF]
        print("--------")

    def close(self):
        print("UI closing")
        print("UI closed")


# Tkinter UI implementation
class TkinterUI(BasicUI):
    def show(self):
        print("Showing Tkinter UI")
        root = tk.Tk()
        root.mainloop()

    def close(self):
        pass
