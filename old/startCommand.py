from gameWrapper import GameWrapper
from discord import Embed
import interactions

# from discord_slash.utils.manage_components import create_button, create_actionrow
# from discord_slash.model import ButtonStyle

BOT_PREFIX = '$'

def includeStartCommand(bot, werewolfServers, maskGenerator, roleGenerator):
    @bot.command()
    async def start(ctx):
        guild = ctx.message.guild
        werewolfServer = werewolfServers[str(guild.id)]

        if ctx.message.channel.id != werewolfServer.hosting.id:
            await ctx.message.channel.send(f'This is the wrong channel! Please use this command to start the game at {werewolfServer.hosting.mention}.')
            return

        numPlayers = len(werewolfServer.getWaiting())
        masks = maskGenerator.generate(numPlayers)
        roles = roleGenerator.generate(numPlayers)
        game = GameWrapper(bot, werewolfServer, roles, masks)
        await game.createChannels()
        werewolfServer.addGame(game)
        print()

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        #aka a command hasn't been run
        if str(message.guild.id) in werewolfServers:
            werewolfServer = werewolfServers[str(message.guild.id)]
            await werewolfServer.sendMessage(message)
        await bot.process_commands(message)

    @bot.command()
    async def test(ctx):
        buttons = [
                    create_button(
                        style=ButtonStyle.green,
                        label="A Green Button"
                    ),
                ]

        action_row = create_actionrow(*buttons)

        embed = Embed(title="Cast your vote!", description="Select the person who you would like to vote!", color=0xFF5733)
        await ctx.send(embed=embed, components=[action_row])