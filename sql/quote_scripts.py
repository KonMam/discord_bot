sql_create_quote_table = """
    CREATE TABLE IF NOT EXISTS quotes (
        name text NOT NULL,
        quote text NOT NULL,
        date text NOT NULL
    )"""

sql_insert_quote = """
        INSERT INTO quotes(name, quote, date)
        VALUES(?, ?, ?)
    """

sql_get_all_quotes = """SELECT * FROM quotes"""