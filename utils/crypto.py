from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import hashlib
## utils/crypto_6.py（鍵ペア生成＋署名）::250618_19_15
def generate_keys(output_folder):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # Save private key
    priv_path = f"{output_folder}/private_key.pem"
    with open(priv_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Save public key
    pub_path = f"{output_folder}/public_key.pem"
    with open(pub_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    return private_key, public_key

def sign_pdf(private_key, pdf_path, signature_path):
    with open(pdf_path, "rb") as f:
        data = f.read()

    hash_value = hashlib.sha256(data).digest()

    signature = private_key.sign(
        hash_value,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    with open(signature_path, "wb") as f:
        f.write(signature)

    return hash_value, signature