
import os
import dotenv
import discord
from discord.ext import commands

dotenv.load_dotenv()

TOKEN = os.getenv('APP_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello World!')

bot.run(token=TOKEN)
