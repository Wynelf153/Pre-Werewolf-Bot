import discord
from discord.ext import commands
import os

import interactions

from setupCommand import includeSetupCommand
from startCommand import includeStartCommand
from maskClass import Masks
from roleClass import Roles

BOT_PREFIX = '$'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=BOT_PREFIX, intents = intents)

BASE_PATH = "C:\\Users\\Godwy\\Documents\\coding\\discord-bot"

def getToken():
    FILE_PATH = os.path.join(BASE_PATH, 'token.txt')
    file = open(FILE_PATH, "r").read()
    return file

werewolfClasses = {}
maskGenerator = Masks()
roleGenerator = Roles()

includeSetupCommand(bot, werewolfClasses)
includeStartCommand(bot, werewolfClasses, maskGenerator, roleGenerator)

token = getToken()
bot.run(token)
