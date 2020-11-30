from Crypto.PublicKey import RSA
from base64 import b64decode
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA


def verify_sign(data, pub_key, sign):
    """Verify base64 encoded signature of string data
    with provided public RSA key.
    """
    sign = b64decode(sign)
    rsa_key = RSA.importKey(pub_key)
    hashed_data = SHA.new(data.encode())
    veryfier = PKCS1_PSS.new(rsa_key)
    if veryfier.verify(hashed_data, sign):
        return True
    return False
