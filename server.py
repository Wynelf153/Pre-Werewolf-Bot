import os
import json
import helper.metadata as metadata
import datetime

BOT_PREFIX = '$'

class WerewolfServer:
    #ctx is the context when create command is called.
    def __init__(self, bot, guildId, channelIds = None):

        #Basic Info
        self._bot = bot
        self.guild = bot.get_guild(guildId)
        if channelIds != None:
            self.category  = bot.get_channel(channelIds['categoryId'])
            self.hosting   = bot.get_channel(channelIds['hostId'])
            self.signup    = bot.get_channel(channelIds['signupId'])
        else:
            self.category, self.hosting, self.signup = (None, None, None)
        
        self._waiting = []

        self._games = []

        return

    def addGame(self, game):
        self._games.append(game)

    async def sendMessage(self, message):
        for game in self._games:
            if game.hasChannel(message.channel) and game.hasPlayer(message.author) and not game.Ended:
                await message.delete()
                if not message.content.startswith(BOT_PREFIX): 
                    await game.sendMessage(message)
                break
            else:
                continue

    async def setup(self, ctx):
        if self._clashNames():
            await ctx.message.channel.send('There is already another category with the name Werewolf-Corner! If you want to continue, please delete it first.')
            return None
        self.category  = await self.guild.create_category_channel('werewolf-corner')
        self.hosting   = await self.guild.create_text_channel('hosting', category = self.category)
        self.signup    = await self.guild.create_text_channel('signup', category = self.category)

        return {
            'categoryId':   self.category.id,
            'hostId':       self.hosting.id,
            'signupId':     self.signup.id
        }

    def resetWaiting(self):
        self._waiting = []

    def getWaiting(self):
        return self._waiting.copy()

    def inWaiting(self, player):
        return player.id in [waitingPlayer.id for waitingPlayer, time in self._waiting]

    def addWaiting(self, player, time):
        self._waiting = [(waitingPlayer, time) for waitingPlayer, time in self._waiting if waitingPlayer.id != player.id]
        self._waiting.append((player, time))
        return True
    
    def popWaiting(self, player):
        if self.inWaiting(player):
            self._waiting = [(waitingPlayer, time) for waitingPlayer, time in self._waiting if waitingPlayer.id != player.id]
            return True
        else:
            return False

    def waitingPrint(self):
        self._updateWaiting()
        names = [waitingPlayer.name for waitingPlayer, time in self._waiting][::-1]
        return ', '.join(names)

    def _updateWaiting(self):
        def expired(pastDatetime):
            EXPIRE_TIME = 1800 #30 minutes
            return datetime.datetime.now(datetime.timezone.utc) - pastDatetime > datetime.timedelta(seconds = EXPIRE_TIME)
        
        self._waiting = [(waitingPlayer, time) for waitingPlayer, time in self._waiting if not expired(time)]
        return

    def _clashNames(self):
        clash = any([channel for channel in self.guild.channels if channel.type.name == 'category' and channel.name == 'werewolf-corner'])
        return clash

    # @bot.event
    # async def on_message(message):

    #     if message.content.startswith('$hello'):
    #         await message.channel.send('Hello!')

    #     await bot.process_commands(message)