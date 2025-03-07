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
            attempts, s_pity, a_pity, tokens = 1, 1, 1, 0
            cursor.execute("INSERT INTO Gacha (guild_id, user_id, attempts, s_pity, a_pity, tokens) VALUES (?, ?, ?, ?, ?, ?)", (guild_id, user_id, attempts, s_pity, a_pity, tokens))
        else:
            attempts, s_pity, a_pity, tokens = result[2] + 1, result[3] + 1, result[4] + 1, result[5]
            cursor.execute("UPDATE Gacha SET attempts = ?, S_pity = ?, A_pity = ? WHERE guild_id = ? AND user_id = ?", (attempts, s_pity, a_pity, guild_id, user_id))

            if tokens >= 1:
                tokens -= 1
                cursor.execute("UPDATE Gacha SET tokens = ? WHERE guild_id = ? AND user_id = ?", (tokens, guild_id, user_id))
                roll = random.randrange(0,1000)

                if 994 < roll < 1000 or s_pity == 89:
                    pull_result = "**S-Rank**"
                    rank_color = discord.Color.yellow()
                    s_pity = 0
                    cursor.execute("UPDATE Gacha SET S_pity = 0 WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
                    url = "https://static.wikia.nocookie.net/zenless-zone-zero/images/d/d0/Icon_AgentRank_S.png/revision/latest/scale-to-width-down/32?cb=20240914140011"
                elif 900 < roll < 994 or a_pity == 9:
                    pull_result = "A-rank"
                    rank_color = discord.Color.purple()
                    a_pity = 0
                    cursor.execute("UPDATE Gacha SET A_pity = 0 WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
                    url = "https://static.wikia.nocookie.net/zenless-zone-zero/images/5/5c/Icon_AgentRank_A.png/revision/latest/scale-to-width-down/32?cb=20240914135957"
                else:
                    pull_result = "B-rank"
                    rank_color = discord.Color.blue()
                    url = "https://static.wikia.nocookie.net/zenless-zone-zero/images/6/6e/Item_Rank_B.png/revision/latest/scale-to-width-down/32?cb=20231125052351"

                embed = discord.Embed(title="Pull result:", description=f"{pull_result}", color = rank_color)
                embed.set_thumbnail(url=url)
                await interaction.response.send_message(embed=embed)
            else:
                attempts -= 1
                cursor.execute("UPDATE Gacha SET attempts = ? WHERE guild_id = ? AND user_id = ?", (attempts, guild_id, user_id))
                await interaction.response.send_message("You do not have enough tokens.", ephemeral=True)
        
        connection.commit()
        connection.close()

    @app_commands.command(name="10pull", description="Does 10 successive pulls on the bot gacha.")
    async def tenpull(self, interaction: discord.Interaction):

        pull_counter = 0
        pull_list = []
        connection = sqlite3.connect("./cogs/attempts.db")
        cursor = connection.cursor()
        guild_id = interaction.guild.id
        user_id = interaction.user.id
        cursor.execute("SELECT * FROM Gacha WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
        result = cursor.fetchone()
        tokens = result[5]

        if tokens >= 10:
            while pull_counter < 10:
                cursor.execute("SELECT * FROM Gacha WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
                result = cursor.fetchone()

                if result is None:
                    attempts, s_pity, a_pity, tokens = 1, 1, 1, 0
                    cursor.execute("INSERT INTO Gacha (guild_id, user_id, attempts, s_pity, a_pity, tokens) VALUES (?, ?, ?, ?, ?, ?)", (guild_id, user_id, attempts, s_pity, a_pity, tokens))
                else:
                    attempts, s_pity, a_pity, tokens = result[2] + 1, result[3] + 1, result[4] + 1, result[5]
                    cursor.execute("UPDATE Gacha SET attempts = ?, s_pity = ?, a_pity = ? WHERE guild_id = ? AND user_id = ?", (attempts, s_pity, a_pity, guild_id, user_id))

                roll = random.randrange(0,1000)

                if 994 < roll < 1000 or s_pity >= 89:
                    pull_list.append("**S-rank**")
                    s_color = True
                    a_color = False
                    s_pity = 0
                    cursor.execute("UPDATE Gacha SET S_pity = 0 WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
                elif 900 < roll < 994 or a_pity >= 9:
                    pull_list.append("A-rank")
                    s_color = False
                    a_color = True
                    a_pity = 0
                    cursor.execute("UPDATE Gacha SET A_pity = 0 WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
                else:
                    pull_list.append("B-rank")

                pull_counter += 1
                tokens -= 1
                cursor.execute("UPDATE Gacha SET tokens = ? WHERE guild_id = ? AND user_id = ?", (tokens, guild_id, user_id))
                print(f"Pull complete. Pull Counter: {pull_counter}. Tokens left: {tokens}")
        else:
            await interaction.response.send_message("You do not have enough tokens.", ephemeral=True)
            return

            
        connection.commit()
        connection.close()

        if s_color == True:
            rank_color = discord.Color.yellow()
            url = "https://static.wikia.nocookie.net/zenless-zone-zero/images/d/d0/Icon_AgentRank_S.png/revision/latest/scale-to-width-down/32?cb=20240914140011"
        elif a_color == True:
            rank_color = discord.Color.purple()
            url = "https://static.wikia.nocookie.net/zenless-zone-zero/images/5/5c/Icon_AgentRank_A.png/revision/latest/scale-to-width-down/32?cb=20240914135957"

        if pull_counter == 10:
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
        else:
            return

    @app_commands.command(name="info", description="Request information about gacha")
    async def info(self, interaction: discord.Interaction):

        connection = sqlite3.connect("./cogs/attempts.db")
        cursor = connection.cursor()
        guild_id = interaction.guild.id
        user_id = interaction.user.id

        cursor.execute("SELECT * FROM Gacha WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
        result = cursor.fetchone()

        if result is None:
            attempts, s_pity, a_pity, tokens = 0, 0, 0, 0
            cursor.execute("INSERT INTO Gacha (guild_id, user_id, attempts, s_pity, a_pity, tokens) VALUES (?, ?, ?, ?, ?, ?)", (guild_id, user_id, attempts, s_pity, a_pity, tokens))
        else:
            attempts, s_pity, a_pity, tokens = result[2], result[3], result[4], result[5]

        embed = discord.Embed(title="Information on the Gacha:")
        embed.add_field(name= "Rates: ", value = "S-rank: 0.6%, A-rank: 9.4%, B-rank: 90%", inline=False)
        embed.add_field(name= "Pity: ", value = f"S-rank: {s_pity}/90, A-Rank: {a_pity}/10", inline=False)
        embed.add_field(name= "/pull: " , value="Does a single pull on the gacha.", inline=False)
        embed.add_field(name= "/10pull: ", value="Does 10 consecutive pulls on the gacha.", inline=False)
        embed.add_field(name="Attempts: ", value=f"{attempts}")
        embed.add_field(name="Tokens:", value=f"{tokens}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

        connection.commit()
        connection.close()
    
    @app_commands.command(name="reset", description="Reset the user's attempts to 0, including pity.")
    @app_commands.checks.has_permissions(administrator=True)
    async def reset(self, interaction:discord.Interaction, user: discord.User):
        
        connection = sqlite3.connect("./cogs/attempts.db")
        cursor = connection.cursor()
        guild_id = interaction.guild.id
        user_id = user.id
        display_name = user.display_name
        

        cursor.execute("SELECT * FROM Gacha WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
        result = cursor.fetchone()

        if result is None or result[2] == 0:
            attempts, s_pity, a_pity, tokens = 0, 0, 0, 0
            cursor.execute("INSERT INTO Gacha (guild_id, user_id, attempts, s_pity, a_pity, tokens) VALUES (?, ?, ?, ?, ?, ?)", (guild_id, user_id, attempts, s_pity, a_pity, tokens))
            await interaction.response.send_message(f"{display_name} attempts and pity are already 0.", ephemeral=True)
        else:        
            cursor.execute("UPDATE Gacha SET attempts = 0, s_pity = 0, a_pity = 0 WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
            print("Attempts and pity reset.")
            await interaction.response.send_message(f"{display_name}'s attempts and pity have been reset to 0.", ephemeral=True)

            connection.commit()
            connection.close()

    @reset.error
    async def reset_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have the required permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)    

    @app_commands.command(name="givetoken", description="Give an user a specific number of tokens.")
    @app_commands.checks.has_permissions(administrator=True)
    async def give_token(self, interaction:discord.Interaction, user: discord.User, tokens:int):

        connection = sqlite3.connect("./cogs/attempts.db")
        cursor = connection.cursor()
        guild_id = interaction.guild.id
        user_id = user.id
        display_name = user.display_name

        cursor.execute("SELECT * FROM Gacha WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
        result = cursor.fetchone()

        if result is None and tokens >= 1:
            attempts, s_pity, a_pity = 0, 0, 0
            cursor.execute("INSERT INTO Gacha (guild_id, user_id, attempts, s_pity, a_pity, tokens) VALUES (?, ?, ?, ?, ?, ?)", (guild_id, user_id, attempts, s_pity, a_pity, tokens))
            grant_token_str = f"{tokens} " + ("tokens have" if tokens > 1 else "token has") + f" been granted to {display_name}."
            await interaction.response.send_message(grant_token_str, ephemeral=True)
        elif tokens >= 1:
            new_tokens = result[5] + tokens
            cursor.execute("UPDATE Gacha SET tokens = ? WHERE guild_id = ? AND user_id = ?", (new_tokens, guild_id, user_id))
            grant_token_str = f"{tokens} " + ("tokens have" if tokens > 1 else "token has") + f" been granted to {display_name}."
            await interaction.response.send_message(grant_token_str, ephemeral=True)

        connection.commit()
        connection.close()
        
    @give_token.error
    async def give_token_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You do not have the required permissions to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)                    

async def setup(bot):
    await bot.add_cog(Gacha(bot))