import discord
from discord.ext import commands
from discord import app_commands

class help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Help is ready.')

    @app_commands.command(name="help", description="Gain information about the different bot functions!")
    @app_commands.describe(category="The information you want")
    @app_commands.choices(category=[
        app_commands.Choice(name="Moderation", value=1),
        app_commands.Choice(name="Game", value=2),
    ])
    async def help(self, interaction: discord.Interaction, category: app_commands.Choice[int]):
        if category.value == 1:
            embed = discord.Embed(title="Moderation", colour=0x6AA6BF)
            embed.add_field(name="/warn", value="Warn a member for an offence, **requires you to set permission**", inline=False)
            embed.add_field(name="/unwarn", value="Lower a member's warning count, **requires you to set permission** ", inline=False)
            embed.add_field(name="/kick", value="Kick a member from the server, **requires kick_members permission**", inline=False)
            embed.add_field(name="/ban", value="Ban a member from the server, **requires ban_members permission**", inline=False)
            embed.add_field(name="/purge", value="Clear chat messages, **requires administrator permission**", inline=False)
            embed.add_field(name="/freeze", value="Mute a member, **requires you to set permission and for bot to have a higher role than user your trying to mute**", inline=False)
            embed.add_field(name="/melt", value="Unmute a member, **requires you to set permission and for bot to have a higher role than user your trying to unmute**", inline=False)
            embed.set_footer(text="If permission requires you to set, do this in discord server intergrations page!")
            return await interaction.response.send_message(embed=embed)
        if category.value == 2:
            embed = discord.Embed(title="Game", description="So you might be wondering how to play this game? Well its quite simple actually. Start off by typing a message in chat. Then do /profile {your_username} to check if your in database! When you send a message in chat there is a 1 in 10 chance that a monster will spawn. These monsters have different difficulties. You can attack monsters but be careful! If the monster's defence is heigher than your attack you will die! The only way to come back from the dead is purchasing a revive or being revived by a admin! For duels when your defence hits 0 you lose the duel and 1/6 of your coins. Attacking monsters gets you coins which you use to buy items in shop!", colour=0x6AA6BF)
            embed.add_field(name="/revive", value="Allows staff to bring players back from the dead without revive, **requires you to set permission**", inline=False)
            embed.add_field(name="/kill_monster", value="Kills the currently spawned monster but won't grant you any coins!", inline=False)
            embed.add_field(name="/attack_monster", value="Attacks the currently spawned monster using your attack stat!", inline=False)
            embed.add_field(name="/profile", value="View your stats, type a message in chat after bot joins server to be added to database!", inline=False)
            embed.add_field(name="/inventory", value="View your items, type a message in chat after bot joins server to be added to database!", inline=False)
            embed.add_field(name="/use_item", value="Use your items", inline=False)
            embed.add_field(name="/battle", value="First make sure both players have typed a message in chat to be added in database. If you can find both members with /profile then things will work (in theory). Then use this command and type opponent name. The opponent can either accept or deny the challange based on their reactions to the emojis. The first player to attack will be randomly determined. Winning will result in 1/6 of your opponent's coins!", inline=False)
            embed.add_field(name="/attack", value="Attack your opponent in a duel!", inline=False)
            embed.add_field(name="/store", value="Buy items!", inline=False)
            return await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(help(client))