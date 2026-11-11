import base64
import hashlib
from typing import Optional
from cryptography.fernet import Fernet
from app.core.config import settings

def _get_fernet_key() -> bytes:
    raw_key = settings.DATA_ENCRYPTION_KEY.encode()
    digest = hashlib.sha256(raw_key).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt_clinical_note(plain_text: Optional[str]) -> Optional[str]:
    """
    Encrypts sensitive clinical notes before writing to database (AES-256 via Fernet).
    """
    if plain_text is None or plain_text == "":
        return plain_text
    f = Fernet(_get_fernet_key())
    encrypted = f.encrypt(plain_text.encode("utf-8"))
    return encrypted.decode("utf-8")

def decrypt_clinical_note(encrypted_text: Optional[str]) -> Optional[str]:
    """
    Decrypts sensitive clinical notes when reading from database.
    """
    if encrypted_text is None or encrypted_text == "":
        return encrypted_text
    try:
        f = Fernet(_get_fernet_key())
        decrypted = f.decrypt(encrypted_text.encode("utf-8"))
        return decrypted.decode("utf-8")
    except Exception:
        return encrypted_text

def hash_password(password: str) -> str:
    """
    Basic deterministic hash with salt for demonstration/PoC.
    """
    salt = "mindful_ai_salt"
    return hashlib.sha256((password + salt).encode()).hexdigest()
