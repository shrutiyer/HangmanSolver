"""dis be da ai fo da list, mon"""
import sets
from collections import Counter
from time import time

word_list = [line.strip() for line in open("words.txt", 'r')]
word_set = set(word_list)

# tile = ['p']
# tile = [tile[0].upper()]
# inventory = ['a','t','w','l','p','p','i']
# word = 'apple'
# location = (2,3)

points = {'A':1,'B':3,'C':3, 'D':2, 
            'E':1, 'F': 4, 'G':2, 'H':4, 
            'I': 1,'J':8, 'K': 5, 'L': 1,
            'M':3, 'N':1, 'O':1, 'P':3,
            'Q':10, 'R':1, 'S':1, 'T':1,
            'U':1,'V':4, 'W':4, 'X':8,
            'Y':4,'Z':10}

def stepone(tile,inventory,word):
	"""figures out if the word can be made given the letter and inventory"""
	letterstock = list(tile) + inventory
	listed_word = list(word)
	return not Counter(listed_word)-Counter(letterstock)

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
		if tile[0].upper() in word:
			cleaned_list.append(word)
	return cleaned_list

def splitter(tile,word):
	"""splits the word at the tile"""
	temp = list(word)
	index = temp.index(tile[0].upper())
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
	if len(tuplewear[0]) <= tile_spaces[0] and len(tuplewear[1]) <= tile_spaces[1]:
		return tuplewear[0], tile[0], tuplewear[1]
	else:
		#print "thinks there isn't room"
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
	for part in word:
		for letter in part:
			score += points[letter.upper()]
	return score

def score_list(cleaned_list):
	"""prints the highest scoring word in the list"""
	scores = []
	#print 'cleaned list', cleaned_list
	for word in cleaned_list:
		score=get_score(word)
		scores.append((score,word))
	if scores:
		return max(scores)
	else:
		#print "thinks there are no words"
		return False

def overall(tile,inventory,location):
	possible_words = steptwo(tile,inventory)
	cleaner_list = cleaner(tile,possible_words)
	#print cleaner_list
	tuplewear = split_list(tile,cleaner_list)
	ok_list = check_list(tile,tuplewear,location)
	cleanest_list = clean_list(ok_list)
	return score_list(cleanest_list)

def parse_through_list(all_positions,inventory):
	"""Give it the list within the list within a list"""
	#print "all position in parse", all_positions
	list_of_possible_words = []
	inventory = [x.lower() for x in inventory]
	# print "lower list", inventory
	for each_position in all_positions:
		#print 'each position', each_position
		letter = each_position[0].lower()
		#print "lower letter", letter
		row_spots = each_position[1]
		column_spots = each_position[2]
		location = each_position[3]
		if row_spots != [0,0]:
			#print "row spots", row_spots
			if overall(letter,inventory,row_spots):
				list_of_possible_words.append([overall(letter,inventory,row_spots),'r',location])
		if column_spots != [0,0]:
			#print "column_spots", column_spots
			if overall(letter,inventory,column_spots):
				list_of_possible_words.append([overall(letter,inventory,column_spots),'c',location])
		#print "list_of_possible_words in ailist", list_of_possible_words
	if not all(item is False for item in list_of_possible_words):
		return max(list_of_possible_words)
	else:
		return False