""" dis be our ai for tha tree, mon"""
import pickle
from tree import Tree
from tree import Node
from time import time
Paul = pickle.load(open('pickledtree.txt','rb'))

points = {'a':1,'b':3,'c':3, 'd':2, 
            'e':1, 'f': 4, 'g':2, 'h':4, 
            'h': 1,'i':1, 'j':8, 'k': 5, 'l': 1,
            'm':3, 'n':1, 'o':1, 'p':3,
            'q':10, 'r':1, 's':1, 't':1,
            'u':1,'v':4, 'w':4, 'x':8,
            'y':4,'z':10}




# letterstock = inventory + letter
# print letterstock
# start = time()
# possible_words = Paul.find_all_words(letterstock)
# print possible_words
# print time() - start

def make_all_words(tile,inventory):
	"""finds the list of possible words at a location"""
	letterstock = []
	letterstock.extend(inventory)
	letterstock.extend(tile)
	alreadyfound = {}
	if tile[0] in alreadyfound:
		return alreadyfound[tile[0]]
	else:
		alreadyfound[tile[0]] = Paul.find_all_words(letterstock)
		return alreadyfound[tile[0]]

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
	"""checks to see if you can actually put a word there"""
	if len(tuplewear[0]) <= tile_spaces[0] and len(tuplewear[1]) <= tile_spaces[1]:
		return (tuplewear[0] ,tile[0], tuplewear[1])
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
	for part in word:
		for letter in part:
			score += points[letter]
	return score

def score_list(cleaned_list):
	"""prints the highest scoring word in the list"""
	scores = []
	for word in cleaned_list:
		score=get_score(word)
		scores.append((score,word))
	#print 'scores', scores
	if scores:
		return max(scores)
	else:
		return False

def letter_loop(letterlist,inventory,locations):
	"""loops through the list of possible letter-location combos"""


# inventory = ['e','x','r','z','a','d','a']
# letter = ['a']
# location = [2,3]

def overall(letter,inventory,location):
	''' 
	takes in inventory, letter and spacing around the letter
	returns highest scoring word and its score'''
	#print "letter, inventory, location", letter,inventory,location
	wordlist = make_all_words(letter, inventory)
	wordlist = cleaner(letter,wordlist)
	#print 'wordlist', wordlist
	tuplist = split_list(letter,wordlist)
	checked_list = check_list(letter, tuplist, location)
	#print 'checked list', checked_list
	cleaned_list = clean_list(checked_list)
	#print 'cleaned list', cleaned_list
	if cleaned_list:
		return score_list(cleaned_list)
	else:
		return False

#print overall(letter,inventory,location)

def parse_through_list(all_positions,inventory):
	"""Give it the list within the list within a list"""
	list_of_possible_words = []
	inventory = [x.lower() for x in inventory]
	#print "lower list", inventory
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
	if not all(item is False for item in list_of_possible_words):
		return max(list_of_possible_words)
	else:
		return False

""" function to loop through all of them in all locations and see if 
	they're legal then compute the max"""

"""letter plus inventory
	-make all possible find_all_words
	-see if you can put words there
	-add possible words to list
	-do for every place"""

""" if i've already computed, return previous computation
	using dictionary value, list"""
""" dominant cost"""