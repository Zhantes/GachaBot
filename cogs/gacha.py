import discord
from discord import app_commands
from discord.ext import commands
import random
import sqlite3

class Gacha(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online.")     
    
    @app_commands.command(name="pull", description ="Does 1 (one) pull in the bot gacha.")
    async def pull(self, interaction: discord.Interaction):

        connection = sqlite3.connect("./cogs/attempts.db")
        cursor = connection.cursor()
        guild_id = interaction.guild.id
        user_id = interaction.user.id

        cursor.execute("SELECT * FROM Gacha WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
        result = cursor.fetchone()

        if result is None:
            attempts = 1
            cursor.execute("INSERT INTO Gacha (guild_id, user_id, attempts) VALUES (?, ?, ?)", (guild_id, user_id, attempts))
        else:
            attempts = result[2] + 1
            cursor.execute("UPDATE Gacha SET attempts = ? WHERE guild_id = ? AND user_id = ?", (attempts, guild_id, user_id))

        roll = random.randrange(0,1000)

        if 994 < roll < 1000 or attempts % 91 == 90:
            pull_result = "**S-Rank**"
            rank_color = discord.Color.yellow()
            url = "https://static.wikia.nocookie.net/zenless-zone-zero/images/d/d0/Icon_AgentRank_S.png/revision/latest/scale-to-width-down/32?cb=20240914140011"
        elif 900 < roll < 994 or attempts % 11 == 10:
            pull_result = "A-rank"
            rank_color = discord.Color.purple()
            url = "https://static.wikia.nocookie.net/zenless-zone-zero/images/5/5c/Icon_AgentRank_A.png/revision/latest/scale-to-width-down/32?cb=20240914135957"
        else:
            pull_result = "B-rank"
            rank_color = discord.Color.blue()
            url = "https://static.wikia.nocookie.net/zenless-zone-zero/images/6/6e/Item_Rank_B.png/revision/latest/scale-to-width-down/32?cb=20231125052351"

        embed = discord.Embed(title="Pull result:", description=f"{pull_result}", color = rank_color)
        embed.set_thumbnail(url=url)
        await interaction.response.send_message(embed=embed)
        
        connection.commit()
        connection.close()

    @app_commands.command(name="10pull", description="Does 10 successive pulls on the bot gacha.")
    async def tenpull(self, interaction: discord.Interaction):

        pull_counter = 0
        pull_list = []

        while pull_counter < 10:
            connection = sqlite3.connect("./cogs/attempts.db")
            cursor = connection.cursor()
            guild_id = interaction.guild.id
            user_id = interaction.user.id

            cursor.execute("SELECT * FROM Gacha WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
            result = cursor.fetchone()

            if result is None:
                attempts = 1
                cursor.execute("INSERT INTO Gacha (guild_id, user_id, attempts) VALUES (?, ?, ?)", (guild_id, user_id, attempts))
            else:
                attempts = result[2] + 1
                cursor.execute("UPDATE Gacha SET attempts = ? WHERE guild_id = ? AND user_id = ?", (attempts, guild_id, user_id))

            roll = random.randrange(0,1000)

            if 994 < roll < 1000 or attempts % 91 == 90:
                pull_list.append("**S-rank**")
                s_color = True
            elif 900 < roll < 994 or attempts % 11 == 10:
                pull_list.append("A-rank")
                s_color = False
            else:
                pull_list.append("B-rank")
                s_color = False

            pull_counter += 1
            
            connection.commit()
            connection.close()

        if s_color == True:
            rank_color = discord.Color.yellow()
            url = "https://static.wikia.nocookie.net/zenless-zone-zero/images/d/d0/Icon_AgentRank_S.png/revision/latest/scale-to-width-down/32?cb=20240914140011"
        else:
            rank_color = discord.Color.purple()
            url = "https://static.wikia.nocookie.net/zenless-zone-zero/images/5/5c/Icon_AgentRank_A.png/revision/latest/scale-to-width-down/32?cb=20240914135957"

        embed = discord.Embed(title="Pulls result:", color=rank_color)
        embed.set_thumbnail(url=url)
        embed.add_field(name="#1:", value=f"{pull_list[0]}", inline=False)
        embed.add_field(name="#2:", value=f"{pull_list[1]}", inline=False)
        embed.add_field(name="#3:", value=f"{pull_list[2]}", inline=False)
        embed.add_field(name="#4:", value=f"{pull_list[3]}", inline=False)
        embed.add_field(name="#5:", value=f"{pull_list[4]}", inline=False)
        embed.add_field(name="#6:", value=f"{pull_list[5]}", inline=False)
        embed.add_field(name="#7:", value=f"{pull_list[6]}", inline=False)
        embed.add_field(name="#8:", value=f"{pull_list[7]}", inline=False)
        embed.add_field(name="#9:", value=f"{pull_list[8]}", inline=False)
        embed.add_field(name="#10:", value=f"{pull_list[9]}", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="info", description="Request information about gacha")
    async def info(self, interaction: discord.Interaction):

        connection = sqlite3.connect("./cogs/attempts.db")
        cursor = connection.cursor()
        guild_id = interaction.guild.id
        user_id = interaction.user.id

        attempts = cursor.execute("SELECT attempts FROM Gacha WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))

        if attempts is None:
            attempts = 0
        else:
            attempts = cursor.fetchone()

        embed = discord.Embed(title="Information on the Gacha:")
        embed.add_field(name= "Rates: ", value = "S-rank: 0.6%, A-rank: 9.4%, B-rank: 90%", inline=False)
        embed.add_field(name= "Pity: ", value = "S-rank: 90 attempts, A-Rank: 10 attempts")
        embed.add_field(name= "/pull: " , value="Does a single pull on the gacha.", inline=False)
        embed.add_field(name= "/10pull: ", value="Does 10 consecutive pulls on the gacha.", inline=False)
        embed.add_field(name="Attempts: ", value=f"{attempts}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

        connection.commit()
        connection.close()
    
    @app_commands.command(name="reset", description="Reset the user's attempts to 0, including pity.")
    @app_commands.checks.has_permissions(administrator=True)
    async def reset(self, interaction:discord.Interaction, user: discord.User):
        
        connection = sqlite3.connect("./cogs/attempts.db")
        cursor = connection.cursor()
        user_id = user.id

        cursor.execute("SELECT * FROM Gacha WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        if result is None:
            await interaction.response.send_message("User ID not found in database, they have not used the gacha yet.", ephemeral=True)
            return
        else:        
            cursor.execute("UPDATE Gacha SET attempts = 0 WHERE user_id = ?", (user_id,))
            print("Attempts reset.")
            await interaction.response.send_message(f"{user.name}'s attempts have been reset to 0.", ephemeral=True)

            connection.commit()
            connection.close()

    @reset.error
    async def reset_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have the required permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)    

async def setup(bot):
    await bot.add_cog(Gacha(bot))