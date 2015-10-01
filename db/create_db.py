#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect('trivia.db')
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS users""")
cur.execute("""DROP TABLE IF EXISTS questions""")
cur.execute("""DROP TABLE IF EXISTS categories""")
cur.execute("""DROP TABLE IF EXISTS answers""")
cur.execute("""DROP TABLE IF EXISTS flags""")
cur.execute("""DROP TABLE IF EXISTS scores""")
cur.execute("""DROP TABLE IF EXISTS games""")

with open('schema.sql') as f:
    cur.executescript(f.read())

conn.commit()
