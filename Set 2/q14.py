from q11 import random_key, is_ecb
from q10 import *
from q9 import *
import random
key = bytes(random_key(16))
random_prefix = bytes(random_key(random.randint(0,255)))

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

def get_random_prefix_size(oracle,block_size):
	for size in range(block_size):
		reps = 10
		my_block = bytearray("A" * size)
		buffer = encryption_oracle(my_block + bytearray("YELLOW SUBMARINE" * reps))
		prev_block = None
		count = 0 
		index = 0  
		for i in range(0, len(buffer), block_size):
			block = buffer[i:i+block_size]
			if (prev_block == block):
				count +=1
			else:
				index = i
				prev_block = block
				count = 1
			if count == reps:
				return index, size
	
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

	prefix_index, prefix_padding_size =  get_random_prefix_size(oracle,block_size)
	prefix_size = prefix_index - prefix_padding_size
	uk_string_size = get_unknown_string_size(oracle) - prefix_size
	rounded_size = (((uk_string_size / block_size) + 1) * block_size)
	unknown_string = bytearray()

	for i in range(rounded_size-1, 0,-1):
		d1 = bytearray('A'*(i +prefix_padding_size))
		c1 = encryption_oracle(d1)[prefix_index:rounded_size+prefix_index]

		for c in range(256):
			d2 = d1[:] + unknown_string + chr(c)
			c2  = encryption_oracle(d2)[prefix_index:prefix_index + rounded_size]
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

	plaintext = pkcs_pad(random_prefix + data + unknown_string, AES.block_size)
	return aes_128_ecb_enc(plaintext, key)

def main():
	print decrypt_ecb_string(encryption_oracle(""))


if __name__ == '__main__':
	main()