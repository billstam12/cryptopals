plaintext = "billstam12@gmail.com"
key = "ICE"
b1 = bytearray(plaintext)
b2 = bytearray(key)

flag = 0 
b = bytearray(len(b1))
for i in range(len(b1)):

	b[i] = b1[i] ^ b2[flag]
	flag +=1
	if(flag==2):
		flag = 0

import binascii
b = binascii.hexlify(bytearray(b))
print b