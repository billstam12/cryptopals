from q21 import mt_rng


def unshift_right(value, shift):
	result = 0
	for i in range(32/shift +1):
		result ^= value >>(shift*i)
	return result

def unshift_left_mask(value, shift, mask):
	result = 0 
	for i in range(32/shift + 1):
		part_mask = (0xffffffff >> (32 - shift)) << (shift * i)
		part = value & part_mask
		value ^= (part << shift) & mask
		result |= part
	return result

def untemper(y):
	value = y
	value = unshift_right(value, 18)
	value = unshift_left_mask(value, 15, 4022730752)
	value = unshift_left_mask(value, 7, 2636928640)
	value = unshift_right(value, 11)
	return value


def temper(y):
    y ^= y >> 11
    y ^= (y << 7) & 2636928640        
    y ^= (y << 15) & 4022730752
    y ^= y >> 18
    
    return y

untempered = []
rng = mt_rng(1)

for i in range(623):
	untempered.append(untemper(rng.extract_number()))


for i in range(623):
	assert rng.extract_number() == temper(untempered[i])

