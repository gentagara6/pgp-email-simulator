import os
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from typing import Optional

KEYS_DIR = Path("keys")
KEYS_DIR.mkdir(exist_ok=True)


def generate_key_pair(email: str, passphrase: Optional[str] = None):
    
    if not email or "@" not in email:
        raise ValueError("Invalid email address")

    print(f" Generating key pair for {email}...")

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )

    private_path = KEYS_DIR / f"{email}_private.pem"
    public_path = KEYS_DIR / f"{email}_public.pem"

    if passphrase:
        encryption = serialization.BestAvailableEncryption(passphrase.encode('utf-8'))
        print(" Private key protected with passphrase.")
    else:
        encryption = serialization.NoEncryption()
        print("  Warning: Private key is NOT password protected!")

    with open(private_path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=encryption,
            )
        )

    with open(public_path, "wb") as f:
        f.write(
            private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )

    print(f" Key pair generated successfully for {email}")
    return True