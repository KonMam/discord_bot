
import os
from datetime import date

import discord
import dotenv
from discord.ext import commands

dotenv.load_dotenv()

TOKEN = os.getenv('APP_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='info')
async def member_info(ctx, member: discord.Member):
    msg = f'{member} joined on {member.joined_at.date()} and has {len(member.roles)} roles.'
    await ctx.send(msg)

@bot.command(name='find')
async def find_member(ctx, name: str):
    match_list: list[str] = []

    if name == "*":
        for guild in bot.guilds:
            for member in guild.members:
                match_list.append(member.display_name)
            else:
                pass

    else:
        for guild in bot.guilds:
            for member in guild.members:
                if name in member.name:
                    match_list.append(member.display_name)
                else:
                    pass

    if len(match_list) > 0:
        await ctx.send(", ".join(match_list))
    else:
        await ctx.send('User not found.')

@bot.command(name='quote')
async def quote(ctx, member:discord.Member, quote):
    msg = f'{quote} -{member}, {date.today().strftime("%d/%m/%Y")}'
    await ctx.send(msg)


bot.run(token=TOKEN)
