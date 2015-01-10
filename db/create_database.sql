CREATE TABLE users(
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
    );

CREATE TABLE questions(
    question_id INTEGER PRIMARY KEY,
    qustion TEXT NOT NULL,
    questions_answered INTEGER NOT NULL,
    questions_correct INTEGER NOT NULL,
    category TEXT NOT NULL
    );

CREATE TABLE categories(
    category_id INTEGER PRIMARY KEY,
    category TEXT NOT NULL
    );

CREATE TABLE answers(
    answer_id INTEGER PRIMARY KEY,
    qustion_id INTEGER NOT NULL,
    correct BOOLEAN NOT NULL,
    answer_text TEXT NOT NULL
    FOREIGN KEY(question_id) REFERENCES questions(question_id)
    );

CREATE TABLE flags(
    flag_id INTEGER PRIMARY KEY,
    question_id INTEGER NOT NULL
    FOREIGN KEY(question_id) REFERENCES questions(question_id)
    );

CREATE TABLE scores(
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    num_answered INTEGER NOT NULL,
    num_correct INTEGER NOT NULL
    PRIMARY KEY(user_id, category_id)
    FOREIGN KEY(user_id) REFERENCES users(user_id)
    FOREIGN KEY(category_id) REFERENCES categories(category_id)
    );
    
