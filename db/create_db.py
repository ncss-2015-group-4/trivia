import sqlite3

conn = sqlite3.connect('trivia.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
    );""")

cur.execute("""CREATE TABLE IF NOT EXISTS questions(
    question_id INTEGER PRIMARY KEY,
    question TEXT NOT NULL,
    questions_answered INTEGER NOT NULL,
    questions_correct INTEGER NOT NULL,
    category TEXT NOT NULL
    );""")    

cur.execute("""CREATE TABLE IF NOT EXISTS categories(
    category_id INTEGER PRIMARY KEY,
    category TEXT NOT NULL
    );""")

cur.execute("""CREATE TABLE IF NOT EXISTS answers(
    answer_id INTEGER PRIMARY KEY,
    question_id INTEGER NOT NULL,
    correct BOOLEAN NOT NULL,
    answer_text TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions (question_id)
    );""")

cur.execute("""CREATE TABLE IF NOT EXISTS flags(
    flag_id INTEGER PRIMARY KEY,
    question_id INTEGER NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions (question_id)
    );""")

cur.execute("""CREATE TABLE IF NOT EXISTS scores(
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    num_answered INTEGER NOT NULL,
    num_correct INTEGER NOT NULL,
    PRIMARY KEY(user_id, category_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (category_id) REFERENCES categories (category_id)
    );""")
