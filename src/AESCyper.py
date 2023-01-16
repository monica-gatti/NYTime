import binascii
import uuid
from Crypto import Random
from Crypto.Cipher import AES
import os

nonce = b'\x19\x07v\x96\x80~E\xff\x94;zO\x8d\x0b\x14q'
str_key =  os.environ.get('NYTIMES_CYPHER_KEY')

def sym_encrypt(data):
    key = str_key.encode("utf-8")
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = data + (" " * (16 - (len(data) % 16)))
    return cipher.encrypt(data.encode("utf-8")).hex()

def sym_decrypt(data):
    key = str_key.encode("utf-8")
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(binascii.unhexlify(data)).decode("utf8").rstrip()

#example
# enc = sym_encrypt("ciaociao")
# print(enc)
# dec = sym_decrypt(enc)
# print(dec)
