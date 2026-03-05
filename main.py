import discord
import random
import aiohttp
import asyncio
import io
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()

class NikoBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents, status=discord.Status.online)
        
    async def setup_hook(self):
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}")

bot = NikoBot()

@bot.tree.command(name="ping", description="Check the bot's response time")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"Response Time: `{latency}ms`")

@bot.tree.command(name="macarena", description="Does the macarena")
async def macarena(interaction: discord.Interaction):
    await interaction.response.send_message("https://tenor.com/view/wobbly-life-macarena-dance-meme-song-gif-3201141539685971562")

meows = [
    "meow",
    "mrrp~!",
    "miau",
    "mreow",
    "<insert meow sound effect here>",
    "mrawr"
]

@bot.tree.command(name="meow", description="Meows for you :3")
async def meow(interaction: discord.Interaction):
    meowIdx = random.randint(0, len(meows)-1)
    await interaction.response.send_message(meows[meowIdx])

@bot.tree.command(name="cat", description="Get a picture of a cat")
async def cat(interaction: discord.Interaction):
    await interaction.response.defer()

    try:
        async with aiohttp.ClientSession() as session:
            timeout = aiohttp.ClientTimeout(total=10)
            async with session.get("https://cataas.com/cat", timeout=timeout) as response:
                if response.status == 200:
                    data = await response.read()
                    image_data = io.BytesIO(data)
                    picture = discord.File(image_data, filename="cat.png")
                    
                    await interaction.followup.send("Found a kitty! :3", file=picture)
                else:
                    await interaction.followup.send(f"Cat API is grumpy (Status {response.status})")
                    
    except asyncio.TimeoutError:
        await interaction.followup.send("The cat was too fast to catch! (API Timed out)")
    except Exception as e:
        print(f"Error: {e}")
        try:
            await interaction.followup.send("Something went wrong!")
        except:
            pass

bot.run(os.getenv("BOT_TOKEN"))