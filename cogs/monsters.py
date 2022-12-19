import discord
import random
import aiosqlite
from discord.ext import commands
from discord import app_commands

class monsters(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Monster spawning is ready.')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
            async with aiosqlite.connect("data/monsters.db") as db:
                    async with db.cursor() as c:
                        await c.execute("CREATE TABLE IF NOT EXISTS monsters (name text, attack_min integer, attack_max integer, defence integer, sprite_url text)")
                        await db.commit()
                        await c.execute("SELECT * FROM monsters")
                        check = await c.fetchall()
                        output = ''.join(f"{row[0]}" for row in check)
                        if output == "":
                                    await c.execute("INSERT INTO monsters (name, attack_min, attack_max, defence, sprite_url) VALUES (?, ?, ?, ?, ?)", ("Taxes", 80, 100, 110, "images/monsters/Taxes.jpg"))
                                    await c.execute("INSERT INTO monsters (name, attack_min, attack_max, defence, sprite_url) VALUES (?, ?, ?, ?, ?)", ("Grinch", 65, 80, 90, "images/monsters/Grinch.jpg"))
                                    await c.execute("INSERT INTO monsters (name, attack_min, attack_max, defence, sprite_url) VALUES (?, ?, ?, ?, ?)", ("Santa", 45, 60, 80, "images/monsters/Santa.jpg"))
                                    await c.execute("INSERT INTO monsters (name, attack_min, attack_max, defence, sprite_url) VALUES (?, ?, ?, ?, ?)", ("Human", 45, 60, 70, "images/monsters/Human.png"))
                                    await c.execute("INSERT INTO monsters (name, attack_min, attack_max, defence, sprite_url) VALUES (?, ?, ?, ?, ?)", ("Raindeer", 35, 40, 50, "images/monsters/Raindeer.jpg"))
                                    await c.execute("INSERT INTO monsters (name, attack_min, attack_max, defence, sprite_url) VALUES (?, ?, ?, ?, ?)", ("Elf", 25, 30, 40, "images/monsters/Elf.png"))
                                    await c.execute("INSERT INTO monsters (name, attack_min, attack_max, defence, sprite_url) VALUES (?, ?, ?, ?, ?)", ("Snowman", 15, 20, 30, "images/monsters/Snowman.png"))
                                    await db.commit()
                        if output != "":
                                return
                        await c.execute("CREATE TABLE IF NOT EXISTS in_channel_check (state text, guild integer, monster text, attack integer, defence integer, reward integer, channel text)")
                        await db.commit()
                        await c.execute("SELECT * FROM in_channel_check WHERE guild = ?", (guild.id,))
                        chek = await c.fetchall()
                        res = ''.join(f"{row[0]}" for row in chek)
                        if res == "":
                            await c.execute("INSERT INTO in_channel_check (state, guild) VALUES (?, ?)", ("no", guild.id))
                            await db.commit()
                        else:
                            return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            if message.content.startswith("ice!"):
                return
            async with aiosqlite.connect("data/monsters.db") as db:
                async with db.cursor() as c:
                    await c.execute("CREATE TABLE IF NOT EXISTS monsters (name text, attack_min integer, attack_max integer, defence integer, sprite_url text)")
                    await db.commit()
                    await c.execute("SELECT * FROM monsters")
                    check = await c.fetchall()
                    output = ''.join(f"{row[0]}" for row in check)
                    if output == "":
                                await c.execute("INSERT INTO monsters (name, attack_min, attack_max, defence, sprite_url) VALUES (?, ?, ?, ?, ?)", ("Taxes", 80, 100, 110, "images/monsters/Taxes.jpg"))
                                await c.execute("INSERT INTO monsters (name, attack_min, attack_max, defence, sprite_url) VALUES (?, ?, ?, ?, ?)", ("Grinch", 65, 80, 90, "images/monsters/Grinch.jpg"))
                                await c.execute("INSERT INTO monsters (name, attack_min, attack_max, defence, sprite_url) VALUES (?, ?, ?, ?, ?)", ("Santa", 45, 60, 80, "images/monsters/Santa.jpg"))
                                await c.execute("INSERT INTO monsters (name, attack_min, attack_max, defence, sprite_url) VALUES (?, ?, ?, ?, ?)", ("Human", 45, 60, 70, "images/monsters/Human.png"))
                                await c.execute("INSERT INTO monsters (name, attack_min, attack_max, defence, sprite_url) VALUES (?, ?, ?, ?, ?)", ("Raindeer", 35, 40, 50, "images/monsters/Raindeer.jpg"))
                                await c.execute("INSERT INTO monsters (name, attack_min, attack_max, defence, sprite_url) VALUES (?, ?, ?, ?, ?)", ("Elf", 25, 30, 40, "images/monsters/Elf.png"))
                                await c.execute("INSERT INTO monsters (name, attack_min, attack_max, defence, sprite_url) VALUES (?, ?, ?, ?, ?)", ("Snowman", 15, 20, 30, "images/monsters/Snowman.png"))
                                await db.commit()

                    await c.execute("CREATE TABLE IF NOT EXISTS in_channel_check (state text, guild integer, monster text, attack integer, defence integer, reward integer, channel text)")
                    await db.commit()
                    await c.execute("SELECT * FROM in_channel_check WHERE guild = ?", (message.guild.id,))
                    chek = await c.fetchall()
                    res = ''.join(f"{row[0]}" for row in chek)
                    if res == "":
                        await c.execute("INSERT INTO in_channel_check (state, guild) VALUES (?, ?)", ("no", message.guild.id,))
                        await db.commit()

                    await c.execute("SELECT * FROM in_channel_check WHERE guild = ?", (message.guild.id,))
                    chek = await c.fetchall()
                    res = ''.join(f"{row[0]}" for row in chek)
                    if res == "no":
                        num = random.randint(1, 10)
                        if num == 1:
                            monster_spawner_decider = random.randint(1, 100)
                            if monster_spawner_decider <= 1 and monster_spawner_decider <= 5:
                                await c.execute("SELECT * FROM monsters WHERE rowid = 1")
                            if monster_spawner_decider > 5 and monster_spawner_decider <= 10:
                                await c.execute("SELECT * FROM monsters WHERE rowid = 2")
                            if monster_spawner_decider > 10 and monster_spawner_decider <= 20:
                                await c.execute("SELECT * FROM monsters WHERE rowid = 3")
                            if monster_spawner_decider > 20 and monster_spawner_decider <= 35:
                                await c.execute("SELECT * FROM monsters WHERE rowid = 4")
                            if monster_spawner_decider > 35 and monster_spawner_decider <= 50:
                                await c.execute("SELECT * FROM monsters WHERE rowid = 5")
                            if monster_spawner_decider > 50 and monster_spawner_decider <= 70:
                                await c.execute("SELECT * FROM monsters WHERE rowid = 6")
                            if monster_spawner_decider > 70 and monster_spawner_decider <= 100:
                                await c.execute("SELECT * FROM monsters WHERE rowid = 7")
                            #await c.execute("SELECT * FROM monsters ORDER BY RANDOM() LIMIT 1")
                            get_rand_monster = await c.fetchall()
                            #get the attack
                            a = ''.join(f"{row[1]}" for row in get_rand_monster)
                            b = ''.join(f"{row[2]}" for row in get_rand_monster)
                            get_attack = random.randint(int(a), int(b))
                            monster_name = ''.join(f"{row[0]}" for row in get_rand_monster)
                            monster_defence = ''.join(f"{row[3]}" for row in get_rand_monster)
                            monster_img = ''.join(f"{row[4]}" for row in get_rand_monster)
                            file = discord.File(f"{monster_img}", filename=f"{monster_name}.png")
                            reward = get_attack * 2
                            await c.execute("UPDATE in_channel_check SET state = ?, monster = ?, attack = ?, defence = ?, reward = ?, channel = ? WHERE guild = ?", ("yes", monster_name, get_attack, monster_defence, reward, message.channel.name, message.guild.id,))
                            await db.commit()
                            embed = discord.Embed(title=f"{monster_name} has spawned!", colour=0x6AA6BF)
                            embed.add_field(name="Attack", value=get_attack, inline=True)
                            embed.add_field(name="Defence", value=monster_defence, inline=True)
                            embed.add_field(name="Reward", value=f"{reward} coins", inline=True)
                            embed.set_image(url=f"attachment://{monster_name}.png")
                            return await message.channel.send(file=file, embed=embed)
                        if num != 1:
                            return
                    if res == "yes":
                        return

        await self.client.process_commands(message)

    @app_commands.command(name="attack_monster", description="Attack the currently spawned monster")
    async def attack_monster(self, interaction: discord.Interaction):
        g = interaction.guild.id
        table_name = f"_{g}"
        async with aiosqlite.connect("data/monsters.db") as db:
            async with db.cursor() as c:
                await c.execute("SELECT * FROM in_channel_check WHERE guild = ?", (interaction.guild.id,))
                chek = await c.fetchall()
                channel = interaction.channel.name
                monster_channel = ''.join(f"{row[6]}" for row in chek)
                if channel != str(monster_channel):
                    embed = discord.Embed(title="Must be in same channel as monster!", colour=0x6AA6BF)
                    return await interaction.response.send_message(embed=embed)
                res = ''.join(f"{row[0]}" for row in chek)
                if res == "no":
                    embed = discord.Embed(title="There are currently no monsters :|", colour=0x6AA6BF)
                    return await interaction.response.send_message(embed=embed)
                async with aiosqlite.connect("data/users.db") as ub:
                    async with ub.cursor() as u:
                        await u.execute("SELECT * FROM {} WHERE id = {}".format(table_name, interaction.user.id,))
                        get_user_info = await u.fetchall()
                        await c.execute("SELECT * FROM monsters")
                        await c.fetchall()

                        user_attack = ''.join(f"{row[2]}" for row in get_user_info)
                        user_defence_min = ''.join(f"{row[3]}" for row in get_user_info)
                        monster_name = ''.join(f"{row[2]}" for row in chek)
                        monster_attack = ''.join(f"{row[3]}" for row in chek)
                        monster_defence = ''.join(f"{row[4]}" for row in chek)
                        monster_reward = ''.join(f"{row[5]}" for row in chek)

                        user_damage_result = int(monster_defence) - int(user_attack)
                        monster_damage_result = int(user_defence_min) - int(monster_attack)

                if res == "yes":
                        if user_defence_min == "0":
                            embed = discord.Embed(title="You can't attack because your dead 💀", colour=0x6AA6BF)
                            return await interaction.response.send_message(embed=embed, ephemeral=True)
                        if user_defence_min != "0":
                            if user_damage_result <= 0:
                                async with aiosqlite.connect("data/users.db") as ub:
                                    async with ub.cursor() as u:
                                        await u.execute("UPDATE {} SET balance = balance + {} WHERE id = {}".format(table_name, monster_reward, interaction.user.id,))
                                        await ub.commit()
                                        await c.execute("UPDATE in_channel_check SET state = ?, monster = ?, attack = ?, defence = ?, reward = ?, channel = ? WHERE guild = ?", ("no", None, None, None, None, None, interaction.guild.id))
                                        await db.commit()
                                        return await interaction.response.send_message(f"{interaction.user.mention} has made {monster_name} no longer exist and has gained {monster_reward} coins!")

                            if user_damage_result > 0:
                                if monster_damage_result <= 0:
                                    async with aiosqlite.connect("data/users.db") as ub:
                                        async with ub.cursor() as u:
                                            await u.execute("UPDATE {} SET defence_min = {} WHERE id = {}".format(table_name, int(0), interaction.user.id,))
                                            await ub.commit()
                                            await interaction.response.send_message(f"{interaction.user.mention} has died 😵")
                                    will_monster_run = random.randint(1, 10)
                                    if will_monster_run == 1:
                                        await c.execute("UPDATE in_channel_check SET state = ?, monster = ?, attack = ?, defence = ?, reward = ?, channel = ? WHERE guild = ?", ("no", None, None, None, None, None, interaction.guild.id))
                                        await c.commit()
                                        embed = discord.Embed(title=f"{monster_name} has gone to the milk store and will not be coming back 🥛", colour=0x6AA6BF)
                                        return await interaction.response.send_message(embed=embed)
                                if monster_damage_result > 0:
                                    async with aiosqlite.connect("data/monsters.db") as db:
                                        async with db.cursor() as c:
                                            await c.execute("UPDATE in_channel_check SET defence = ? WHERE guild = ?", (user_damage_result, interaction.guild.id))
                                            await db.commit()
                                    async with aiosqlite.connect("data/users.db") as ub:
                                        async with ub.cursor() as u:
                                            await u.execute("UPDATE {} SET defence_min = ? WHERE id = ?".format(table_name), (monster_damage_result, interaction.user.id,))
                                            await ub.commit()
                                    embed = discord.Embed(description=f"{interaction.user.mention} has done **{user_attack}** of damage on {monster_name} leaving {monster_name} on **{user_damage_result}**!\n{monster_name} responds by attacking {interaction.user.mention} with {monster_attack} attack points leaving {interaction.user.mention} on {monster_damage_result}!", colour=0x6AA6BF)
                                    return await interaction.response.send_message(embed=embed)

    @app_commands.command(name="kill_monster", description="Kill the currently spawned monster")
    async def kill_monster(self, interaction: discord.Interaction):
        async with aiosqlite.connect("data/monsters.db") as db:
            async with db.cursor() as c:
                await c.execute("SELECT * FROM in_channel_check WHERE guild = ?", (interaction.guild.id,))
                get_result = await c.fetchall()
                state = ''.join(f"{row[0]}" for row in get_result)
                if state == "yes":
                    await c.execute("UPDATE in_channel_check SET state = ?, monster = ?, attack = ?, defence = ?, reward = ?, channel = ? WHERE guild = ?", ("no", None, None, None, None, None, interaction.guild.id))
                    await db.commit()
                    embed = discord.Embed(title="Monster has been successfully terminated!", colour=0x6AA6BF)
                    return await interaction.response.send_message("Monster has been successfully terminated!")
                if state == "no":
                    embed = discord.Embed(title="No monsters are currently active!",colour=0x6AA6BF)
                    return await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="revive", description="Bring a player back from the dead")
    @app_commands.describe(member="The user you want to revive")
    async def revive(self, interaction: discord.Interaction, member: discord.Member):
        g = interaction.guild.id
        table_name = f"_{g}"
        async with aiosqlite.connect("data/users.db") as db:
            async with db.cursor() as c:
                await c.execute("SELECT * FROM {} WHERE id = {}".format(table_name, member.id))
                get_result = await c.fetchall()
                user_defence = ''.join(f"{row[3]}" for row in get_result)
                if user_defence == "0":
                    await c.execute("UPDATE {} SET defence_min = {} WHERE id = {}".format(table_name, 50, member.id))
                    await db.commit()
                    embed = discord.Embed(title=f"{member.name}#{member.discriminator} has been revived!", colour=0x6AA6BF)
                    return await interaction.response.send_message(embed=embed)
                if user_defence != "0":
                    embed = discord.Embed(title="User is not dead :|", colour=0x6AA6BF)
                    return await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(client):
    await client.add_cog(monsters(client))