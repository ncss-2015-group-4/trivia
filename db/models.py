# The models for Trivia

import sqlite3
import random
import time

from . import hasher

class Model:
    """Base class for models defined in this module."""

    def __init__():
        pass

    @classmethod
    def _table_name(cls):
        """Internal use only: returns the database table name for a model class."""
        return cls.__name__.lower() + 's'

    @classmethod
    def _id_field(cls):
        """Internal: returns the correct id field of the model's table."""
        return cls.__name__.lower() + '_id'

    @classmethod
    def _query(cls, action, single=True, **kwargs):
        """
        Execute a query against the class' database table (given by
        `cls._table_name()`) of a specified action (e.g. `SELECT columns`,
        `DELETE`) where each keyword argument is treated as a corresponding
        field, value pair in the table, returning results as necessary.

        If 'id' is given as a field name, it is translated to the correct id
        field of the table, for example, `user_id` for the users table.

        If single is True (default), returns the first row from the database.
        Otherwise, returns a list of all the matching rows.

        NB: This should not be called directly outside of any Model class,
        consider using the find* methods instead.

        >>> Question._query("SELECT question", question_id=1)['question']
        'Which house is Harry Potter in?'
        >>> Question._query("SELECT question", id=1)['question']
        'Which house is Harry Potter in?'
        >>> User._query("SELECT email", username='awesomealex')['email']
        'dummy@example.com'
        """ 

        query = '{0} FROM {1}'.format(action, cls._table_name())
        if kwargs:
            query += ' WHERE ' + ' AND '.join((cls._id_field() if key == 'id' else key) + ' = ?' for key in kwargs)
        values = tuple(kwargs.values())

        cur = conn.cursor()
        cur.execute(query, values)

        if single:
            return cur.fetchone()

        return cur.fetchall()

    @classmethod
    def find(cls, **kwargs):
        """
        A shortcut for `Model(*Model._query("SELECT *", **kwargs))`.

        >>> Question.find(question_id=1).question
        'Which house is Harry Potter in?'
        """

        row = cls._query("SELECT *", **kwargs)
        if row:
            return cls(*row)

    @classmethod
    def delete_where(cls, **kwargs):
        cls._query("DELETE", **kwargs)

    def delete(self):
        self.delete_where(id=self.id)

    @classmethod
    def find_all(cls, **kwargs):
        return [cls(*row) for row in cls._query("SELECT *", single=False, **kwargs)]

    @classmethod
    def create():
        raise NotImplementedError()


class User(Model):
    """
    A model representing a user in the database.

    Properties:
    * id       - the user's unique ID
    * username - the user's username
    * email    - the user's email address

    Methods:
    * user.check_login(password)
    * user.set_email(new_email)
    * user.set_password(new_password)

    Class methods:
    * User.create(username, password, email)
    * User.find(**kwargs)
    """

    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email

    @classmethod
    def find(cls, **kwargs):
        """
        Find and return a user where the kwargs match their records.

        >>> User.find(username='awesomealex').email
        'dummyemail@email.com'
        >>> User.find(user_id=1).username
        'awesomealex'
        """

        row = cls._query("SELECT user_id, username, email", **kwargs)
        if row:
            return cls(*row)

    def check_login(self, password):
        """Check whether a provided password is the user's password."""
        cur = conn.cursor()
        cur.execute('SELECT password, salt FROM users WHERE user_id = ?', (self.id,))
        result = cur.fetchone()
        return hasher.hash(password, result['salt']) == result['password']

    @classmethod
    def create(cls, username, password, email):
        """
        Create a user in the database with the given username, password, and email.

        Example: User.create('drowsydavid', 'lol', 'devnull@vovo')
        """

        salt = hasher.new_salt()
        cur=conn.cursor()
        cur.execute('INSERT INTO users VALUES(NULL,?,?,?,?)',(username,hasher.hash(password, salt)
                                                            ,salt,
                                                            email,))
        conn.commit()
        return cls(cur.lastrowid,username,email)

    def set_email(self, new_email):
        """
        Set a user's email address in the database.

        >>> user = User.find(username='fantasticfeddy')
        >>> user.email
        'dummyemail1@email.com'
        >>> user.set_email('feddie@example.com')
        >>> user.email
        'feddie@example.com'
        """

        cur = conn.cursor()
        cur.execute('UPDATE users SET email = ? WHERE user_id = ?', (new_email, self.id))
        self.email = new_email
        conn.commit()

    def set_password(self, new_password):
        """
        Set a user's password in the database.

        >>> user = User.find(username='awesomealex')
        >>> user.check_login('password')
        True
        >>> user.set_password('helloworld')
        >>> user.check_login('password')
        False
        >>> user.check_login('helloworld')
        True
        >>> user.set_password('password')
        """

        salt = hasher.new_salt()
        cur = conn.cursor()
        cur.execute('UPDATE users SET password = ?, salt = ? WHERE user_id = ?', (hasher.hash(new_password, salt), salt, self.id))
        conn.commit()


class Question(Model):
    """
    A model representing trivia questions in the database.

    Properties:
    * id           - the question's unique ID
    * question     - the question text
    * questions_answered - the number of times the question has been answered
    * questions_correct  - the number of times the question has been answered correctly

    Methods:
    * question.flag()
    * question.get_answers()

    Class methods:
    * Question.create(question_text, category_id)
    """

    def __init__(self, question_id, question, questions_answered, questions_correct, category, difficulty):
        self.id = question_id
        self.question = question
        self.questions_answered = questions_answered
        self.questions_correct = questions_correct
        self.category = category
        self.difficulty = difficulty

    @classmethod
    def create(cls, question, category_id):
        cur=conn.cursor()
        cur.execute('INSERT INTO questions VALUES(NULL,?,0,0,?,0)', (question, category_id))
        conn.commit()
        return cls(cur.lastrowid, question, 0, 0, category_id, 0)

    def flag(self):
        return Flag.create(self.id)

    def get_answers(self):
        return Answer.find_all(question_id=self.id)


class Category(Model):
    """
    A model that represents a category in the database.

    Properties:
    * id   - the unique category ID
    * name - the category name

    Class methods:
    * Category.create(category_name)
    """

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
        return cls(cur.lastrowid,name)

    def create_question(self, question, answers):
        question = Question.create(question, self.id)
        for index, answer in enumerate(answers):
            if index == 0:
                Answer.create(question.id, 1, answer)
            else:
                Answer.create(question.id, 0, answer)
        return question


class Flag(Model):
    """
    A model that represents a flag on a Question.

    Properties:
    * id          - the unique flag ID
    * question_id - the ID of the question flagged

    Class method:
    * Flag.create(question_id)
    """

    def __init__(self, flag_id, question_id):
        self.id = flag_id
        self.question_id = question_id

    @classmethod
    def create(cls, question_id):
        cur=conn.cursor()
        cur.execute('INSERT INTO flags VALUES(NULL,?)',(question_id,))
        conn.commit()
        return cls(cur.lastrowid,question_id)


class Answer(Model):
    """Q
    A model that represents an answer for a Question.

    Properties:
    * id          - the unique answer ID
    * question_id - the question ID
    * correct     - True if the answer is the correct answer, False otherwise.
    * text        - the answer text

    Class methods:
    * Answer.create(answer_id, question_id, correct, text)
    """

    def __init__(self, answer_id, question_id, correct, text):
        self.id = answer_id
        self.question_id = question_id
        self.correct = correct
        self.text = text

    @classmethod
    def create(cls, question_id, correct, text):
        cur=conn.cursor()
        cur.execute('INSERT INTO answers VALUES(NULL,?,?,?)',(question_id,correct,text))
        conn.commit()
        return cls(cur.lastrowid, question_id, correct, text)


class Score(Model):
    """
    A model that represents the score of a User in a certain Category.

    Properties:
    * user_id      - the user's ID
    * category_id  - the category ID
    * questions_answered - the number of questions the user has answered
    * questions_correct  - the number of questions the user answered correctly
    """

    def __init__(self, user_id, category_id, num_answered, num_correct):
        self.user_id = user_id
        self.category_id = category_id
        self.num_answered = num_answered
        self.num_correct = num_correct

    @classmethod
    def create(cls, user_id, category_id):
        cur=conn.cursor()
        cur.execute('INSERT INTO scores VALUES(?,?,0,0)',(user_id,category_id))
        conn.commit()
        return cls(user_id,category_id,0,0)

    def update_score(self,correct_answer):
        if correct_answer:
            self.num_correct += 1
        self.num_answered += 1
        cur = conn.cursor()
        cur.execute('UPDATE scores SET num_answered=?,num_correct=? WHERE user_id=? AND category_id=?', (self.num_answered, self.num_correct, self.user_id, self.category_id))
        conn.commit()

class QuestionResult(Model):
    """
    A model that represents a single user's answers to the questions in a single game.

    Properties:
    * game_id     - the id of the Game the user played
    * question_id - the question the user answered
    * user_id     - the id of the user that answered (perhaps multiple users can play a game in future)
    * answer_id   - the answer the user selected (either correctly or incorrectly)
    * correct     - whether the answer was correct or not (mostly for convenience)
    """

    def __init__(self, game_id, question_id, user_id, answer_id, correct):
        self.game_id = game_id
        self.question_id = question_id
        self.user_id = user_id
        self.answer_id = answer_id
        self.correct = correct

    @classmethod
    def create(cls, game_id, question_id, user_id, answer_id, correct):
        cur = conn.cursor()
        cur.execute('INSERT INTO questionresults VALUES(?, ?, ?, ?, ?)',
                (game_id, question_id, user_id, answer_id, correct))
        conn.commit()
        return cls(game_id, question_id, user_id, answer_id, correct)

    def question(self):
        """Returns the question object that represents the question asked."""
        return Question.find(question_id=self.question_id)

    def users_answer(self):
        """Returns the Answer object that the user selected."""
        return Answer.find(answer_id=self.answer_id)

    def correct_answer(self):
        """Returns the Answer object for the correct answer to the question."""
        return Answer.find(question_id=self.question_id, correct=True)

class Game(Model):
    """
    A model that represents a Game that a user is/was playing

    Properties:
    * id                - the games id
    * user_id           - the user id
    * time_started      - when the game started
    * time_completed    - when the game finished
    * difficulty        - what difficulty the game is
    * category_id       - what category the game is in
    * score             - the current score in the game
    """
    def __init__(self, game_id, user_id, question_ids, question_index, time_started, time_completed, difficulty, category_id, score):
        self.id = game_id
        self.user_id = user_id
        if isinstance(question_ids, str):
            question_ids = [int(x) for x in question_ids.split(',')]
        self.question_ids = question_ids
        self.question_index = question_index
        self.time_started = time_started
        self.time_completed = time_completed
        self.difficulty = difficulty
        self.category_id = category_id
        self.score = score

    @classmethod
    def create(cls, user_id, category_id, difficulty, n=5):
        cur=conn.cursor()
        question_ids = []
        for row in cur.execute('SELECT question_id FROM questions WHERE category = ? AND difficulty =?', (category_id, difficulty)):
            question_ids.append(row["question_id"])

        if not question_ids:
            return None

        random.shuffle(question_ids)
        question_ids = question_ids[:n]
        print("number of questions generated: " + str(len(question_ids)))

        cur.execute('INSERT INTO games VALUES(NULL, ?, ?, 0, ?, 0, ?, ?, 0)',(user_id, ','.join(map(str, question_ids)), time.time(),category_id, difficulty))
        conn.commit()
        return cls(cur.lastrowid, user_id, question_ids, 0, time.time(), 0, difficulty, category_id, 0)


    def submit_answer(self, question_id, answer_id):
        cur=conn.cursor()
        correct = 0
        question = Question.find(question_id=question_id)
        answer = Answer.find(answer_id=answer_id)
        if question and answer:
            if question.id == answer.question_id:
                if answer.correct:
                    correct = 1
                    cur.execute('UPDATE games SET score = score + 1 WHERE game_id = ?',(self.id,))
                    self.score += 1
                    print("SCORE INCREMENTED")
                else:
                    print("answer:",answer)
                question_result = QuestionResult.create(self.id, question_id, self.user_id, answer_id, correct)
                cur.execute('UPDATE questions SET questions_answered = questions_answered + 1, questions_correct = questions_correct + ? WHERE question_id = ?',
                                (correct, question_id))
                conn.commit()
                
                return correct
        return False

    def get_question_results(self):
        """Returns the list of results for each question answered."""
        # TODO: Make this the same order as the questions were asked (currently random order)
        # We probably need to store the index in the db as well.
        results = QuestionResult.find_all(game_id=self.id)
        return results

    def get_questions(self):
        questions = []
        for id in self.question_ids:
            questions.append(Question.find(question_id=id))

        return questions

    def get_question(self, index):
        print(repr(self.question_ids), index)
        current_question_id = self.question_ids[index]
        print(current_question_id)
        question = Question.find(question_id=current_question_id)

        return question

    def game_nextquestion(self):
        cur=conn.cursor()
    
        cur.execute('UPDATE games SET question_index = question_index + 1 WHERE game_id=?',(self.id,))
        self.question_index += 1
        conn.commit()
        return self.score

conn = sqlite3.connect('db/trivia.db')
conn.row_factory = sqlite3.Row
