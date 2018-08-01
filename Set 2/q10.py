from q9 import pkcs_pad, pkcs_unpad
from Crypto.Cipher import AES

def xor(b1, b2):
    b = bytearray(len(b1))
    for i in range(len(b1)):
        b[i] = b1[i] ^ b2[i]
    return b

def aes_128_ecb_enc(b,key):
	cipher = AES.new(key, AES.MODE_ECB)
	return bytearray(cipher.encrypt(bytes(b)))

def aes_128_ecb_dec(b,key):
	cipher = AES.new(key, AES.MODE_ECB)
	return bytearray(cipher.decrypt(bytes(b)))


def aes_128_cbc_enc(b,key,iv):
	plaintext = pkcs_pad(b, AES.block_size)
	ciphertext = bytearray(len(plaintext))
	prev_block = iv
	for i in range(0,len(plaintext), AES.block_size):
		ciphertext[i:i+AES.block_size] = aes_128_ecb_enc(xor(plaintext[i:i+AES.block_size],prev_block),key)
		prev_block = ciphertext[i:i+AES.block_size]
	return ciphertext

def aes_128_cbc_dec(ciphertext,key,iv):
	plaintext = bytearray(len(ciphertext))
	prev_block = iv
	for i in range(0,len(ciphertext), AES.block_size):
		plaintext[i:i+AES.block_size] = xor(aes_128_ecb_dec(bytes(ciphertext[i: i + AES.block_size]), key),prev_block)
		prev_block = ciphertext[i:i+AES.block_size]
	return pkcs_unpad(plaintext)

def main():
		
	ciphertext = bytearray("".join(list(open("10.txt", "r"))).decode("base64"))
	iv = bytearray([chr(0)]*AES.block_size)
	key = "YELLOW SUBMARINE"

	print aes_128_cbc_dec(ciphertext,key,iv)



