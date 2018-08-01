from q11 import random_key, is_ecb
from q10 import *
from q9 import *

key = bytes(random_key(16))

def get_block_size(oracle):
    ciphertext_length = len(oracle)
    i = 1
    while True:
        data = bytearray("A" * i)
        new_ciphertext_length = len(encryption_oracle(data))
        block_size = new_ciphertext_length - ciphertext_length
        if block_size:
            return block_size
        i += 1

def get_unknown_string_size(oracle):
    ciphertext_length = len(encryption_oracle(bytearray()))
    i = 1
    while True:
        data = bytearray("A" * i)
        new_ciphertext_length = len(encryption_oracle(data))
        if ciphertext_length != new_ciphertext_length:
            return new_ciphertext_length - i
        i += 1

def decrypt_ecb_string(oracle):
	block_size = get_block_size(oracle)

	input_block = random_key(block_size - 1)

	uk_string_size = get_unknown_string_size(oracle)
	rounded_size = (((uk_string_size / block_size) + 1) * block_size)
	unknown_string = bytearray()

	for i in range(rounded_size-1, 0,-1):
		d1 = bytearray('A'*i)
		c1 = encryption_oracle(d1)[:rounded_size]

		for c in range(256):
			d2 = d1[:] + unknown_string + chr(c)
			c2  = encryption_oracle(d2)[:rounded_size]
			if c1 == c2:
				unknown_string += chr(c)
				break
	return unknown_string

def encryption_oracle(data):
	unknown_string = bytearray((
        "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\n" +
        "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\n" +
        "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\n" +
        "YnkK").decode("base64"))

	plaintext = pkcs_pad(data +unknown_string, AES.block_size)

	return aes_128_ecb_enc(plaintext, key)

#print decrypt_ecb_string(encryption_oracle(""))
