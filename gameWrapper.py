import random, datetime
from discord.ext import tasks
from channelClass import Channel
from gameState import GameState

#TODO: Include gameState object and add handling for game end
class GameWrapper:
    def __init__(self, bot, werewolfServer, roles, masks):
        players = [player for player, time in werewolfServer.getWaiting()]

        random.shuffle(masks)
        random.shuffle(roles)

        self._gameState = GameState(players, roles)

        self._serverClass = werewolfServer
        self._channel2Player = {}
        self._player2Channel = {}

        self._players = players
        self._channels = []

        self._webhookData = [{'player':player, **maskDict} for player, maskDict in zip(players, masks)]

        self.dayNum = 0
        self.isDay = True

    #Call resolve
    @tasks.loop(minutes = 1)
    async def update(self):
        day, isDay = self.getTime()
        if isDay != self.isDay:
            if day == self.dayNum:
                lynched = self._gameState.resolveDay()
                self._gameState.resetVotes()
            else:
                self._gameState.resolveNight()
            self._gameState.parityCheck()
            self._gameState.resetActions()

    def getTime(self):
        delta = datetime.datetime.now() - self.startTime
        day = delta//datetime.timedelta(minutes = self._dayMin + self._nightMin)

        left = delta%datetime.timedelta(minutes = self._dayMin + self._nightMin)
        isDay = left > datetime.timedelta(minutes = self._dayMin)
        return day, isDay 

    async def sendMessage(self, message):
        #Add handling for who can receive messages here
        targets, prefix = self.getMessageTargetPrefix(message.author)
        targetChannels = [self._player2Channel(target.obj.id) for target in targets]
        for channelClass in targetChannels:
            webhook = channelClass.player2Webhook(message.author)
            await webhook.send(f'{prefix}{message.content}')
        return

    #Returns list of players to send to
    def getMessageTargetPrefix(self, player):
        playerClass = self._gameState.getPlayerClass(player)
        if self.isDay and playerClass.alive:
            target = self._gameState.getTown()
            prefix = ''
        elif self.isDay and not playerClass.alive:
            target = self._gameState.getGraveyard()
            prefix = '(To the graveyard) '
        elif not self.isDay:
            alignment = self._gameState.getAlignment(player)
            target, prefix = self._gameState.getFactionPrefix(alignment)
        return target, prefix

    def hasChannel(self, queryChannel):
        return queryChannel.id in [channelClass.obj.id for channelClass in self._player2Channel.values()]

    def hasPlayer(self, queryPlayer):
        return queryPlayer.id in [player.id for player in self._channel2Player.values()]
    
    def channel2Player(self, queryChannel):
        return self._channel2Player[queryChannel.id]

    def player2Channel(self, queryPlayer):
        return self._player2Channel[queryPlayer.id]

    async def createChannels(self):
        for player in self._players:
            channelClass = await self._createChannel(player)

            self._channel2Player[channelClass.obj.id] = player
            self._player2Channel[player.id] = channelClass

            self._channels.append(channelClass)

    async def _createChannel(self, channelOwner):
        channelObj = await self._serverClass.guild.create_text_channel(channelOwner.name, category = self._serverClass.category)
        await channelObj.set_permissions(self._serverClass.guild.default_role, read_messages=False)
        await channelObj.set_permissions(channelOwner, read_messages=True)

        channelClass = Channel(channelObj)
        for info in self._webhookData:
            webhook = await channelObj.create_webhook(name = info['fakeName'], avatar = info['img'])
            actualPlayer = info['player']
            channelClass.addWebhook(webhook, actualPlayer)
            await webhook.send(f"Hi, I'm {info['fakeName']}")
        return channelClass

