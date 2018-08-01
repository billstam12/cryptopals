from functions import *
from Crypto.Cipher import AES
from struct import pack

def aes_ctr_dec(ciphertext, key, nonce):
	counter = 0
	plaintext = bytearray(len(ciphertext))
	for i in range(0,len(ciphertext), AES.block_size):
		keystream = aes_128_ecb_enc(bytearray(pack('<Q', nonce)) + bytearray(pack('<Q', counter)),key)
		plaintext[i:i+AES.block_size] = xor(bytearray(ciphertext[i:i+AES.block_size]),keystream)
		counter +=1
	return plaintext



def aes_ctr_enc(plaintext, key, nonce):
	counter = 0
	ciphertext = bytearray(len(plaintext))
	for i in range(0,len(plaintext), AES.block_size):
		keystream = aes_128_ecb_enc(bytearray(pack('<Q', nonce)) + bytearray(pack('<Q', counter)),key)
		ciphertext[i:i+AES.block_size] = xor(plaintext[i:i+AES.block_size],keystream)
		counter +=1
	return ciphertext

ciphertext = bytearray("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==").decode("base64")
print ciphertext
key = "YELLOW SUBMARINE"
plaintext =  aes_ctr_dec(ciphertext, key, 0 )
ciphertext = aes_ctr_enc(plaintext, key, 0)

print plaintext
print ciphertext