from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify

private_key = RSA.generate(1024)
public_key = private_key.publickey()

private_pem = private_key.exportKey('PEM').decode()
public_pem = public_key.exportKey('PEM').decode()

with open('private_pem.pem', 'w') as pr:
    pr.write(private_pem)

with open('public_pem.pem', 'w') as pu:
    pu.write(public_pem)

pr_key = RSA.import_key(open('private_pem.pem', 'r').read())
pu_key = RSA.import_key(open('public_pem.pem', 'r').read())