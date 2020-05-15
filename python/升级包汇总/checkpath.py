import os

def CheckifExists(path):
	if os.path.exists(path):
		return True
	return False