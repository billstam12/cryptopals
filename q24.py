from q21 import mt_rng
from functions import random_key
from random import randint
def trivial_keystream_generator(seed):
	prng = mt_rng(seed)
	while True:
		yield prng.extract_number() % pow(2, 8)

def xor(b1,b2):
	b = bytearray()
	for byte in b1:
		b.append(byte ^ b2.next())
	return b 

def encrypt(plaintext, seed):
	ciphertext = xor(plaintext, trivial_keystream_generator(seed))
	return ciphertext

plaintext = random_key(randint(0, 256)) + bytearray(["A"] * 14)
seed = randint(0, pow(2,16))
ciphertext = encrypt(plaintext, seed)
