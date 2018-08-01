import random
from Crypto.Cipher import AES
from struct import pack

def score(s):
    freq = {}
    freq[' '] = 700000000
    freq['e'] = 390395169
    freq['t'] = 282039486
    freq['a'] = 248362256
    freq['o'] = 235661502
    freq['i'] = 214822972
    freq['n'] = 214319386
    freq['s'] = 196844692
    freq['h'] = 193607737
    freq['r'] = 184990759
    freq['d'] = 134044565
    freq['l'] = 125951672
    freq['u'] = 88219598
    freq['c'] = 79962026
    freq['m'] = 79502870
    freq['f'] = 72967175
    freq['w'] = 69069021
    freq['g'] = 61549736
    freq['y'] = 59010696
    freq['p'] = 55746578
    freq['b'] = 47673928
    freq['v'] = 30476191
    freq['k'] = 22969448
    freq['x'] = 5574077
    freq['j'] = 4507165
    freq['q'] = 3649838
    freq['z'] = 2456495
    score = 0
    for c in s.lower():
        if c in freq:
            score += freq[c]
    return score
def random_key(len):
	key = bytearray(random.getrandbits(8) for i in range(len))
	return key

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

    
def pkcs_pad(buffer, block_size):
    if len(buffer) % block_size:
        padding = (len(buffer) / block_size + 1) * block_size - len(buffer)
    else:
        padding = 0
    # Padding size must be less than a byte
    assert 0 <= padding <= 255
    new_buffer = bytearray()
    new_buffer[:] = buffer
    new_buffer += bytearray([chr(padding)] * padding)
    return new_buffer

def pkcs_unpad(buffer):
    padding = buffer[-1]
    for i in range(len(buffer) - 1, len(buffer) - padding - 1, -1):
        if buffer[i] != buffer[-1]:
            return buffer
    new_buffer = bytearray()
    new_buffer[:] = buffer[:-padding]
    return new_buffer

def pkcs_unpad_2(buffer):
    padding = buffer[-1]
    if padding >= AES.block_size:
    	return buffer
    for i in range(len(buffer) - 1, len(buffer) - padding - 1, -1):
    	if buffer[i] != buffer[-1]:
    		raise Exception("Bad PKCS#7 padding")

    new_buffer = bytearray()
    new_buffer[:] = buffer[:-padding]
    return new_buffer

def aes_ctr_dec(ciphertext, key, nonce):
    counter = 0
    plaintext = bytearray(len(ciphertext))
    for i in range(0,len(ciphertext), AES.block_size):
        keystream = aes_128_ecb_enc(bytearray(pack('<Q', nonce)) + bytearray(pack('<Q', counter)),key)
        plaintext[i:i+AES.block_size] = xor(bytearray(ciphertext[i:i+AES.block_size]),keystream)
        counter +=1
    return pkcs_unpad(plaintext)



def aes_ctr_enc(plaintext, key, nonce):
    counter = 0
    ciphertext = bytearray(len(plaintext))
    for i in range(0,len(plaintext), AES.block_size):
        keystream = aes_128_ecb_enc(bytearray(pack('<Q', nonce)) + bytearray(pack('<Q', counter)),key)
        ciphertext[i:i+AES.block_size] = xor(plaintext[i:i+AES.block_size],keystream)
        counter +=1
    return ciphertext
