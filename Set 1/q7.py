from Crypto.Cipher import AES

b = ("".join(list(open("7.txt", "r"))).decode("base64"))

key = "YELLOW SUBMARINE"
cipher = AES.new(key, AES.MODE_ECB)

msg = cipher.decrypt(b)
print msg
