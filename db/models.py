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
    def __init__(self, id, question, num_answered, num_correct, category):
        self.id = id
        self.question = question
        self.num_answered = num_answered
        self.num_correct = num_correct
        self.category = category

    @classmethod
    def create(cls, question, category):
        raise NotImplementedError
        # num_answered = 0
        # num_correct = 0
        ...
        return cls(qid, question, 0, 0, category)


class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name):
        raise NotImplementedError
        ...
        return cls(cid, name)


def hash_password(string):
    raise NotImplementedError()
    return string

    

    
 
