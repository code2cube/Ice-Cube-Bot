import discord
import aiosqlite
from discord.ext import commands
from discord import app_commands

class user_add(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('User add is ready.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            g = message.guild.id
            table_name = f"_{g}"
            async with aiosqlite.connect("data/users.db") as db:
                async with db.cursor() as c:
                    await c.execute("CREATE TABLE IF NOT EXISTS {} (username text, id integer, attack integer, defence_min integer, defence_max integer, balance integer, wins integer, losses integer)".format(table_name,))
                    await db.commit()
                    await c.execute("SELECT * FROM {} WHERE id = {}".format(table_name, message.author.id,))
                    check = await c.fetchall()
                    result = ''.join(f"{row[0]}" for row in check)
                    if result == "":
                        await c.execute("INSERT INTO {} (username, id, attack, defence_min, defence_max, balance, wins, losses) VALUES (?, ?, ?, ?, ?, ?, ?, ?)".format(table_name), (f"{message.author.name}#{message.author.discriminator}", message.author.id, 40, 50, 50, 0, 0, 0,))
                        return await db.commit()
                    if result != "":
                        return
        await self.client.process_commands(message)

    @app_commands.command(name="profile", description="View the user's profile for this server")
    @app_commands.describe(member="The profile you want to see")
    async def profile(self, interaction: discord.Interaction, member: discord.Member):
        g = interaction.guild.id
        table_name = f"_{g}"

        async with aiosqlite.connect("data/users.db") as db:
            async with db.cursor() as c:
                await c.execute("SELECT * FROM {} WHERE id = {}".format(table_name, member.id,))
                check = await c.fetchall()
                result = ''.join(f"{row[0]}" for row in check)
                if result == "":
                    embed = discord.Embed(title="User not found in database!", colour=0x6AA6BF)
                    return await interaction.response.send_message(embed=embed, ephemeral=True)
                if result != "":
                    attack = ''.join(f"{row[2]}" for row in check)
                    defence_min = ''.join(f"{row[3]}" for row in check)
                    defence_max = ''.join(f"{row[4]}" for row in check)
                    balance = ''.join(f"{row[5]}" for row in check)
                    wins = ''.join(f"{row[6]}" for row in check)
                    losses = ''.join(f"{row[7]}" for row in check)
                    embed = discord.Embed(title=f"{member.name}#{member.discriminator}", colour=0x6AA6BF)
                    embed.add_field(name="Attack", value=attack, inline=False)
                    embed.add_field(name="Defence", value=f"{defence_min}/{defence_max}", inline=False)
                    embed.add_field(name="Balance", value=f"{balance} coins", inline=False)
                    embed.add_field(name="Wins", value=wins, inline=False)
                    embed.add_field(name="Losses", value=losses, inline=False)
                    embed.set_thumbnail(url=member.display_avatar.url)
                    await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(user_add(client))