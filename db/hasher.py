import hashlib, binascii, os

def hash(password, salt):
	return binascii.hexlify(hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 5000)).decode()

def new_salt():
	return binascii.hexlify(os.urandom(50)).decode()