from q9 import *
from q10 import *
from q11 import random_key, is_ecb
from Crypto.Cipher import AES
from q15 import pkcs_unpad_2

key = bytes(random_key(AES.block_size))
iv = bytearray(random_key(AES.block_size))


def encryption_oracle(input_data):
	input_data = input_data.replace(';','%3b').replace('=', '%3d')
	plaintext = pkcs_pad("comment1=cooking%20MCs;userdata=" + input_data + ";comment2=%20like%20a%20pound%20of%20bacon", AES.block_size)
	return aes_128_cbc_enc(plaintext, key, iv)

def find_admin(ciphertext):
	plaintext = aes_128_cbc_dec(ciphertext,key,iv)
	return "admin=true;" in plaintext

def get_admin():
	dummy_block = bytearray('A'* AES.block_size)
	crack_block = pkcs_pad(bytearray("AadminAtrueA"), AES.block_size)

	plaintext = dummy_block + crack_block
	ciphertext = encryption_oracle(plaintext)

	# Below i do the following,
	# Xor the ciphertext dummy bits with the xor I want. That way the cbc 1 bit error will change
	# the value of the next block too.
	ciphertext[32] = bytes(xor(bytearray(chr(ciphertext[32])), xor(bytearray("A"), bytearray(";"))))
	ciphertext[38] = bytes(xor(bytearray(chr(ciphertext[38])), xor(bytearray("A"), bytearray("="))))
	ciphertext[43] = bytes(xor(bytearray(chr(ciphertext[43])), xor(bytearray("A"), bytearray(";"))))

	print ciphertext
	print find_admin(ciphertext)

#1st question
#print find_admin(encryption_oracle("admin=true;"))

def main():
	get_admin()


if __name__ == "__main__":
	main()