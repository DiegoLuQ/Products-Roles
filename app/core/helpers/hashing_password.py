from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher():
    @staticmethod
    def verify_password(normal_pass, hashed_pass):
        return pwd_context.verify(normal_pass, hashed_pass)
    
    @staticmethod
    def get_pass_hash(normal_pass):
        return pwd_context.hash(normal_pass)
    