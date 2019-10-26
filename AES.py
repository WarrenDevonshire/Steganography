# Author: Dr. Baliga

import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import binascii

backend = default_backend()  # Provides primitives for operating the ciphers
key_size = 128  # AES can operate with different key sizes. We use 128 bit = 16 bytes
block_size = 128  # AES block size is 128
key = os.urandom(key_size // 8)  # Create a random key. NOTE: os.urandom uses analog sources to generate random bits
initializationvec = os.urandom(16)  # Used for CBC cipher mode

cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
# cipher = Cipher(algorithms.AES(key), modes.CBC(initializationvec), backend=backend)


encryptor = cipher.encryptor()
plaintext = (chr(0) * 16).encode()
ciphertext = encryptor.update(plaintext)
decryptor = cipher.decryptor()
decryptedtext = decryptor.update(ciphertext)
decryptedtext == plaintext
print(binascii.hexlify(plaintext), binascii.hexlify(ciphertext))


def AES(key, plaintext):  # AES encryption algorithm
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    block_size = 128
    if len(plaintext * 8) % block_size != 0:
        print(len(plaintext))
        print ("Plain text must be a multiple of %s" % (block_size))
        return
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext)
    decryptor = cipher.decryptor()
    decryptedtext = decryptor.update(ciphertext)

    # Pad with 0's at left to make output 128 bits
    pt = format(int(binascii.hexlify(plaintext), 16), 'b')
    pt_padded = "0" * (len(plaintext) * 8 - len(pt)) + pt

    ct = format(int(binascii.hexlify(ciphertext), 16), 'b')
    ct_padded = "0" * (len(ciphertext) * 8 - len(ct)) + ct

    return (pt_padded, ct_padded)


(p1, c1) = AES(key, ((chr(0)) * 16).encode())  # Plaintext is 16 bytes, all 0

print ("Plaintext bits: " + p1)
print ("Ciphertext bits: " + c1)

print;
print;

(p2, c2) = AES(key, ((chr(0)) * 15 + chr(1)).encode())  # Plaintext is 16 bytes, 15 all 0, 16th byte value is 1
print ("Plaintext bits: " + p2)
print ("Ciphertext bits: " + c2)

print("Difference: %d positions out of %d" % (len([i for i in range(len(c1)) if c1[i] != c2[i]]), len(c1)))
