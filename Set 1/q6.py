import base64
import numpy as np
from q3 import xor, score, break_single_key_xor

def hamming_distance(s1,s2):
	diffs = 0.0
	for byte in xor(s1,s2):
		diffs += bin(byte).count("1")
	return diffs

def main2():
	s1 = "this is a test"
	s2 = "wokka wokka!!!"
	s1 = s1.encode('hex')
	s2 = s2.encode('hex')
	print hamming_distance(s1,s2)


def main():
	b = bytearray("".join(list(open("6.txt", "r"))).decode("base64"))
	dists = []
	for keysize in range(2,40):
		distances = []
		chunks = [b[i:i+keysize] for i in range(0, len(b),keysize)]
		for i in range(6):
			
			chunk1 = chunks[i]
			chunk2 = chunks[i+1]
			dist = hamming_distance(chunk1,chunk2)
			distances.append(dist/keysize)

		fin_dist = 0
		if(len(distances)!=0):
			fin_dist = sum(distances)/ len(distances)
		
		dists.append((keysize, fin_dist))
	dists = sorted(dists, key = lambda (_,y):y)

	for keysize, _ in dists[:5]:
		block_bytes = [[] for _ in range(keysize)]

		for i, byte in enumerate(b):
			block_bytes[i % keysize].append(byte)

		keys = ""
		for bbytes in block_bytes:
			keys += break_single_key_xor(bbytes)[0]
		#print keys, key= Terminator X: Bring the noise

	key = bytearray("Terminator X: Bring the noise"* len(b))
	plaintext = bytes(xor(b, key))
	print plaintext

if __name__ =='__main__':
	main()

