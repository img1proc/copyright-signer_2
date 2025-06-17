from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import os

def generate_keys(output_dir):
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key = private_key.public_key()

    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, "private_key.pem"), "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(os.path.join(output_dir, "public_key.pem"), "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    return private_key, public_key


def sign_pdf(private_key, pdf_path, sig_path):
    with open(pdf_path, "rb") as f:
        data = f.read()

    from hashlib import sha256
    hash_value = sha256(data).digest()

    signature = private_key.sign(
        hash_value,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    with open(sig_path, "wb") as f:
        f.write(signature)

    return hash_value.hex(), signature