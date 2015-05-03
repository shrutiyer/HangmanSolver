"""dis be da ai fo da list, mon"""
import sets
from collections import Counter
from time import time

word_list = [line.strip() for line in open("words.txt", 'r')]
word_set = set(word_list)

tile = ['p']
tile = [tile[0].upper()]
inventory = ['a','t','w','l','p','p','i']
word = 'apple'
location = (2,3)

points = {'A':1,'B':3,'C':3, 'D':2, 
            'E':1, 'F': 4, 'G':2, 'H':4, 
            'I': 1,'J':8, 'K': 5, 'L': 1,
            'M':3, 'N':1, 'O':1, 'P':3,
            'Q':10, 'R':1, 'S':1, 'T':1,
            'U':1,'V':4, 'W':4, 'X':8,
            'Y':4,'Z':10}

def stepone(tile,inventory,word):
	"""figures out if the word can be made given the letter and inventory"""
	letterstock = tile + inventory
	listed_word = list(word)
	return not Counter(listed_word)-Counter(inventory)

def steptwo(tile,inventory):
	"""makes a list of all possible words that can be made"""
	possible_words = []
	for word in word_set:
		if stepone(tile,inventory,word) == True:
			possible_words.append(word.upper())
	return possible_words
	
def cleaner(tile,possible_words):
	"""removes all word that don't contain the tile in them"""
	cleaned_list = []
	for word in possible_words:
		if tile[0] in word:
			cleaned_list.append(word)
	return cleaned_list

def splitter(tile,word):
	"""splits the word at the tile"""
	temp = list(word)
	index = temp.index(tile[0])
	return (''.join(temp[:index]),''.join(temp[index+1:]))

def split_list(tile, possible_words):
	"""splits the list of possible words into tuples
		you need to clean the possible words first"""
	tuplist = []
	for word in possible_words:
		tuplist.append(splitter(tile,word))
	return tuplist

def checker(tile, tuplewear, tile_spaces):
	"""checks to see if you can actually put a word there
		tuplewear = the tuple from split_list"""
	if len(tuplewear[0]) <= tile_spaces[0]:
		if len(tuplewear[1]) <= tile_spaces[1]:
			return tuplewear[0] + tile[0] + tuplewear[1]
		else:
			return False
	else:
		return False

def check_list(tile, tuplist, tile_spaces):
	"""cheks to see if the words in the list are ok"""
	ok_list=[]
	for element in tuplist:
		ok_list.append(checker(tile[0],element,tile_spaces))
	return ok_list

def clean_list(ok_list):
	"""gets rid of the false's in the list"""
	cleaned_list = []
	for word in ok_list:
		if word != False:
			cleaned_list.append(word)
	return cleaned_list

def get_score(word):
	"""uses a dict to get the score"""
	score = 0
	for letter in word:
		score += points[letter]
	return score

def score_list(cleaned_list):
	"""prints the highest scoring word in the list"""
	scores = []
	for word in cleaned_list:
		score=get_score(word)
		scores.append((score,word))
	return max(scores)

# def overall(tile,inventory,location):
# 	wordlist = steptwo(tile,inventory)
# 	print word_list
# 	wordlist = cleaner(tile,wordlist)
# 	print wordlist
# 	tuplist = split_list(tile,wordlist)
# 	print tuplist
# 	checked_list = check_list(tile, tuplist, location)
# 	print checked_list
# 	cleaned_list = clean_list(checked_list)
# 	print cleaned_list
# 	highest_word = score_list(cleaned_list)
# 	return highest_word
start = time()
possible_words = steptwo(tile,inventory)
cleaner_list = cleaner(tile,possible_words)
tuplewear = split_list(tile,cleaner_list)
ok_list = check_list(tile,tuplewear,(3,1))
cleanest_list = clean_list(ok_list)
print score_list(cleanest_list)
print time() - start