import os
import json

BASE_PATH = "C:\\Users\\Godwy\\Documents\\coding\\discord-bot"

def getGuildMetadata():
    FILE_PATH = os.path.join(BASE_PATH, 'guildData.json')
    file = open(FILE_PATH, "r").read()
    return json.loads(file)

def saveGuildMetadata(data):
    FILE_PATH = os.path.join(BASE_PATH, 'guildData.json')
    file = open(FILE_PATH, "w")
    file.write(json.dumps(data))
    return 