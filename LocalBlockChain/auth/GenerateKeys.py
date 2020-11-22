import cryptography, base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
    
def generate_key_pairs():

    # Generate private key 
    private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
    )

    # Generate public key
    public_key = private_key.public_key()

    # Encode private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open('private_pem.pem', 'wb') as f: f.write(private_pem)
        
    # public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('public_pem.pem', 'wb') as f: f.write(public_pem)

if __name__ == "__main__":
    generate_key_pairs()