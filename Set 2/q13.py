from q9 import *
from q10 import *
from q11 import random_key, is_ecb
from q12 import *
key = bytes(random_key(AES.block_size))

uid = 0
def k_v_routine(str):
	obj  = {}
	for kv in str.split('&'):
		kv = kv.split("=")
		obj[kv[0]] = kv[1]
	return obj

def profile_for(email):
	email = email.replace("&","").replace("=","")
	profile = "email=" + email + "&uid=10&role=user"

	padded_buffer = bytes(pkcs_pad(bytearray(profile), AES.block_size))
	return aes_128_ecb_enc(padded_buffer, key) 

def profile_dec(buffer):
	return bytes(pkcs_unpad(aes_128_ecb_dec(buffer, key)))

def get_admin():
	block_size =  get_block_size(profile_for(""))
	mandatory_bytes = "email=&uid=10&role="
	remaining_bytes = (len(mandatory_bytes) / block_size + 1) * block_size
	email_len = remaining_bytes - len(mandatory_bytes)
	email = "A" * email_len
	profile_prefix = profile_for(bytearray(email))[:remaining_bytes]

	mandatory_bytes = "email="
	remaining_bytes = (len(mandatory_bytes) / block_size + 1) * block_size
	email_len = remaining_bytes - len(mandatory_bytes)
	email = "A" * email_len
	email += pkcs_pad("admin", block_size)
	profile_postfix = profile_for(email)[
		remaining_bytes:remaining_bytes + block_size
	]

	profile = profile_prefix + profile_postfix
	print bytes(profile_dec(profile))

print k_v_routine(profile_dec(profile_for("billstam12@gmail.com&role=admin")))


get_admin()