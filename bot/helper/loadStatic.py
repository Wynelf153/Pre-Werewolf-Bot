import os, random
from files import FileManager

#TODO: Populate static
        # Roles counter
        # Images/Names counter
class StaticManager:
    def __init__(self, BASE_PATH):
        self.BASE_PATH      = BASE_PATH
        self.fileManager    = FileManager(BASE_PATH)
        self._roleSetups    = self.fileManager.readJson("static/gameSetups")
        self._avatarSetups  = self._loadAvatars("static/avatarSetups")
    
    def generateRole(self, numPlayers):
        setups = self._roleSetups[numPlayers]
        return random.choice(setups)
    
    def generateAvatars(self, numPlayers):
        setups = self._avatarSetups[numPlayers]
        return random.choice(setups)

    def _loadAvatars(self, relPath):
        avatarPath = os.path.join(self.BASE_PATH, relPath)
        playerCounts = self.fileManager.listDir(avatarPath)
        ret = {}
        for playerCount in playerCounts:
            countPath = os.path.join(avatarPath, playerCount)
            ret[playerCount] = self.fileManager.readImgs(countPath)
        return ret



