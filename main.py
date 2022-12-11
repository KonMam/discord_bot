
import os
from datetime import date
import sqlite3
from sqlite3 import Error

import discord
import dotenv
from discord.ext import commands

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
	    print(e)

def create_quote(conn, quote_params):
    sql_insert_quote = """
        INSERT INTO quotes(id, name, quote, date)
        VALUES(?, ?, ?, ?)
    """
    c = conn.cursor()
    c.execute(sql_insert_quote, quote_params)
    c.commit()
    return c.lastrowid

sql_create_quote_table = """
    CREATE TABLE IF NOT EXISTS quotes (
        id integer PRIMARY KEY,
        name text NOT NULL,
        quote text NOT NULL,
        date text NOT NULL)
    """


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
    conn = create_connection("app.db")
    quote_params = (0, member, quote, date.today().strftime("%d/%m/%Y"))
    
    if conn is not None:
        create_table(conn, sql_create_quote_table)
        create_quote(conn, quote_params)
        conn.close()

    msg = f'{quote} -{member}, {date.today().strftime("%d/%m/%Y")}'
    await ctx.send(msg)


bot.run(token=TOKEN)
