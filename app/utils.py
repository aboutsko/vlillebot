UPDATE_FILE = './.update'

def get_last_update():
	with open(UPDATE_FILE, 'r') as update_file:
		try:
			last_update = int(update_file.read())
		except ValueError:
			last_update = 0
		return last_update
	
def set_last_update(last_update):
	with open(UPDATE_FILE, 'w') as update_file:
		update_file.write(str(last_update))
		