import discord
import aiosqlite
from discord.ext import commands
from discord import app_commands

class store(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Store is ready.')

    @app_commands.command(name="store", description="Use your coins to buy items!")
    @app_commands.describe(item="The item you want to buy")
    @app_commands.choices(item=[
        app_commands.Choice(name="Heal (50 coins)", value=1),
        app_commands.Choice(name="Revive (50 coins)", value=2),
        app_commands.Choice(name="Max Revive (150 coins)", value=3),
        app_commands.Choice(name="10% Defence Increase (500 coins)", value=4),
        app_commands.Choice(name="10% Attack Increase (500 coins)", value=5)
    ])
    async def store(self, interaction: discord.Interaction, item: app_commands.Choice[int]):
        if item.value == 1:
            name = "Heal"
            cost = 50
        if item.value == 2:
            name = "Revive"
            cost = 50
        if item.value == 3:
            name = "Max_Revive"
            cost = 150
        if item.value == 4:
            name = "10%_Defence_Increase"
            cost = 500
        if item.value == 5:
            name = "10%_Attack_Increase"
            cost = 500
        g = interaction.guild.id
        table_name = f"_{g}"
        async with aiosqlite.connect("data/users.db") as db:
            async with db.cursor() as c:
                await c.execute("SELECT * FROM {} WHERE id = ?".format(table_name), (interaction.user.id,))
                get_info = await c.fetchall()
                bal = ''.join(f"{row[5]}" for row in get_info)
                if int(cost) > int(bal):
                    embed = discord.Embed(title="You can't afford this :|", colour=0x6AA6BF)
                    return await interaction.response.send_message(embed=embed, ephemeral=True)
                if int(cost) <= int(bal):
                    await c.execute("UPDATE {} SET balance = balance - ? WHERE id = ?".format(table_name), (str(cost), interaction.user.id,))
                    await db.commit()
                    if name == "10%_Defence_Increase":
                        await c.execute("UPDATE {} SET defence_min = defence_min + defence_min * ?, defence_max = defence_max + defence_max * ? WHERE id = ?".format(table_name), (str(0.1), str(0.1), interaction.user.id,))
                        await db.commit()
                        embed = discord.Embed(title="Your defence stats have increased by 10% for 500 coins!", colour=0x6AA6BF)
                        return await interaction.response.send_message(embed=embed)
                    if name == "10%_Attack_Increase":
                        await c.execute("UPDATE {} SET attack = attack + attack * ? WHERE id = ?".format(table_name), (str(0.1), interaction.user.id,))
                        await db.commit()
                        embed = discord.Embed(title="Your attack stats have increased by 10% for 500 coins!", colour=0x6AA6BF)
                        return await interaction.response.send_message(embed=embed)
                    async with aiosqlite.connect("data/inventory.db") as inv:
                        async with inv.cursor() as iv:
                            await iv.execute("CREATE TABLE IF NOT EXISTS {} (name text, id integer, Heal integer, Revive integer, Max_Revive integer)".format(table_name))
                            await inv.commit()
                            await iv.execute("SELECT * FROM {} WHERE id = ?".format(table_name), (interaction.user.id,))
                            check = await iv.fetchall()
                            res = ''.join(f"{row[0]}" for row in check)
                            if res == "":
                                if name == "Heal":
                                    await iv.execute("INSERT INTO {} (name, id, Heal, Revive, Max_Revive) VALUES (?, ?, ?, ?, ?)".format(table_name), (interaction.user.name, interaction.user.id, 1, 0, 0,))
                                    await inv.commit()
                                    embed = discord.Embed(title="You have bought a Heal for 50 coins!", colour=0x6AA6BF)
                                    embed.set_footer(text="/inventory")
                                    return await interaction.response.send_message(embed=embed)
                                if name == "Revive":
                                    await iv.execute("INSERT INTO {} (name, id, Heal, Revive, Max_Revive) VALUES (?, ?, ?, ?, ?)".format(table_name), (interaction.user.name, interaction.user.id, 0, 1, 0,))
                                    await inv.commit()
                                    embed = discord.Embed(title="You have bought a Revive for 50 coins!", colour=0x6AA6BF)
                                    embed.set_footer(text="/inventory")
                                    return await interaction.response.send_message(embed=embed)
                                if name == "Max_Revive":
                                    await iv.execute("INSERT INTO {} (name, id, Heal, Revive, Max_Revive) VALUES (?, ?, ?, ?, ?)".format(table_name), (interaction.user.name, interaction.user.id, 0, 0, 1,))
                                    await inv.commit()
                                    embed = discord.Embed(title="You have bought a Max Revive for 150 coins!", colour=0x6AA6BF)
                                    embed.set_footer(text="/inventory")
                                    return await interaction.response.send_message(embed=embed)
                            if res != "":
                                if name == "Heal":
                                    await iv.execute("UPDATE {} SET Heal = Heal + ? WHERE id = ?".format(table_name), (str(1), interaction.user.id,))
                                    await inv.commit()
                                    embed = discord.Embed(title="You have bought a Heal for 50 coins!", colour=0x6AA6BF)
                                    embed.set_footer(text="/inventory")
                                    return await interaction.response.send_message(embed=embed)
                                if name == "Revive":
                                    await iv.execute("UPDATE {} SET Revive = Revive + ? WHERE id = ?".format(table_name), (str(1), interaction.user.id,))
                                    await inv.commit()
                                    embed = discord.Embed(title="You have bought a Revive for 50 coins!", colour=0x6AA6BF)
                                    embed.set_footer(text="/inventory")
                                    return await interaction.response.send_message(embed=embed)
                                if name == "Max_Revive":
                                    await iv.execute("UPDATE {} SET Max_Revive = Max_Revive + ? WHERE id = ?".format(table_name), (str(1), interaction.user.id,))
                                    await inv.commit()
                                    embed = discord.Embed(title="You have bought a Max Revive for 150 coins!", colour=0x6AA6BF)
                                    embed.set_footer(text="/inventory")
                                    return await interaction.response.send_message(embed=embed)

    @app_commands.command(name="inventory", description="View your items!")
    async def inventory(self, interaction: discord.Interaction):
        g = interaction.guild.id
        table_name = f"_{g}"
        async with aiosqlite.connect("data/inventory.db") as db:
            async with db.cursor() as c:
                await c.execute("SELECT * FROM {} WHERE id = ?".format(table_name), (interaction.user.id,))
                check = await c.fetchall()
                output = ''.join(f"{row[0]}" for row in check)
                if output == "":
                    embed = discord.Embed(title="You never bought any items :|", colour=0x6AA6BF)
                    return await interaction.response.send_message(embed=embed, ephemeral=True)
                if output != "":
                    heal = ''.join(f"{row[2]}" for row in check)
                    if heal == "0":
                        heal = "None"
                    revive = ''.join(f"{row[3]}" for row in check)
                    if revive == "0":
                        revive = "None"
                    max_revive = ''.join(f"{row[4]}" for row in check)
                    if max_revive == "0":
                        max_revive = "None"
                    embed = discord.Embed(title="Your Inventory", colour=0x6AA6BF)
                    embed.add_field(name="Heals:", value=heal, inline=False)
                    embed.add_field(name="Revives:", value=revive, inline=False)
                    embed.add_field(name="Max Revives:", value=max_revive, inline=False)
                    embed.set_thumbnail(url=interaction.user.display_avatar.url)
                    return await interaction.response.send_message(embed=embed)

    @app_commands.command(name="use_item", description="Use one of your items!")
    @app_commands.describe(item="The item you want to use")
    @app_commands.choices(item=[
        app_commands.Choice(name="Heal", value=1),
        app_commands.Choice(name="Revive", value=2),
        app_commands.Choice(name="Max Revive", value=3)
    ])
    async def use_item(self, interaction: discord.Interaction, item: app_commands.Choice[int]):
        g = interaction.guild.id
        table_name = f"_{g}"
        async with aiosqlite.connect("data/inventory.db") as db:
            async with db.cursor() as c:
                await c.execute("SELECT * FROM {} WHERE id = ?".format(table_name), (interaction.user.id,))
                check = await c.fetchall()
                output = ''.join(f"{row[0]}" for row in check)
                if output == "":
                    embed = discord.Embed(title="You have no items :|", colour=0x6AA6BF)
                    return await interaction.response.send_message(embed=embed, ephemeral=True)
                if output != "":
                    async with aiosqlite.connect("data/users.db") as ud:
                        async with ud.cursor() as u:
                            await u.execute("SELECT * FROM {} WHERE id = ?".format(table_name), (interaction.user.id,))
                            get_user_info = await u.fetchall()
                            user_defence_min = ''.join(f"{row[3]}" for row in get_user_info)
                            user_defence_max = ''.join(f"{row[4]}" for row in get_user_info)
                            if item.value == 1:
                                heals = ''.join(f"{row[2]}" for row in check)
                                if int(heals) == int(0):
                                    embed = discord.Embed(title="You have no heals :|", colour=0x6AA6BF)
                                    return await interaction.response.send_message(embed=embed, ephemeral=True)
                                if int(heals) > int(0):
                                    if int(user_defence_min) <= int(0):
                                        embed = discord.Embed(title="You can't use heal because you are dead :|", colour=0x6AA6BF)
                                        return await interaction.response.send_message(embed=embed, ephemeral=True)
                                    if int(user_defence_min) == int(user_defence_max):
                                        embed = discord.Embed(title="You can't use heal because you are already at max health :|", colour=0x6AA6BF)
                                        return await interaction.response.send_message(embed=embed, ephemeral=True)
                                    if int(user_defence_min) > int(0):
                                        await c.execute("UPDATE {} SET Heal = Heal - ? WHERE id = ?".format(table_name), (str(1), interaction.user.id,))
                                        await db.commit()
                                        await u.execute("UPDATE {} SET defence_min = ? WHERE id = ?".format(table_name), (str(user_defence_max), interaction.user.id,))
                                        await ud.commit()
                                        embed = discord.Embed(title="Your health has been restored to it's max value!", colour=0x6AA6BF)
                                        return await interaction.response.send_message(embed=embed)
                            if item.value == 2:
                                revives = ''.join(f"{row[3]}" for row in check)
                                if int(revives) == int(0):
                                    embed = discord.Embed(title="You have no revives :|", colour=0x6AA6BF)
                                    return await interaction.response.send_message(embed=embed, ephemeral=True)
                                if int(revives) > int(0):
                                    if int(user_defence_min) > int(0):
                                        embed = discord.Embed(title="You can't use revive because you aren't dead :|", colour=0x6AA6BF)
                                        return await interaction.response.send_message(embed=embed, ephemeral=True)
                                    if int(user_defence_min) <= int(0):
                                        revive_health = int(user_defence_max) / int(2)
                                        await c.execute("UPDATE {} SET Revive = Revive - ? WHERE id = ?".format(table_name), (str(1), interaction.user.id,))
                                        await db.commit()
                                        await u.execute("UPDATE {} SET defence_min = ? WHERE id = ?".format(table_name), (str(revive_health), interaction.user.id,))
                                        await ud.commit()
                                        embed = discord.Embed(title="You have been revived!", colour=0x6AA6BF)
                                        return await interaction.response.send_message(embed=embed)
                            if item.value == 3:
                                max_revives = ''.join(f"{row[4]}" for row in check)
                                if int(max_revives) == int(0):
                                    embed = discord.Embed(title="You have no max revives :|", colour=0x6AA6BF)
                                    return await interaction.response.send_message(embed=embed, ephemeral=True)
                                if int(max_revives) > int(0):
                                    if int(user_defence_min) > int(0):
                                        embed = discord.Embed(title="You can't use revive because you aren't dead :|", colour=0x6AA6BF)
                                        return await interaction.response.send_message(embed=embed, ephemeral=True)
                                    if int(user_defence_min) <= int(0):
                                        await c.execute("UPDATE {} SET Max_Revive = Max_Revive - ? WHERE id = ?".format(table_name), (str(1), interaction.user.id,))
                                        await db.commit()
                                        await u.execute("UPDATE {} SET defence_min = ? WHERE id = ?".format(table_name), (str(user_defence_max), interaction.user.id,))
                                        await ud.commit()
                                        embed = discord.Embed(title="You have been revived with max health!", colour=0x6AA6BF)
                                        return await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(store(client))