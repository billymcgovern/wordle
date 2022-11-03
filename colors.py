_RESET = '\u001b[0m'

class Color(object):
	def __init__(self, color_code):
		self.color_code = color_code

	def __call__(self, text):
		return self.color_code + text + _RESET
		
BOLD = Color('\u001b[1m')
GREY = Color('\u001b[2m')
FLASHING = Color('\u001b[5m')
RED = Color('\u001b[91m')
GREEN = Color('\u001b[92m')
YELLOW = Color('\u001b[93m')
WHITE_GREEN_BACKGROUND = Color('\u001b[42m')
WHITE_YELLOW_BACKGROUND = Color('\u001b[43m')

def print_colors():
	for i in range(1, 107):
		code = f'\u001b[{i}m'
		color = Color(code)
		print(color('[' + code[2:] + '] ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

