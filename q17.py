from functions import *
from random import choice

strings = ["MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"]



def encryption_oracle():
	global key 
	key = bytes(random_key(AES.block_size))
	string = choice(strings)
	iv = bytearray(random_key(AES.block_size))

	return aes_128_cbc_enc(pkcs_pad(string, AES.block_size),key, iv), iv

def decrypt(enc, iv):
	plaintext = aes_128_cbc_dec(enc, key, iv)
	try:
		pkcs_unpad_2(plaintext)
		return True
	except:
		return False

def crack_block(block,iv):
	plaintext_block = bytearray()
	start_guess = 0
	while len(plaintext_block) < AES.block_size: # Increment until we have created the plaintext block
		for guess in range(start_guess, 256): 
			padding = len(plaintext_block) + 1
			corrupted_iv = bytearray(iv)
			for byte in range(1, padding + 1):
				if byte < padding:
					corrupted_iv[-byte] =  bytes(xor(xor(bytearray([iv[-byte]]), bytearray(chr(plaintext_block[-byte]))),bytearray(chr(padding))))
				else:
					corrupted_iv[-byte] =  bytes(xor(xor(bytearray([iv[-byte]]), bytearray(chr(guess))),bytearray(chr(padding))))

		if(decrypt(block,corrupted_iv)):
			plaintext_block = bytearray(chr(guess))
			start_guess = 0
			break
		else:
			try:
				start_guess = int(plaintext_block[0]) + 1
				plaintext_block = plaintext_block[1:]
			except:
				return bytearray()
		return plaintext_block

def crack(ciphertext, iv):
	ciphertext = iv + ciphertext
	plaintext = ''
	for i in range(len(ciphertext) / AES.block_size):
        # We only really need to pass two blocks to the padding oracle...
        # The block to the decrypt, and the one before it which we corrupt
		plaintext += crack_block(
			ciphertext[(i + 1) * AES.block_size: (i + 2) * AES.block_size],
			ciphertext[i * AES.block_size: (i + 1) * AES.block_size]
		)


cipher,iv = encryption_oracle()
plaintext = crack(cipher, iv)




