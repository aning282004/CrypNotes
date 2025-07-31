from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib
import uuid

router = APIRouter()

# Simulasi user database
users_db = {}

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(data: RegisterRequest):
    if data.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Generate RSA keypair
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Encrypt private key with AES
    password_key = hashlib.sha256(data.password.encode()).digest()
    iv = get_random_bytes(16)
    cipher = AES.new(password_key, AES.MODE_CFB, iv)
    encrypted_private_key = cipher.encrypt(private_key)

    users_db[data.username] = {
        "password": hash_password(data.password),
        "public_key": public_key.decode(),
        "private_key": base64.b64encode(encrypted_private_key).decode(),
        "iv": base64.b64encode(iv).decode()
    }

    return {"message": "User registered", "public_key": public_key.decode()}

@router.post("/login")
def login(data: LoginRequest):
    user = users_db.get(data.username)
    if not user or user["password"] != hash_password(data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate dummy token (in real case, use JWT or OAuth2)
    access_token = str(uuid.uuid4())

    return {
        "message": "Login successful",
        "access_token": access_token,
        "public_key": user["public_key"],
        "encrypted_private_key": user["private_key"],
        "iv": user["iv"]
    }
