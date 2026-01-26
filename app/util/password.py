import bcrypt


def hash_password(password: str) -> str:
    """Return a salted password hash."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Перевіряє, чи співпадає звичайний пароль із захешованим."""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())