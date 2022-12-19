import discord
import os
import aiosqlite
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
#https://discord.com/api/oauth2/authorize?client_id=1049077398655742063&permissions=3555978334&scope=bot%20applications.commands
#https://docs.google.com/spreadsheets/d/1FEL9FeW2PGRX21xia0CyTV4652Wijizq3-KW2PXqyiI/edit#gid=0
load_dotenv()

intents = discord.Intents().all()

client = commands.Bot(command_prefix="ice!", help_command=None, intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    try:
        await client.load_extension("cogs.snowball")
        await client.load_extension("cogs.moderation")
        await client.load_extension("cogs.user_add")
        await client.load_extension("cogs.monsters")
        await client.load_extension("cogs.battle")
        await client.load_extension("cogs.store")
        await client.load_extension("cogs.help")
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

client.run(os.getenv("TOKEN"))