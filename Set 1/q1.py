#QUESTION 1

def hex_to_base64(hex_code):
	
	result = hex_code.decode('hex').encode('base64')
	return result
#hex_code = raw_input('Give hex code')
hex_code ="49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
base64 = hex_to_base64(hex_code)
print base64

#QUESTION 2

def fixed_xor(s1,s2):
	return '{1:0{0}x}'.format(len(s1), int(s1, 16) ^ int(s2, 16))

s1 = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
s2 = "3"

string = fixed_xor(s1,s2)

print string




