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



def hash_password(string):
    raise NotImplementedError()
    return string

    

    
        
