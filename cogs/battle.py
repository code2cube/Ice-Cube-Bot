import discord
import aiosqlite
import random
import time
from easy_pil import Editor, load_image_async
from PIL import Image
from discord import File
from discord.ext import commands
from discord import app_commands

class battle(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Battle is ready.')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        else:
            get_guild = payload.member.guild.id
            guild_for_table = f"_{get_guild}"
            channel = self.client.get_channel(payload.channel_id)
            async with aiosqlite.connect("data/battle.db") as db:
                async with db.cursor() as c:
                    await c.execute("SELECT * FROM {}".format(guild_for_table))
                    m = await c.fetchall()
                    if m is None:
                        return
                    else:
                        challenger = ''.join(f"{row[1]}" for row in m)
                        challenged_person = ''.join(f"{row[3]}" for row in m)
                        if int(challenged_person) != int(payload.member.id):
                            return
                        if int(challenged_person) == int(payload.member.id):
                            if payload.emoji.name == '👍':
                                get_status = ''.join(f"{row[4]}" for row in m)
                                if str(get_status) == "confirmed":
                                    return
                                if str(get_status) != "confirmed":
                                        msg_id = ''.join(f"{row[5]}" for row in m)
                                        #guild = user.guild
                                        if payload.message_id == int(msg_id):
                                            first_turn = random.randint(1, 2)
                                            if first_turn == 1:
                                                first = challenger
                                            if first_turn == 2:
                                                first = challenged_person
                                            await c.execute("UPDATE {} SET status = ?, turn = ?".format(guild_for_table), ("confirmed", first))
                                            await db.commit()
                                            background = Editor("images/duel.png")
                                            challenger_image = discord.utils.get(payload.member.guild.members, id=int(challenger))
                                            challenged_image = discord.utils.get(payload.member.guild.members, id=int(challenged_person))
                                            _author_image = await load_image_async(challenger_image.display_avatar.url)
                                            _member_image = await load_image_async(challenged_image.display_avatar.url)
                                            _member_image = _member_image.transpose(Image.FLIP_LEFT_RIGHT)
                                            _author_circle = Editor(_author_image).resize((150, 150)).circle_image()
                                            _member_image = Editor(_member_image).resize((150, 150)).circle_image()
                                            background.paste(_author_circle, (110, 100))
                                            background.paste(_member_image, (560, 100))
                                            file = File(fp=background.image_bytes, filename=f"snowball.png")
                                            await channel.send(content=f"<@{challenger}> vs <@{challenged_person}>", file=file)
                                            time.sleep(3)
                                            await channel.send(f"It is now <@{first}>'s turn!")
                                        else:
                                            return
                            if payload.emoji.name == '👎':
                                await c.execute("DELETE FROM {} WHERE player1_id = ? AND player2_id = ?".format(guild_for_table), (challenger, challenged_person,))
                                await db.commit()
                                return await channel.send(f"<@{challenged_person}> has declined the duel request from <@{challenger}>")



    @app_commands.command(name="battle", description="Challange a player to a duel!")
    @app_commands.describe(opponent="The user you want to duel")
    async def battle(self, interaction: discord.Interaction, opponent: discord.Member):
        get_guild = interaction.guild.id
        guild_for_table = f"_{get_guild}"
        async with aiosqlite.connect("data/battle.db") as db:
            async with db.cursor() as c:
                await c.execute("CREATE TABLE IF NOT EXISTS {} (player1_name text, player1_id integer, player2_name text, player2_id integer, status text, msg_id integer, turn integer)".format(guild_for_table))
                await db.commit()
                await c.execute("SELECT * FROM {} WHERE player1_id = ? AND player2_id = ?".format(guild_for_table), (interaction.user.id, opponent.id,))
                check = await c.fetchall()
                output = ''.join(f"{row[0]}" for row in check)
                if output != "":
                    embed = discord.Embed(title="These players are currently in a duel or are waiting for opponent response!", colour=0x6AA6BF)
                    return await interaction.response.send_message(embed=embed, ephemeral=True)
                if output == "":
                    await c.execute("INSERT INTO {} (player1_name, player1_id, player2_name, player2_id, status) VALUES (?, ?, ?, ?, ?)".format(guild_for_table), (f"{interaction.user.name}#{interaction.user.discriminator}", interaction.user.id, f"{opponent.name}#{opponent.discriminator}", opponent.id, "pending",))
                    await db.commit()
                    async with aiosqlite.connect("data/users.db") as ud:
                        async with ud.cursor() as u:
                            await u.execute("SELECT * FROM {} WHERE id = ?".format(guild_for_table), (opponent.id,))
                            get_opponent_data = await u.fetchall()
                            wins = ''.join(f"{row[6]}" for row in get_opponent_data)
                            losses = ''.join(f"{row[7]}" for row in get_opponent_data)
                            bal = ''.join(f"{row[5]}" for row in get_opponent_data)
                            calc_reward = int(bal) / int(6)
                            reward = round(calc_reward)
                    embed = discord.Embed(title="New Duel Request!", colour=0x6AA6BF)
                    embed.add_field(name="Opponent:", value=interaction.user.mention, inline=False)
                    embed.add_field(name="Wins:", value=wins, inline=False)
                    embed.add_field(name="Losses:", value=losses, inline=False)
                    embed.add_field(name="Reward:", value=f"{reward} coins", inline=False)
                    embed.set_thumbnail(url=interaction.user.display_avatar.url)
                    embed.set_footer(text="Will you accept?")
                    await interaction.response.send_message(content=opponent.mention, embed=embed)
                    msg = await interaction.original_response()
                    await c.execute("UPDATE {} SET msg_id = ?".format(guild_for_table), (msg.id,))
                    await db.commit()
                    await msg.add_reaction('👍')
                    await msg.add_reaction('👎')

    @app_commands.command(name="attack", description="Attack the player your in a duel with!")
    async def attack(self, interaction: discord.Interaction):
        get_guild = interaction.guild.id
        guild_for_table = f"_{get_guild}"
        async with aiosqlite.connect("data/battle.db") as db:
            async with db.cursor() as c:
                await c.execute("SELECT * from {} WHERE player1_id = ? OR player2_id = ?".format(guild_for_table), (interaction.user.id, interaction.user.id,))
                check = await c.fetchall()
                if check == "":
                    embed = discord.Embed(title="Your not in a duel :|", colour=0x6AA6BF)
                    return await interaction.response.send_message(embed=embed, ephemeral=True)
                if check != "":
                    turn = ''.join(f"{row[6]}" for row in check)
                    if int(turn) != interaction.user.id:
                        embed = discord.Embed(title="It is not your turn!", colour=0x6AA6BF)
                        return await interaction.response.send_message(embed=embed, ephemeral=True)
                    if int(turn) == interaction.user.id:
                        player1_id = ''.join(f"{row[1]}" for row in check)
                        player2_id = ''.join(f"{row[3]}" for row in check)
                        if player1_id == turn:
                            opponent = player2_id
                        if player2_id == turn:
                            opponent = player1_id
                        async with aiosqlite.connect("data/users.db") as ud:
                            async with ud.cursor() as u:
                                await u.execute("SELECT * FROM {} WHERE id = ?".format(guild_for_table), (interaction.user.id,))
                                get_user = await u.fetchall()
                                user_attack = ''.join(f"{row[2]}" for row in get_user)
                                user_defence_min = ''.join(f"{row[3]}" for row in get_user)
                                user_defence_max = ''.join(f"{row[4]}" for row in get_user)
                                user_balance = ''.join(f"{row[5]}" for row in get_user)
                                #await interaction.response.send_message("guess what not broken")
                                await u.execute("SELECT * FROM {} WHERE id = ?".format(guild_for_table), (int(opponent),))
                                get_opponent = await u.fetchall()
                                opponent_attack = ''.join(f"{row[2]}" for row in get_opponent)
                                opponent_defence_min = ''.join(f"{row[3]}" for row in get_opponent)
                                opponent_defence_max = ''.join(f"{row[4]}" for row in get_opponent)
                                opponent_balance = ''.join(f"{row[5]}" for row in get_opponent)

                                opponent_remaning_defence = int(opponent_defence_min) - int(user_attack)
                                if opponent_remaning_defence <= 0:
                                    get_reward = int(opponent_balance) / int(6)
                                    reward = round(get_reward)
                                    await u.execute("UPDATE {} SET defence_min = ?, balance = balance - ?, losses = losses + ? WHERE id = ?".format(guild_for_table), (str(0), reward, str(1), int(opponent),))
                                    await u.execute("UPDATE {} SET balance = balance + ?, wins = wins + ? WHERE id = ?".format(guild_for_table), (reward, str(1), interaction.user.id,))
                                    await ud.commit()
                                    await c.execute("DELETE FROM {} WHERE player1_id = ?".format(guild_for_table), (opponent,))
                                    await db.commit()
                                    return await interaction.response.send_message(f"{interaction.user.mention} has sent <@{opponent}> to the spirit realm and has gained {reward} coins!")
                                if opponent_remaning_defence > 0:
                                    await u.execute("UPDATE {} SET defence_min = ? WHERE id = ?".format(guild_for_table), (opponent_remaning_defence, int(opponent),))
                                    await ud.commit()
                                    await c.execute("UPDATE {} SET turn = ?".format(guild_for_table), (int(opponent),))
                                    await db.commit()
                                    return await interaction.response.send_message(f"{interaction.user.mention} has done {user_attack} on <@{opponent}> leaving them on {opponent_remaning_defence}/{opponent_defence_max}!\nIt is now <@{opponent}>'s turn!")

async def setup(client):
    await client.add_cog(battle(client))