import random
from q10 import *
from q9 import *
from collections import Counter

def is_ecb(buffer):
	ciphertext = buffer
	block_size = 16
	reps = []
	block_bytes = []
	for i in range(0,len(ciphertext), block_size):
		block_bytes = bytes(ciphertext[i:i+block_size])
		reps.append(block_bytes)

	#reps = list(map(int,reps))

	counter = Counter(reps)
	if(max(counter.values())>1):
		return 1
	else:
		return 0

def random_key(len):
	key = bytearray(random.getrandbits(8) for i in range(len))
	return key

def encryption_oracle(str):

	#Append random bytes before
	rand = random.randint(5,10)
	b = random_key(rand)
	e = random_key(rand)

	plaintext = pkcs_pad(b + str + e, AES.block_size)
	
	key = bytes(random_key(16))
	rand = random.randint(1,2)
	if (rand==1):
		return aes_128_ecb_enc(plaintext, key)
	else:
		iv = random_key(16)
		return aes_128_cbc_enc(plaintext,key,iv)

plaintext = bytearray("".join(list(open("11.txt", "r"))))
encryption_oracle(plaintext)

