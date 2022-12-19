import discord
import aiosqlite
from discord.utils import get
from discord.ext import commands
from discord import app_commands

class moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation is ready.')

    @app_commands.command(name="warn", description="Warn a member")
    @app_commands.describe(member="The member you want to warn")
    @app_commands.describe(reason="The reason for the warning")
    async def warn(self, interaction, member: discord.Member, reason: str):
        get_guild = interaction.guild.id
        guild_for_table = f"_{get_guild}"
        async with aiosqlite.connect("data/warnings.db") as db:
            async with db.cursor() as c:
                await c.execute("CREATE TABLE IF NOT EXISTS {} (username text, id integer, warning_count integer)".format(guild_for_table))
                await db.commit()

                await c.execute("SELECT * FROM {} WHERE id = {}".format(guild_for_table, member.id,))
                check = await c.fetchall()
                output = "".join(f"{row[2]}" for row in check)

                if output == "":
                    await c.execute("INSERT INTO {} (username, id, warning_count) VALUES (?, ?, ?)".format(guild_for_table), (f"{member.name}#{member.discriminator}", member.id, str(1)))
                    await db.commit()
                    embed = discord.Embed(title=f"{member.name}#{member.discriminator} has been warned for the first time!", colour=0x6AA6BF)
                    embed.add_field(name="Reason:", value=reason, inline=False)
                    embed.set_thumbnail(url=member.display_avatar.url)
                    embed.set_footer(text=f"Warned by {interaction.user}")
                    await interaction.response.send_message(embed=embed)
                    #send user message
                    em = discord.Embed(title=f"You have been warned for the first time at {interaction.guild.name}!", colour=0x6AA6BF)
                    em.add_field(name="Reason:", value=reason, inline=False)
                    em.add_field(name="Staff Member:", value=interaction.user, inline=False)
                    if interaction.guild.icon:
                        em.set_thumbnail(url=interaction.guild.icon.url)
                        await member.send(embed=em)
                    else:
                        return await member.send(embed=em)

                if output == "0":
                    await c.execute("UPDATE {} SET warning_count = warning_count + 1 WHERE id = {}".format(guild_for_table, member.id,))
                    await db.commit()
                    embed = discord.Embed(title=f"{member.name}#{member.discriminator} has been warned for the first time!", colour=0x6AA6BF)
                    embed.add_field(name="Reason:", value=reason, inline=False)
                    embed.set_thumbnail(url=member.display_avatar.url)
                    embed.set_footer(text=f"Warned by {interaction.user}")
                    await interaction.response.send_message(embed=embed)
                    #send user message
                    em = discord.Embed(title=f"You have been warned for the first time at {interaction.guild.name}!", colour=0x6AA6BF)
                    em.add_field(name="Reason:", value=reason, inline=False)
                    em.add_field(name="Staff Member:", value=interaction.user, inline=False)
                    if interaction.guild.icon:
                        em.set_thumbnail(url=interaction.guild.icon.url)
                        await member.send(embed=em)
                    else:
                        return await member.send(embed=em)

                if output > "0" and output != "":
                    await c.execute("UPDATE {} SET warning_count = warning_count + 1 WHERE id = {}".format(guild_for_table, member.id,))
                    await db.commit()
                    embed = discord.Embed(title=f"{member.name}#{member.discriminator} has been warned!", colour=0x6AA6BF)
                    embed.add_field(name="Reason:", value=reason, inline=False)
                    embed.add_field(name="Number of Warnings:", value=int(output) + int(1), inline=False)
                    embed.set_thumbnail(url=member.display_avatar.url)
                    embed.set_footer(text=f"Warned by {interaction.user}")
                    await interaction.response.send_message(embed=embed)
                    #send user message
                    em = discord.Embed(title=f"You have been warned at {interaction.guild.name}!", colour=0x6AA6BF)
                    em.add_field(name="Reason:", value=reason, inline=False)
                    em.add_field(name="Staff Member:", value=interaction.user, inline=False)
                    em.add_field(name="Number of Warnings:", value=int(output) + int(1), inline=False)
                    if interaction.guild.icon:
                        em.set_thumbnail(url=interaction.guild.icon.url)
                        return await member.send(embed=em)
                    else:
                        return await member.send(embed=em)

    @app_commands.command(name="unwarn", description="Revoke a warning from a member")
    @app_commands.describe(member="The member you want to unwarn")
    @app_commands.describe(reason="The reason for a warning being removed")
    async def unwarn(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        get_guild = interaction.guild.id
        guild_for_table = f"_{get_guild}"
        async with aiosqlite.connect("data/warnings.db") as db:
            async with db.cursor() as c:
                await c.execute("CREATE TABLE IF NOT EXISTS {} (username text, id integer, warning_count integer)".format(guild_for_table))
                await db.commit()
                await c.execute("SELECT * FROM {} WHERE id = {}".format(guild_for_table, member.id))
                check = await c.fetchall()
                output = ''.join(f"{row[2]}" for row in check)

                if output == "" or output == "0":
                    embed = discord.Embed(title=f"{member.name}#{member.discriminator} has no warnings :|", colour=0x6AA6BF)
                    return await interaction.response.send_message(embed=embed, ephemeral=True)

                else:
                    await c.execute("UPDATE {} SET warning_count = warning_count - {} WHERE id = {}".format(guild_for_table, str(1), member.id))
                    await db.commit()
                    embed = discord.Embed(title=f"{member.name}#{member.discriminator} has lost a warning!", colour=0x6AA6BF)
                    embed.add_field(name="Reason:", value=reason, inline=False)
                    embed.add_field(name="Number of Warnings:", value=int(output) - int(1), inline=False)
                    embed.set_thumbnail(url=member.display_avatar.url)
                    embed.set_footer(text=f"Warn revoked by {interaction.user}")
                    await interaction.response.send_message(embed=embed)
                    #send user message
                    em = discord.Embed(title=f"Your warning has been revoked at {interaction.guild.name}!", colour=0x6AA6BF)
                    em.add_field(name="Reason:", value=reason, inline=False)
                    em.add_field(name="Staff Member:", value=interaction.user, inline=False)
                    em.add_field(name="Number of Warnings:", value=int(output) - int(1), inline=False)
                    if interaction.guild.icon:
                        em.set_thumbnail(url=interaction.guild.icon.url)
                    return await member.send(embed=em)

    @app_commands.command(name="kick", description="Yeet a member from the server")
    @app_commands.describe(member="The member you want to kick")
    @app_commands.describe(reason="The reason for the kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await member.kick()
        embed = discord.Embed(title=f"{member.name}#{member.discriminator} has been kicked!", colour=0x6AA6BF)
        embed.add_field(name="Reason:", value=reason, inline=False)
        embed.set_image(url=member.display_avatar.url)
        embed.set_footer(text=f"Kicked by {interaction.user}")
        await interaction.response.send_message(embed=embed)
        #send user message
        em = discord.Embed(title=f"You have been kicked from {interaction.guild.name}!", colour=0x6AA6BF)
        em.add_field(name="Reason:", value=reason, inline=False)
        em.add_field(name="Staff Member:", value=interaction.user, inline=False)
        if interaction.guild.icon:
            em.set_thumbnail(url=interaction.guild.icon.url)
        await member.send(embed=em)

    @app_commands.command(name="ban", description="Use the ban hammer")
    @app_commands.describe(member="The member you want to ban")
    @app_commands.describe(reason="The reason for the kick")
    @commands.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        await member.ban()
        embed = discord.Embed(title=f"{member.name}#{member.discriminator} has been banned!", colour=0x6AA6BF)
        embed.add_field(name="Reason:", value=reason, inline=False)
        embed.set_image(url=member.display_avatar.url)
        embed.set_footer(text=f"Banned by {interaction.user}")
        await interaction.response.send_message(embed=embed)
        #send user message
        em = discord.Embed(title=f"You have been banned from {interaction.guild.name}!", colour=0x6AA6BF)
        em.add_field(name="Reason:", value=reason, inline=False)
        em.add_field(name="Staff Member:", value=interaction.user, inline=False)
        if interaction.guild.icon:
            em.set_thumbnail(url=interaction.guild.icon.url)
        await member.send(embed=em)

    @app_commands.command(name="purge", description="Clear messages")
    @app_commands.describe(amount="The amount of messages you want deleted")
    @app_commands.describe(channel="If you want messages deleted from a specific channel")
    @app_commands.describe(user="If you want messages deleted from a specific user")
    @commands.has_permissions(administrator=True)
    async def purge(self, interaction: discord.Interaction, amount: int, channel: discord.TextChannel = None, user: discord.Member = None):
        if channel is None and user is None:
            embed = discord.Embed(title=f"{amount} messages have been cleared from {interaction.channel.name}", colour=0x6AA6BF)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return await interaction.channel.purge(limit=amount)

        if channel != None and user is None:
            embed = discord.Embed(title=f"{amount} messages have been cleared from {channel.name}", colour=0x6AA6BF)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return await channel.purge(limit=amount)

        if channel is None and user != None:
            async for message in interaction.channel.history(limit=amount):
                if message.author.id == user.id:
                    embed = discord.Embed(title=f"{amount} of {message.author.name}#{message.author.discriminator}'s messages have been cleared from {interaction.channel.name}", colour=0x6AA6BF)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return await interaction.channel.purge(limit=amount)

        if channel != None and user != None:
            async for message in interaction.channel.history(limit=amount):
                if message.author.id == user.id:
                    embed = discord.Embed(title=f"{amount} {message.author.name}#{message.author.discriminator}'s messages have been cleared from {channel.name}", colour=0x6AA6BF)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return await channel.purge(limit=amount)

    @app_commands.command(name="freeze", description="Mute a member")
    @app_commands.describe(member="The member you want to mute")
    @app_commands.describe(reason="The reason for the mute")
    async def freeze(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        guild = interaction.guild
        muterole  = discord.utils.get(guild.roles, name="Frozen🥶")
        if muterole in member.roles:
            embed = discord.Embed(title=f"{member.name}#{member.discriminator} is already muted :|", colour=0x6AA6BF)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            if muterole:
                await member.add_roles(muterole)
                embed = discord.Embed(title=f"{member.name}#{member.discriminator}'s mouth is now frozen shut!", colour=0x6AA6BF)
                embed.add_field(name="Reason:", value=reason, inline=False)
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.set_footer(text=f"Frozen by {interaction.user}")
                await interaction.response.send_message(embed=embed)
                #send user message
                em = discord.Embed(title=f"You have been muted at {interaction.guild.name}!", colour=0x6AA6BF)
                em.add_field(name="Reason:", value=reason, inline=False)
                em.add_field(name="Staff Member:", value=interaction.user, inline=False)
                if interaction.guild.icon:
                    em.set_thumbnail(url=interaction.guild.icon.url)
                    return await member.send(embed=em)
                else:
                    return await member.send(embed=em)
            else:
                for channel in guild.channels:
                    muterole = await guild.create_role(name="Frozen🥶")
                    await channel.set_permissions(muterole, speak=False, send_messages=False)
                    await member.add_roles(muterole)
                    embed = discord.Embed(title=f"{member.name}#{member.discriminator}'s mouth is now frozen shut!", colour=0x6AA6BF)
                    embed.add_field(name="Reason:", value=reason, inline=False)
                    embed.set_thumbnail(url=member.display_avatar.url)
                    embed.set_footer(text=f"Frozen by {interaction.user}")
                    await interaction.response.send_message(embed=embed)
                    #send user message
                    em = discord.Embed(title=f"You have been muted at {interaction.guild.name}!", colour=0x6AA6BF)
                    em.add_field(name="Reason:", value=reason, inline=False)
                    em.add_field(name="Staff Member:", value=interaction.user, inline=False)
                    if interaction.guild.icon:
                        em.set_thumbnail(url=interaction.guild.icon.url)
                        return await member.send(embed=em)
                    else:
                        return await member.send(embed=em)

    @app_commands.command(name="melt", description="Unmute a member")
    @app_commands.describe(member="The member you want to unmute")
    @app_commands.describe(reason="The reason for the unmute")
    async def melt(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        guild = interaction.guild
        muterole  = discord.utils.get(guild.roles, name="Frozen🥶")
        if muterole not in member.roles:
            embed = discord.Embed(title=f"{member.name}#{member.discriminator} is not muted :|", colour=0x6AA6BF)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            if muterole:
                await member.remove_roles(muterole)
                embed = discord.Embed(title=f"{member.name}#{member.discriminator}'s mouth is now melted free!", colour=0x6AA6BF)
                embed.add_field(name="Reason:", value=reason, inline=False)
                embed.set_thumbnail(url=member.display_avatar.url)
                embed.set_footer(text=f"Melted by {interaction.user}")
                await interaction.response.send_message(embed=embed)
                #send user message
                em = discord.Embed(title=f"You have been unmuted at {interaction.guild.name}!", colour=0x6AA6BF)
                em.add_field(name="Reason:", value=reason, inline=False)
                em.add_field(name="Staff Member:", value=interaction.user, inline=False)
                if interaction.guild.icon:
                    em.set_thumbnail(url=interaction.guild.icon.url)
                    return await member.send(embed=em)
                else:
                    return await member.send(embed=em)
            if muterole is None:
                embed = discord.Embed(title=f"{member.name}#{member.discriminator} is not muted :|", colour=0x6AA6BF)
                return await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(client):
    await client.add_cog(moderation(client))