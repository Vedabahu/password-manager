import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from db import DataBaseHandler


class Crypto:
    def __init__(self, verification: bool = True):
        db = DataBaseHandler()
        self.__salt = "Oh My Gawd!!, I am Vedabahu!!!".encode()
        if verification:
            self.__key = db.get_key()

        # For the key derivation function
        self.__algorithm = hashes.SHA256()
        self.__length = 64
        self.__iterations = 1_200_000

    def generate_verification_key_from_master_password(
        self, master_password: str
    ) -> bytes:
        """Generates a key from the master password using PBKDF2.

        Args:
            master_password (str): The master password.

        Returns:
            bytes: The derived key.
        """
        kdf = PBKDF2HMAC(
            algorithm=self.__algorithm,
            length=self.__length,
            salt=self.__salt,
            iterations=self.__iterations,
        )
        return kdf.derive(master_password.encode())

    def verify_master_password_from_key(self, master_password: str) -> bool:
        """Verifies the master password against the derived key.

        Args:
            master_password (str): The master password.

        Returns:
            bool: True if the master password is correct, False otherwise.
        """
        try:
            kdf = PBKDF2HMAC(
                algorithm=self.__algorithm,
                length=self.__length,
                salt=self.__salt,
                iterations=self.__iterations,
            )
            kdf.verify(master_password.encode(), self.__key)
            return True
        except Exception:
            return False

    def encrypt_username_password(
        self, username: str, password: str, master_password: str
    ) -> tuple[bytes, bytes]:
        """Encrypts the username and password using Fernet symmetric encryption.

        Args:
            username (str): The username to encrypt.
            password (str): The password to encrypt.

        Returns:
            tuple[bytes, bytes]: The encrypted username and password.
        """
        kdf = Argon2id(
            salt=self.__salt,
            length=32,
            iterations=5,
            lanes=4,
            memory_cost=8 * 4 * 1024,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

        f = Fernet(key)
        encrypted_username = f.encrypt(username.encode())
        encrypted_password = f.encrypt(password.encode())

        return (encrypted_username, encrypted_password)
