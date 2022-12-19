import discord
import requests
from io import BytesIO
from discord import File
from discord.ext import commands
from discord import app_commands
from easy_pil import Editor, load_image_async

class snowball(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Snowball is ready.')

    @app_commands.command(name="snowball", description="Throw a snowball at someone! ⚪")
    @app_commands.describe(member="The person your throwing the snowball at")
    async def snowball(self, interaction: discord.Interaction, member: discord.Member):
        background = Editor("images/background.png")
        _author_image = await load_image_async(interaction.user.display_avatar.url)
        _member_image = await load_image_async(member.display_avatar.url)

        _author_circle = Editor(_author_image).resize((150, 150)).circle_image()
        _member_image = Editor(_member_image).resize((150, 150)).circle_image()
        background.paste(_author_circle, (100, 170))
        background.paste(_member_image, (510, 230))
        file = File(fp=background.image_bytes, filename=f"snowball.png")
        await interaction.response.send_message(file=file)

async def setup(client):
    await client.add_cog(snowball(client))