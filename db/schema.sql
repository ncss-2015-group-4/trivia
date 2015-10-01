CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    salt TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE questions (
    question_id INTEGER PRIMARY KEY,
    question TEXT NOT NULL,
    questions_answered INTEGER NOT NULL,
    questions_correct INTEGER NOT NULL,
    category TEXT NOT NULL,
    difficulty REAL NOT NULL
);

CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY,
    category TEXT UNIQUE NOT NULL
);

CREATE TABLE answers (
    answer_id INTEGER PRIMARY KEY,
    question_id INTEGER NOT NULL,
    correct BOOLEAN NOT NULL,
    answer_text TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions (question_id)
);

CREATE TABLE flags (
    flag_id INTEGER PRIMARY KEY,
    question_id INTEGER NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions (question_id)
);

CREATE TABLE scores (
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    num_answered INTEGER NOT NULL,
    num_correct INTEGER NOT NULL,
    PRIMARY KEY (user_id, category_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (category_id) REFERENCES categories (category_id)
);

CREATE TABLE games (
    game_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    questions TEXT NOT NULL,
    question_index INTEGER NOT NULL,
    time_started INTEGER NOT NULL,
    time_completed INTEGER,
    difficulty REAL NOT NULL,
    category_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (category_id) REFERENCES categories (category_id)
);

CREATE TABLE questionresults (
    game_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    answer_id INTEGER,
    correct BOOLEAN,
    PRIMARY KEY (game_id, question_id, user_id),
    FOREIGN KEY (game_id) REFERENCES games (game_id),
    FOREIGN KEY (question_id) REFERENCES questions (question_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (answer_id) REFERENCES answers (answer_id)
);
