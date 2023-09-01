class Channel:
    def __init__(self, channelObj):
        self.obj = channelObj
        self._webhook2Player = {}
        self._player2Webhook = {}

    def webhook2Player(self, webhook):
        return self._webhook2Player[webhook.id]
    
    def player2Webhook(self, player):
        return self._player2Webhook[player.id]
    
    def addWebhook(self, webhook, player):
        self._webhook2Player[webhook.id] = player
        self._player2Webhook[player.id] = webhook

    async def send(self, player, message):
        webhook = self._player2Webhook[player]
        await webhook.send(message)