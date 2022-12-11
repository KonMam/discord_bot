
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
        print(f"Connection to Database started {date.today()}.")
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
        INSERT INTO quotes(name, quote, date)
        VALUES(?, ?, ?)
    """
    c = conn.cursor()
    c.execute(sql_insert_quote, quote_params)
    conn.commit()
    return c.lastrowid

def get_random_quote(conn):
    sql_get_quotes = """SELECT * FROM quotes"""
    c: sqlite3.Cursor = conn.cursor()
    c.execute(sql_get_quotes)
    row = c.fetchall()[0]
    return row


sql_create_quote_table = """
    CREATE TABLE IF NOT EXISTS quotes (
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

    quote_params = (member.name, quote, date.today().strftime("%d/%m/%Y"))

    if conn is not None:
        create_table(conn, sql_create_quote_table)
        create_quote(conn, quote_params)
        conn.close()
        print(f'Connection to Database closed {date.today()}.')

    msg = f'{quote} -{member}, {date.today().strftime("%d/%m/%Y")}'
    await ctx.send(msg)

@bot.command(name='random_quote')
async def random_quote(ctx):
    conn = create_connection("app.db")

    if conn is not None:
        create_table(conn, sql_create_quote_table)
        row = get_random_quote(conn)
        conn.close()
        print(f'Connection to Database closed {date.today()}.')
    
    msg = f'{row.quote} -{row.name}, {row.date}'
    await ctx.send(msg)



bot.run(token=TOKEN)
