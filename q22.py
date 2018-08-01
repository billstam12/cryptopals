from q21 import mt_rng
import time
from time import sleep
from random import randint

seed = time.time()
def routine():
	sleep(randint(40,1000))
	global seed

	rng = mt_rng(int(seed)).extract_number()

	sleep(randint(40,1000))
	print rng 

def crack():
	rand_int = routine()
	current_time = int(time.time())
	for seed in range(current_time, current_time - 2500, -1):
		my_num = mt_rng(int(seed)).extract_number()
		if(rand_int == my_num):
			return seed
	raise Exception("Failed to crack seed")

print crack()
