from functions import *

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

	max_score = None
	key = None
	for guess in range(256):
		b2 = [guess] * len(bytes_at_index)
		decrypted_bytes = bytes(xor(bytes_at_index, b2))
		sc = score(decrypted_bytes)
		if(sc > max_score):
			max_score = sc
			key = chr(guess)
	keystream.append(key)

for ciphertext in ciphertexts:
	print xor(ciphertext,keystream)