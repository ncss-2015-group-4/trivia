# The models for Trivia

class User:
    def __init__(self, _id, username, password_hash, email):
        self.id = _id
        self.username = username
        self.password = password_hash

    def authenticate(username, password):
        raise NotImplementedError()
        return False
    
    @classmethod
    def find_by_id(cls, id):
        raise NotImplementedError()
        return cls()

    @classmethod
    def find_by_username(cls, username):
        raise NotImplementedError()
        return cls(0, username, "pw", "email")

    @classmethod
    def create(cls, username, password, email):
        #get id from sql?
        _id = 0
        raise NotImplementedError()
        return cls(_id, username, hash_password(password), email)

    @classmethod
    def delete_by_id(cls, id):
        raise NotImplementedError()
        #DELETE ROW WHERE id = ?

        return True

    @classmethod
    def delete_by_username(cls, username):
        raise NotImplementedError()
        #DELETE ROW WHERE username = ?
        return True


class TriviaQuestion:
    def __init__(self, id, question, num_answered, num_correct, category_id):
        self.id = id
        self.question = question
        self.num_answered = num_answered
        self.num_correct = num_correct
        self.category_id = category_id

    @classmethod
    def create(cls, question, category):
        raise NotImplementedError
        # num_answered = 0
        # num_correct = 0
        ...
        return cls(qid, question, 0, 0, category)

    def flag(self):
        return Flag.create(self.id)


class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name):
        raise NotImplementedError
        ...
        return cls(cid, name)


class Flag:
    def __init__(self, id, question_id):
        self.id = id
        self.question_id = question_id

    @classmethod
    def find_by_id(cls, id):
        raise NotImplementedError()

    @classmethod
    def create(cls, question_id):
        raise NotImplementedError()


class Answer:
    def __init__(self, answer_id, question_id, correct, text):
        self.id = answer_id
        self.question_id = question_id
        self.correct = correct
        self.text = text

    @classmethod
    def create(cls, answer_id, question_id, correct, text):
        raise NotImplementedError()

    @classmethod
    def find_by_id(cls, answer_id):
        raise NotImplementedError()

    @classmethod
    def delete_by_id(cls, answer_id):
        raise NotImplementedError()


def hash_password(string):
    raise NotImplementedError()
    return string

    

    
 
