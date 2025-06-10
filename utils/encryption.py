# =============================================================== #
# ===================== utils/encryption.py ===================== #
# --------------------------------------------------------------- #
# 📌 Purpose   : Encrypt and decrypt sensitive PII fields
# 🔐 Tech      : Symmetric encryption using Fernet (AES-128 under the hood)
# ✅ Used by   : Tools, DB inserts, or memory storage if needed
# =============================================================== #

from cryptography.fernet import Fernet
import os

# =============================================================== #
# ======================== ENCRYPTION KEY ======================= #
# =============================================================== #
# NOTE: In production, load from secrets manager or .env securely
FERNET_KEY = os.environ.get("FERNET_KEY", Fernet.generate_key().decode())

fernet = Fernet(FERNET_KEY.encode())

# =============================================================== #
# ======================== ENCRYPT FUNCTION ===================== #
# =============================================================== #
def encrypt_data(plain_text: str) -> str:
    """
    Encrypt a string using Fernet encryption.

    Args:
        plain_text (str): Sensitive data to encrypt

    Returns:
        str: Encrypted string
    """
    if not plain_text:
        return ""
    return fernet.encrypt(plain_text.encode()).decode()

# =============================================================== #
# ======================== DECRYPT FUNCTION ===================== #
# =============================================================== #
def decrypt_data(encrypted_text: str) -> str:
    """
    Decrypt an encrypted string using Fernet.

    Args:
        encrypted_text (str): Cipher text to decrypt

    Returns:
        str: Original plain text
    """
    if not encrypted_text:
        return ""
    return fernet.decrypt(encrypted_text.encode()).decode()

# =============================================================== #
# ======================== END OF FILE ========================== #
# =============================================================== #