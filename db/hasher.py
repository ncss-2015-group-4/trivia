import hashlib, binascii

def hash(password):
	return binascii.hexlify(hashlib.pbkdf2_hmac('sha256', password.encode(), b'SALT_XYZ_YOLO', 5000))
