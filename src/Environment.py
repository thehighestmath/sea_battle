import os
import sys


class Root:
    @staticmethod
    def path():
        return os.path.join(os.path.dirname(__file__), "..")


class Resources:
    @staticmethod
    def path(relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(Root.path(), relative_path)

if __file__ == "__main__":
    pass
