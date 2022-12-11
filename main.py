
import os
import dotenv
import discord
from discord.ext import commands

dotenv.load_dotenv()

TOKEN = os.getenv('APP_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='info')
async def member_info(ctx, member: discord.Member):
    msg = f'{member} joined on {member.joined_at.date} and has {len(member.roles)} role.'
    await ctx.send(msg)

@bot.command(name='find')
async def find_member(ctx, name: str):
    match_list: list[str] = []

    for guild in bot.guilds:
        print(guild)
        for member in guild.members:
            # if name in member.name:
            #     match_list.append(member)
            # else:
            print(member)
    if len(match_list) > 0:
        await ctx.send([(x + ', ') for x in match_list])
    else:
        await ctx.send('User not found.')



bot.run(token=TOKEN)
