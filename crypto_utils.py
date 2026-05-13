import os
import base64
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from typing import Optional
from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidSignature

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

def load_private_key(email):

    with open(f"keys/{email}_private.pem", "rb") as f:

        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )


def load_public_key(email):

    with open(f"keys/{email}_public.pem", "rb") as f:

        return serialization.load_pem_public_key(
            f.read()
        )


def encrypt_and_sign(
    message,
    sender_email,
    receiver_email
):

    sender_private_key = load_private_key(sender_email)

    receiver_public_key = load_public_key(receiver_email)

    symmetric_key = Fernet.generate_key()

    fernet = Fernet(symmetric_key)

    encrypted_message = fernet.encrypt(
        message.encode()
    )

    encrypted_symmetric_key = receiver_public_key.encrypt(
        symmetric_key,

        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),

            algorithm=hashes.SHA256(),

            label=None
        )
    )

    signature = sender_private_key.sign(
        encrypted_message,

        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),

            salt_length=padding.PSS.MAX_LENGTH
        ),

        hashes.SHA256()
    )

    package = {

        "encrypted_key":
        base64.b64encode(
            encrypted_symmetric_key
        ).decode(),

        "encrypted_message":
        base64.b64encode(
            encrypted_message
        ).decode(),

        "signature":
        base64.b64encode(
            signature
        ).decode()
    }

    return package


def decrypt_and_verify(
    package,
    receiver_email,
    sender_email
):

    receiver_private_key = load_private_key(
        receiver_email
    )

    sender_public_key = load_public_key(
        sender_email
    )

    encrypted_key = base64.b64decode(
        package["encrypted_key"]
    )

    encrypted_message = base64.b64decode(
        package["encrypted_message"]
    )

    signature = base64.b64decode(
        package["signature"]
    )

    try:

        sender_public_key.verify(
            signature,

            encrypted_message,

            padding.PSS(
                mgf=padding.MGF1(
                    hashes.SHA256()
                ),

                salt_length=padding.PSS.MAX_LENGTH
            ),

            hashes.SHA256()
        )

    except InvalidSignature:

        raise Exception(
            "Signature verification failed."
        )

    symmetric_key = receiver_private_key.decrypt(

        encrypted_key,

        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),

            algorithm=hashes.SHA256(),

            label=None
        )
    )

    fernet = Fernet(symmetric_key)

    decrypted_message = fernet.decrypt(
        encrypted_message
    ).decode()

    return decrypted_message