# The models for Trivia

import sqlite3
import db.hasher

class Model:
    """Base class for models defined in this module."""
    def __init__():
        pass

    @classmethod
    def _table_name(cls):
        """Internal use only: returns the database table name for a model class."""
        return cls.__name__.lower() + 's'

    @classmethod
    def query(cls, action, **kwargs):
        """
        Run a query with a specified action where keyword arguments are equal
        to its values, and then return an instance of 

        >>> Question.query("SELECT * FROM", question_id=1).question
        'Which house is Harry Potter in?'
        >>> User.query("SELECT * FROM", username='awesomealex').email
        'dummyemail@email.com'
        """
        table_name = cls._table_name()
        query = action.upper() + ' {0} WHERE'.format(cls._table_name())

        for key in kwargs:
            query += ' ' + key + ' = ?'
        values = tuple(kwargs.values())

        cur = conn.cursor()
        cur.execute(query, values)
        result = cur.fetchone()
        if result:
            return cls(*result)

    @classmethod
    def find(cls, **kwargs):
        """
        A shortcut for `Model.query("SELECT * FROM", **kwargs)`.

        >>> Question.find(question_id=1).question
        'Which house is Harry Potter in?'
        >>> User.find(username='awesomealex').email
        'dummyemail@email.com'
        """
        return cls.query("SELECT * FROM", **kwargs)

    @classmethod
    def delete(cls, **kwargs):
        cls.query("DELETE FROM", **kwargs)

    @classmethod
    def create():
        raise NotImplementedError()


class User(Model):
    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email

    @classmethod
    def find(cls, **kwargs):
        return cls.query("SELECT user_id, username, email FROM", **kwargs)

    def check_login(self, password):
        cur = conn.cursor()
        cur.execute('SELECT password FROM users WHERE user_id = ?', (self.id,))
        result = cur.fetchone()
        return hasher.hash(password) == result['password']

    @classmethod
    def create(cls, username, password, email):
        cur=conn.cursor()
        cur.execute('INSERT INTO users VALUES(NULL,?,?,?)',(username,hasher.hash(password),email,))
        conn.commit()
        return cls.find(user_id=cur.lastrowid)

    def set_email(self, new_email):
        cur = conn.cursor()
        cur.execute('UPDATE users SET email = ? WHERE user_id = ?', (new_email, self.id))
        self.email = self.new_email
        cur.commit()

    def set_password(self, new_password):
        cur = conn.cursor()
        cur.execute('UPDATE users SET password_hash = ? WHERE user_id = ?', (hasher.hash(password), self.id))
        cur.commit()


class TriviaQuestion(Model):
    def __init__(self, question_id, question, num_answered, num_correct, category):
        self.id = question_id
        self.question = question
        self.num_answered = num_answered
        self.num_correct = num_correct
        self.category = category

    @classmethod
    def create(cls, question, category):
        cur=conn.cursor()
        cur.execute('INSERT INTO questions VALUES(NULL,?,0,0,?)',(question,category,))
        conn.commit()
        return cls.find(question_id=cur.lastrowid)

    def flag(self):
        return Flag.create(self.id)


class Category(Model):
    def __init__(self, category_id, name):
        self.id = category_id
        self.name = name

    @classmethod
    def _table_name(cls):
        return 'categories'

    @classmethod
    def create(cls, name):
        cur=conn.cursor()
        cur.execute('INSERT INTO categories VALUES(NULL,?)',(name))
        conn.commit()
        return cls.find(category_id=cur.lastrowid)


class Flag(Model):
    def __init__(self, flag_id, question_id):
        self.id = flag_id
        self.question_id = question_id

    @classmethod
    def create(cls, question_id):
        cur=conn.cursor()
        cur.execute('INSERT INTO flags VALUES(NULL,?)',(question_id))
        conn.commit()
        return cls.find(flag_id=cur.lastrowid)


class Answer(Model):
    def __init__(self, answer_id, question_id, correct, text):
        self.id = answer_id
        self.question_id = question_id
        self.correct = correct
        self.text = text

    @classmethod
    def create(cls, answer_id, question_id, correct, text):
        cur=conn.cursor()
        cur.execute('INSERT INTO answers VALUES(NULL,?)',(name))
        conn.commit()
        return cls.find(answer_id=cur.lastrowid)

    @classmethod
    def delete_by_id(cls, answer_id):
        raise NotImplementedError()


class Score(Model):
    def __init__(self, user_id, category_id, num_answered, num_correct):
        self.user_id = user_id
        self.category_id = category_id
        self.num_answered = num_answered
        self.num_correct = num_correct

    @classmethod
    def create(cls, user_id, category_id):
        raise NotImplementedError()


conn = sqlite3.connect('db/trivia.db')
conn.row_factory = sqlite3.Row
