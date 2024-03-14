import bcrypt


def get_hashed_password(plain_text_password):
    plain_text_password_bytes = str.encode(plain_text_password)
    return bcrypt.hashpw(plain_text_password_bytes, bcrypt.gensalt())


def verify_password(plain_text_password, hashed_password):
    plain_text_password_bytes = str.encode(plain_text_password)
    return bcrypt.checkpw(plain_text_password_bytes, hashed_password)
