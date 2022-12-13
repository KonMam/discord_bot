import sqlite3
from datetime import datetime as dt
from random import randint
from sqlite3 import Error

def _create_connection(db_file: str) -> sqlite3.Connection | None:
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"{dt.now().strftime('%Y-%m-%d %H:%M:%S')} INFO     Connection to Database started.")
        return conn
    except Error as e:
        print(e)
    return conn

def _get_query_results(c: sqlite3.Cursor) -> list[sqlite3.Row]:
    rows: list[sqlite3.Row] = c.fetchall()
    return rows

def execute_query(sql_query: str, quote_params: tuple = (), results: bool = False) -> list[sqlite3.Row] | None:
    conn = _create_connection("app.db")

    rows = None
    try:
        c: sqlite3.Cursor = conn.cursor()
    except Error as e:
        print(e)

    if tuple == ():
        c.execute(sql_query)
    else:
        c.execute(sql_query, quote_params)

    if results:
        rows = _get_query_results(c=c)
        return rows

    conn.close()
    print(f"{dt.now().strftime('%Y-%m-%d %H:%M:%S')} INFO     Connection to Database closed.")

def get_random_result(rows: list[sqlite3.Row] | None):
    if rows != None:
        table_size = len(rows)
        random_quote = rows[randint(0, table_size - 1)]
        return random_quote


