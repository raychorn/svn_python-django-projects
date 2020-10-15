def prettySize(size):
	suffixes = [("B",2**10), ("K",2**20), ("M",2**30), ("G",2**40), ("T",2**50)]
	for suf, lim in suffixes:
		if size > lim:
			continue
		else:
			return round(size/float(lim/2**10),2).__str__()+suf

if (__name__ == '__main__'):
	print prettySize(213458923)
	# Output: 203.57M
	
	print prettySize(1234)
	# Output: 1.21K
