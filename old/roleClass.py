import random
import os
import json

class Roles:
    def __init__(self):
        self.BASE_PATH = "C:\\Users\\Godwy\\Documents\\coding\\discord-bot\\static\\gameSetup.json"
        self.gameSetups = self._load()
        return

    def generate(self, numPlayers):
        setup = self.gameSetups[numPlayers]
        return random.choice(setup)

    def _load(self):
        file = open(self.BASE_PATH, "r").read()
        ret = json.loads(file)
        return ret