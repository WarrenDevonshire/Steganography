# Author: Dr. Baliga

# Creating a 128 bit hash using AES in CBC mode


import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import binascii
import timeit

from cryptography.hazmat.primitives import padding
block_size = 128 # AES block size is 128 bits = 16 bytes
padder = padding.PKCS7(block_size).padder()
padded_data = padder.update(chr(0)*16)
padded_data += padder.finalize()
padded_data


unpadder = padding.PKCS7(block_size).unpadder()
data = unpadder.update(padded_data)
data += unpadder.finalize()
data


iv = os.urandom(16)
key = os.urandom(16)


def AES_CBC(iv, key, plaintext):  # AES encryption algorithm
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

    padder = padding.PKCS7(block_size).padder()
    padded_data = padder.update(plaintext)
    padded_data += padder.finalize()
    
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) 
    ciphertext += encryptor.finalize()
    return (binascii.hexlify(padded_data), binascii.hexlify(ciphertext))
    


(padded, ctext) = AES_CBC(iv, key, "The brown fox ate the ducks that were swimming in the lake") # open("/Users/baliga/Downloads/ubuntu-18.04.3-desktop-amd64.iso").read() 
print("Padded text: " + padded)
print("Ciphertext: " + ctext)
print("Hash: " + ctext[::-1][0:block_size/4]) # Hash is the final 128 bits; 32 hex digits

# Now change the first character in the plaintext
# Observe how the hash changes
(_, ctext) = AES_CBC(iv, key, "the brown fox ate the ducks that were swimming in the lake") # open("/Users/baliga/Downloads/ubuntu-18.04.3-desktop-amd64.iso").read() 
# print("Padded text: " + padded)
print("Ciphertext: " + ctext)
print("Hash: " + ctext[::-1][0:block_size/4])
