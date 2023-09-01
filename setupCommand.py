import helper.metadata as metadata
import time
from server import WerewolfServer
from gameWrapper import GameWrapper

BOT_PREFIX = '$'

data = metadata.getGuildMetadata()

def channelsMatch(bot, guild, channelIds):
    category  = bot.get_channel(channelIds['categoryId'])
    hosting   = bot.get_channel(channelIds['hostId'])
    signup    = bot.get_channel(channelIds['signupId'])
    return category != None and hosting != None and signup != None

def classMatch(werewolfServer, channelIds):
    if werewolfServer == None:
        return False
    return (werewolfServer.category.id == channelIds['categoryId'] and
            werewolfServer.hosting.id == channelIds['hostId'] and 
            werewolfServer.signup.id == channelIds['signupId'])

def notSetup(werewolfServers, guildId):
    return str(guildId) not in werewolfServers or werewolfServers[str(guildId)] == None

def includeSetupCommand(bot, werewolfServers):
    @bot.command()
    async def setup(ctx):
        workstation = WerewolfServer(bot, ctx.message.guild.id)
        ids = await workstation.setup(ctx)
        if ids:
            data[str(ctx.message.guild.id)] = ids
        metadata.saveGuildMetadata(data)
        werewolfServers[ctx.message.guild.id] = workstation

    @bot.before_invoke
    async def common(ctx):
        if ctx.message.content.startswith("$setup"):
            return
        guild = ctx.message.guild
        if str(guild.id) not in data:
            await ctx.message.channel.send(f'Please run {BOT_PREFIX}setup first!')
            werewolfServers[str(guild.id)] = None
            return
        elif not channelsMatch(bot, guild, data[str(guild.id)]):
            await ctx.message.channel.send(f'Some channels are missing. Please delete the category werewolf-corner and run {BOT_PREFIX}setup.')
            werewolfServers[str(guild.id)] = None
            return
        
        werewolfServer = werewolfServers.get(str(guild.id), None)
        if not classMatch(werewolfServer, data[str(guild.id)]):
            werewolfServers[str(guild.id)] = WerewolfServer(bot, guild.id, channelIds= data[str(guild.id)])
            return
    
    @bot.command()
    async def register(ctx):
        guild = ctx.message.guild
        author = ctx.message.author

        if notSetup(werewolfServers, guild.id):
            return

        #werewolfClass represents the werewolfClass object corresponding to current guild.
        werewolfServer = werewolfServers[str(guild.id)]

        if ctx.message.channel.id != werewolfServer.signup.id:
            await ctx.message.channel.send(f'This is the wrong channel! Please register at {werewolfServer.signup.mention}.')
            return

        if werewolfServer.inWaiting(author):
            werewolfServer.addWaiting(author, ctx.message.created_at)
            await ctx.message.channel.send(f'Updated register time! Currently waiting: {werewolfServer.waitingPrint()}')
        else:
            werewolfServer.addWaiting(author, ctx.message.created_at)
            await ctx.message.channel.send(f'Registered! Currently waiting: {werewolfServer.waitingPrint()}')

    @bot.command()
    async def unregister(ctx):
        guild = ctx.message.guild
        author = ctx.message.author

        if notSetup(werewolfServers, guild.id):
            return
        
        #werewolfClass represents the werewolfClass object corresponding to current guild.
        werewolfServer = werewolfServers[str(guild.id)]
        succ = werewolfServer.popWaiting(author)
        if succ:
            await ctx.message.channel.send(f'Unregistered! Currently waiting: {werewolfServer.waitingPrint()}')
        else:
            await ctx.message.channel.send(f"You weren't registered in the first place!")
