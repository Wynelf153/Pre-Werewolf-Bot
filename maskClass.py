import random
import os

#TODO: Add a cache
class Masks:
    def __init__(self):
        self.BASE_PATH = "C:\\Users\\Godwy\\Documents\\coding\\discord-bot\\static"
        self.cache = {}
        return

    def generate(self, numPlayers):
        optionsPath = os.path.join(self.BASE_PATH, f'{numPlayers}p')
        folders = os.listdir(optionsPath)
        chosenFolder = random.choice(folders)

        chosenPath = os.path.join(optionsPath, chosenFolder)
        return self._getFolder(chosenPath)
        
    def _getFolder(self, path):
        folder = os.listdir(path)
        files = [(self.prune(fileName), os.path.join(path, fileName)) for fileName in folder]
        return [{'fakeName':name, 'img':self._getMedia(path)} for (name, path) in files]

    def _getMedia(self, path):
        if path in self.cache:
            return self.cache[path]
        ret = open(path, "rb").read()
        self.cache[path] = ret
        return ret

    def prune(self, imgName):
        dotIndex = imgName.find('.')
        return imgName[:dotIndex]