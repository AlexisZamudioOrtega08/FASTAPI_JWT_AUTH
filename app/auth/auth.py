from fastapi import Security, HTTPException
from jose import JWTError, jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os


class AuthHandler:
    security = HTTPBearer()

    def __init__(self):
        path_dotenv = "../.env"
        while os.getenv("SECRET") == None:
            load_dotenv(path_dotenv)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret = os.getenv("SECRET")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=1),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except JWTError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
