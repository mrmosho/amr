import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

class EncryptionModule:
    def __init__(self, key: bytes = None):
        if key is None:
            key = Fernet.generate_key()
        self.key = key
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, data: str) -> str:
        """Encrypt the given data using Fernet symmetric encryption."""
        return self.cipher_suite.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt the given encrypted data using Fernet symmetric encryption."""
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()

    @staticmethod
    def derive_key(password: str, salt: bytes = None) -> bytes:
        """Derive a key from a password using PBKDF2."""
        if salt is None:
            salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key 