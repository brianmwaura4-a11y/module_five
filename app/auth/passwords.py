from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(plain: str) -> str:
    return generate_password_hash(plain)


def verify_password(plain: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, plain)
