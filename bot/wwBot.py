import json
import os
import asyncio
import discord
from discord.ext import commands

from bot.helper.loadStatic import StaticManager

class wwBot:
    def __init__(self, BASE_PATH):
        self._static = StaticManager(BASE_PATH)
                
        BOT_PREFIX  = '$'
        self.client = discord.Client()
        self.bot    = commands.Bot(command_prefix=BOT_PREFIX)

        #TODO: Rewrite file structure
        self._servers    = self._static.fileManager.readJson("guildData.json")

        # TODO: Add commands
        # Setup: Creates channels and updates self._servers and guildData.json
        # Help: Returns an embed containing help information
        # 
        # Pass the other commands to corresponding server    

        self._run()

    def _run(self):
        token = self._static.fileManager.read('token.txt')
        self.bot.run(token)
        return
    