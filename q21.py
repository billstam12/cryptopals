import time

N = 624

class mt_rng(object):
	global N
	def __init__(self, seed = time):
		self.state = [0] * N
		self.n = 1812433253
		self.m = 397
		self.u = 11
		self.s = 7
		self.b = 0x9D2C5680
		self.t = 15
		self.c = 0xEFC60000
		self.l = 18
		self.index = N
		self.lower_mask = (1<<31)-1
		self.upper_mask = 1<<31

		self.state[0] = seed
		for i in range(1,N):
			self.state[i] = self.int_32(self.n*(self.state[i-1] ^ (self.state[i-1]>>30)) + i)

	def extract_number(self):
		if self.index >= N:
			self.twist()
		y = self.state[self.index]
		y = y^(y>>self.u)
		y = y^((y<<self.s)&self.b)
		y = y^((y<<self.t)&self.c)
		y = y^(y>>self.l)
		self.index+=1
		return self.int_32(y)

	def twist(self):
		for i in range(N):
			x = self.int_32(self.state[i] & self.upper_mask) + (self.state[(i+1)%N]&self.lower_mask)
			x_a = x >> 1
			if ((x % 2) !=0):
				x_a ^= 0x9908b0df
			self.state[i] = self.state[(i + self.m) % N] ^ x_a
		self.index = 0
	
	def int_32(self, number):
		return int(0xFFFFFFFF & number)


