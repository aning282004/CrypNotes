# routes/crypto_api.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from base64 import b64encode, b64decode
from Crypto.Random import get_random_bytes

router = APIRouter()

# === Request Schemas ===

class AESRequest(BaseModel):
    plaintext: str
    key: str  # base64 encoded key

class AESDecryptRequest(BaseModel):
    ciphertext: str
    key: str
    iv: str

class RSAEncryptRequest(BaseModel):
    plaintext: str
    public_key: str  # PEM format

class RSADecryptRequest(BaseModel):
    ciphertext: str
    private_key: str  # PEM format

class SignRequest(BaseModel):
    message: str
    private_key: str  # PEM

class VerifyRequest(BaseModel):
    message: str
    signature: str
    public_key: str  # PEM

# === AES ENCRYPTION ===

@router.post("/encrypt_aes")
def encrypt_aes(data: AESRequest):
    key = b64decode(data.key)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    ciphertext = cipher.encrypt(data.plaintext.encode())
    return {
        "ciphertext": b64encode(ciphertext).decode(),
        "iv": b64encode(iv).decode()
    }

@router.post("/decrypt_aes")
def decrypt_aes(data: AESDecryptRequest):
    key = b64decode(data.key)
    iv = b64decode(data.iv)
    cipher = AES.new(key, AES.MODE_CFB, iv)
    plaintext = cipher.decrypt(b64decode(data.ciphertext))
    return {"plaintext": plaintext.decode()}

# === RSA ENCRYPTION ===

@router.post("/encrypt_rsa")
def encrypt_rsa(data: RSAEncryptRequest):
    pubkey = RSA.import_key(data.public_key.encode())
    cipher = PKCS1_OAEP.new(pubkey)
    ciphertext = cipher.encrypt(data.plaintext.encode())
    return {"ciphertext": b64encode(ciphertext).decode()}

@router.post("/decrypt_rsa")
def decrypt_rsa(data: RSADecryptRequest):
    privkey = RSA.import_key(data.private_key.encode())
    cipher = PKCS1_OAEP.new(privkey)
    plaintext = cipher.decrypt(b64decode(data.ciphertext))
    return {"plaintext": plaintext.decode()}

# === SIGNATURE ===

@router.post("/sign")
def sign(data: SignRequest):
    privkey = RSA.import_key(data.private_key.encode())
    h = SHA256.new(data.message.encode())
    signature = pkcs1_15.new(privkey).sign(h)
    return {"signature": b64encode(signature).decode()}

@router.post("/verify")
def verify(data: VerifyRequest):
    pubkey = RSA.import_key(data.public_key.encode())
    h = SHA256.new(data.message.encode())
    try:
        pkcs1_15.new(pubkey).verify(h, b64decode(data.signature))
        return {"valid": True}
    except (ValueError, TypeError):
        return {"valid": False}
