import os
import json

class FileManager:
    def __init__(self, BASE_PATH):
        self.BASE_PATH = BASE_PATH

    def read(self, relPath):
        FILE_PATH = os.path.join(self.BASE_PATH, relPath)
        file = open(FILE_PATH, "r").read()
        return file

    def write(self, relPath, data):
        FILE_PATH = os.path.join(self.BASE_PATH, relPath)
        file = open(FILE_PATH, "w")
        file.write(data)
        return 
    
    def readJson(self, relPath):
        file = self.read(relPath)
        return json.loads(file)
    
    def writeJson(self, relPath, data):
        data = json.dumps(data)
        self.write(relPath, data)
        return 