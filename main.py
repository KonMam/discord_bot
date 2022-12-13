from datetime import date
import os

import discord
import dotenv
from discord.ext import commands

from utils.db import execute_query, get_random_result
from sql.quote_scripts import sql_create_quote_table, sql_insert_quote, sql_get_all_quotes

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

    quote_params = (member.name, quote, date.today().strftime("%d/%m/%Y"))

    execute_query(sql_query=sql_insert_quote, query_params=quote_params)

    msg = f'**"{quote}"**    - *{member}, {date.today().strftime("%d/%m/%Y")}*'
    await ctx.send(msg)

@bot.command(name='random_quote')
async def random_quote(ctx):

    rows = execute_query(sql_query=sql_get_all_quotes, results=True)
    random_quote = get_random_result(rows=rows)
    
    msg = f'**"{random_quote[2]}"**    - *{random_quote[1]}, {random_quote[3]}*'
    await ctx.send(msg)


def main():
    # Checks if quote table exists, if not creates one
    execute_query(sql_query=sql_create_quote_table)
    # Starts the bot
    bot.run(token=TOKEN)

main()
