import colors
import argparse
import random

from enum import Enum, unique

LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


@unique
class State(Enum):
	NOT_GUESSED = -1
	INCORRECT = 0
	CORRECT = 1
	WRONG_POS = 2


class Word(object):
	def __init__(self, word):
		self.word = word
		self.letters = []
		for l in word:
			self.letters.append(Letter(l))
	
	def check(self, other):
		incorrect_letters = []
		correct_letters = []
		for idx, letter in enumerate(self.letters):
			if letter != other.letters[idx]:
				eq = False
				if letter in other.letters:
					num_total = other.letters.count(letter)
					num_actual = correct_letters.count(letter)
					if num_actual < num_total:
						letter.state = State.WRONG_POS
					else:
						letter.state = State.INCORRECT
				else:
					letter.state = State.INCORRECT
					incorrect_letters.append(letter)
			else:
				letter.state = State.CORRECT
				correct_letters.append(letter)
		return incorrect_letters
		

	def __eq__(self, other):
		return self.word == other.word


class Letter(object):
	def __init__(self, letter):
		self.letter = letter.lower()
		self.state = State.NOT_GUESSED
	
	def __str__(self):
		letter = f' {self.letter} '
		if State.INCORRECT == self.state:
			return colors.BOLD(colors.GREY(letter))
		elif State.CORRECT == self.state:
			return colors.BOLD(colors.WHITE_GREEN_BACKGROUND(letter))
		elif State.WRONG_POS == self.state:
			return colors.BOLD(colors.WHITE_YELLOW_BACKGROUND(letter))
		else:
			return '   '

	def __eq__(self, other):
		return self.letter == other.letter


class Board(object):
	def __init__(self, word, word_list, max_guesses):
		self.word = Word(word)
		self.word_list = word_list
		self.guesses = []
		self.blank_guess = Word(' ' * len(self.word.letters))
		self.num_guesses = 0
		self.max_guesses = max_guesses
		self.incorrect_letters = []

	def __str__(self):
		if not self.guesses:
			return self.str_guess(self.blank_guess, print_bottom=True)
		else:
			out = ''
			for guess in self.guesses[:-1]:
				out += self.str_guess(guess)
			out += self.str_guess(self.last_guess, print_bottom=True)
		if self.incorrect_letters:
			out += ', '.join(colors.BOLD(colors.GREY(il)) for il in self.incorrect_letters)
			out += '\n'
		out += ', '.join(letter.lower() for letter in LETTERS if letter.lower() not in self.incorrect_letters)
		out += '\n'
		
		return out

	def str_guess(self, guess, print_bottom=False):
		rows = ('*---' * len(self.word.letters)) + '*'
		columns = ''
		for letter in guess.letters:
			columns += '|{}'.format(str(letter))
		columns += '|'

		row = rows + '\n' + columns + '\n'
		if print_bottom:
			row += rows + '\n'
		return row

	@property
	def last_guess(self):
		return self.guesses[-1]

	def guess(self, word):
		self.guesses.append(Word(word))

		incorrect_letters = self.last_guess.check(self.word)
		for letter in incorrect_letters:
			if letter.letter not in self.incorrect_letters:
				self.incorrect_letters.append(letter.letter)

		if self.last_guess == self.word:
			return True
		return False

	def play(self):
		while self.num_guesses < self.max_guesses:
			print(str(self))
			guess = input('guess > ')
			if len(guess) > len(self.word.word):
				print(colors.BOLD(colors.RED('Word too long')))
				continue
			elif len(guess) < len(self.word.word):
				print(colors.BOLD(colors.RED('Word not long enough')))
				continue
			if guess not in self.word_list:
				print(colors.BOLD(colors.RED('Word not in word list')))
				continue
			self.num_guesses += 1
			if self.guess(guess):
				print(str(self))
				print(colors.FLASHING(colors.BOLD(colors.GREEN('WIN!'))))
				return True
		print(str(self))
		print(colors.BOLD(colors.RED('LOSER!')))
		print(f'The word was: {colors.BOLD(self.word.word)}')


def choose_word(path):
	words = []
	with open(path, 'r') as file:
		[words.append(word.strip('\n')) for word in file.readlines()]
	return words[random.randint(0, len(words) - 1)], words


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('word_file', type=str)
	parser.add_argument('--num_guesses', type=int, default=5)
	pargs = parser.parse_args()
	
	word, word_list = choose_word(pargs.word_file)
	board = Board(word, word_list, pargs.num_guesses)
	try:
		board.play()
	except KeyboardInterrupt:
		return
	
if __name__ == '__main__':
	main()
