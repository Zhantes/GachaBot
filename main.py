import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print("An error with syncing application commands has occurred: ", e)

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

load_dotenv()
TOKEN: str = os.getenv("TOKEN")
async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)

asyncio.run(main())