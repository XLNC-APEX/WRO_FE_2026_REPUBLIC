

def get_wait(cw: bool, right: float, left: float):
	if cw:
		dist = left
	else:
		dist = right
	wt = dist * 0.7
	return wt;
