from collections import Counter
#What i did was cycle through each ciphertext and break it into blocks.
#After that, I initialized a reps array for each text and in that i stored
#the bytes in their corresponding index. If they had much of the same blocks
#they probably where ECB
counts = []
for ciphertext in list(open("8.txt","r")):
	ciphertext = ciphertext.rstrip()
	ba = bytearray(ciphertext)
	block_size = 16
	reps = []
	block_bytes = []
	for i in range(0,len(ba), block_size):
		block_bytes = bytes(ba[i:i+block_size])
		reps.append(block_bytes)

	#reps = list(map(int,reps))
	counter = Counter(reps)
	print counter.values()
	counts.append((len(counter),ciphertext))

print min(counts)






# block_size = 16
# 	reps = []
# 	for i in range(0,len(ba), block_size):
# 		block_bytes = (ba[i:i+block_size])
		
# 		reps.append(block_bytes)

# 	reps = list(map(int,reps))
# 	print reps
# 	break