from functions import *
import numpy as np 

ciphertexts = []
key = bytes(random_key(AES.block_size))
FIXED_NONCE = 0

for encoded_plaintext in list(open("19.txt", "r")):
	plaintext = bytearray(encoded_plaintext).decode("base64")
	plaintext = pkcs_pad(plaintext, AES.block_size)
	#print plaintext
	ciphertexts.append(aes_ctr_enc(plaintext, key, FIXED_NONCE))


keystream = bytearray()
max_length = max(map(len, ciphertexts))

bbs = []
for i in range(max_length):
	# Here I want to create arrays with the bytes at each index from each ciphertext
	bytes_at_index = map(ord, filter(lambda x:x, map(lambda x:x[i:i+1],ciphertexts)))

	#pad bytes at index to max length
	bytes_at_index = bytes_at_index[:max_length] + [0] * (max_length - len(bytes_at_index))
	bbs.append(bytes_at_index)

bbs = np.array(bbs)
key = None
bbs[:,1] ^= ord("I")
bbs[:,1] ^= 32

for b in bbs:
	st  = "".join(map(chr,b))
	print st.encode("utf-8")
#for ciphertext in ciphertexts:
	#print xor(ciphertext,keystream)