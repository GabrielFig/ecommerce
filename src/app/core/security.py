from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    # Add your hashing logic here
    return "hashed_" + password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Add your verification logic here
    return hashed_password == "hashed_" + plain_password