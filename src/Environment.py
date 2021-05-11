import os
import sys
import ast

DEBUG = False


class Root:
    @staticmethod
    def path():
        return os.path.dirname(os.path.dirname(__file__))


class Resources:
    @staticmethod
    def path():
        relativePath = str(ResourceDirectory())
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relativePath)
        return os.path.join(Root.path(), relativePath)


class ResourceDirectory(object):
    def __new__(cls, relative_path=None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ResourceDirectory, cls).__new__(cls)
        if not hasattr(cls, 'relativePath') and relative_path == None:
            cls.relativePath = "res"
        elif relative_path:
            cls.relativePath = relative_path

        return cls.instance

    def __repr__(self):
        return self.relativePath

    def __str__(self):
        return self.relativePath

class ScoreBoard:
    @staticmethod
    def read():
        rootPath = Root.path()
        file = open(os.path.join(rootPath, "ScoreBoard.txt"), "w+")
        try:
            scoreBoard = ast.literal_eval(file.read())
        except Exception:
            scoreBoard = {}
        file.close()
        return scoreBoard

    @staticmethod
    def write(scoreBoard):
        rootPath = Root.path()
        print(os.path.join(rootPath, "ScoreBoard.txt"))
        file = open(os.path.join(rootPath, "ScoreBoard.txt"), "r")
        file.write("%s" % scoreBoard)
        file.close()

if __name__ == "__main__":
    # print(Root.path())
    # # ResourceDirectory("oioi")
    # print("path: ", Resources.path())
    ScoreBoard.write({'key1':'1','key2':'2'})
    print(ScoreBoard.read())