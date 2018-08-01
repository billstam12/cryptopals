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

def main():
	s1 = "vasilis stamatopoulos"
	print len(s1)
	print pkcs_pad(s1,20)
	print pkcs_unpad(s1)

