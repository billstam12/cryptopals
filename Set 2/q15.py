from Crypto.Cipher import AES
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

#pkcs_unpad(bytearray("ICE ICE BABY\x04\x04\x04\x04"))
