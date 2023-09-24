import discord
from discord.ext import commands
import os

import interactions

BOT_PREFIX = '$'

client = discord.Client()
bot = commands.Bot(command_prefix=BOT_PREFIX)

BASE_PATH = "C:\\Users\\Godwy\\Documents\\coding\\discord-bot"

def getToken():
    FILE_PATH = os.path.join(BASE_PATH, 'token.txt')
    file = open(FILE_PATH, "r").read()
    return file

token = getToken()
bot.run(token)
