from json.decoder import JSONDecodeError
import os
import sys
import json

DEBUG = False


class Root:
    @staticmethod
    def path():
        if hasattr(sys, "_MEIPASS"):
            return os.path.dirname(__file__)
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
    __fileName = "scoreboard"

    @staticmethod
    def setFileName(name):
        ScoreBoard.__fileName = name

    @staticmethod
    def read():
        rootPath = Root.path()
        filePath = os.path.join(rootPath, f"{ScoreBoard.__fileName}.json")
        try:
            with open(filePath) as fp:
                try:
                    sb = json.load(fp)
                except JSONDecodeError:
                    sb = {'PVP': [], 'PVE': []}
        except FileNotFoundError:
            sb = {'PVP': [], 'PVE': []}

        return sb

        # file = open(os.path.join(rootPath, "ScoreBoard.txt"), "w+")
        # try:
        #     scoreBoard = ast.literal_eval(file.read())
        # except Exception:
        #     scoreBoard = {}
        # file.close()
        # return scoreBoard

    @staticmethod
    def write(scoreBoard):
        rootPath = Root.path()
        filePath = os.path.join(rootPath, f"{ScoreBoard.__fileName}.json")

        with open(filePath, "w") as fp:
            json.dump(scoreBoard, fp, indent=2)

        # file = open(os.path.join(rootPath, "ScoreBoard.txt"), "r")
        # file.write("%s" % scoreBoard)
        # file.close()
    
    @staticmethod
    def readLine(mode, name):
        sb = ScoreBoard.read()
        lines = sb[mode]
        for line in lines:
            if line["name"] == name:
                return line["scores"]
        return 0

    @staticmethod
    def writeLine(mode, name, value):
        sb = ScoreBoard.read()
        lines = sb[mode]
        for line in lines:
            if line["name"] == name:
                line["scores"] = value
                ScoreBoard.write(sb)
                return

        lines.append({"name": name, "scores": value})
        ScoreBoard.write(sb)

if __name__ == "__main__":
    pass
    # ScoreBoard.setName("oasdosufsd")
    # print(Root.path())
    # # ResourceDirectory("oioi")
    # print("path: ", Resources.path())
    # ScoreBoard.write({'key1':'1','key2':'2'})
    # print(ScoreBoard.read())
