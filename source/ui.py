# ui.py

from abc import ABC, abstractmethod
from inputs import UserInput
from export import ExportManager

# UI manager


# UI interface - abstract class
class BasicUI(ABC):
    @abstractmethod
    def setup(self, UserInput):
        pass

    @abstractmethod
    def show(self):
        pass


# Terminal UI implementation
class TerminalUI(BasicUI):
    def hello(self):
        print("UI show")
        folder = input("Input folder address: ")
        print("UI closing")
        print("--------")
        return folder

# TKinter UI implementation

