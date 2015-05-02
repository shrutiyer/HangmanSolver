"""this is the tree dude"""

import pickle
from copy import deepcopy

word_list = [line.strip() for line in open("words.txt", 'r')]
word_set = set(word_list)

class Node(object):
	def __init__(self, value, parentcw): # parentcw = cum_word of parent
		self.value = value		# this is the data of the node
		self.children = []		# this is the list of children
		self.cum_word = parentcw + self.value
		#self.is_word = False
		self.is_word = self.is_real_word(self.cum_word)


	def __str__(self):		 	
		return self.value

	def print_kids(self):
		for elements in self.children:
			return elements
			print elements

	def add_child(self, obj):
		self.children.append(obj)

	def already_exists(self, word):
		''' checks to see if self (current node) has a
		child with a value equal to first letter of input word
		if true: returns the children
		if false: returns false'''
		for child in self.children:
			if child.value == word[0]:
				return child
		return False

	def add_word(self, word):
		'''adds a branch for the input word
		works by recursively doing it one letter at a time
		returns false if word already exists'''
		if len(word) == 1: #base case because going to use recursion
			if self.already_exists(word):
				return False
			else:
				self.add_child(Node(word,self.cum_word))
				return True
		else:
			child = self.already_exists(word)
			if not child: # aka if word already exists
				self.add_child(Node(word[0],self.cum_word))
				# print word[0]
				#self.child.add_word(word[1:])
				#cuts off first letter then calls add word again
			#else: # if word doesn't already exist
			child = self.already_exists(word)
			child.add_word(word[1:])
				# this line doesn't work yet
				# theoretically goes into the child that already exists
				# and then continues adding word

	def add_word2(self, word):
		""" another shot at adding a word to the tree"""
		if len(word) == 0:
			#self.is_word = True
			return False
		temp = Node(word[0],self.cum_word)
		cumulative_child_words = {c.cum_word : c for c in self.children}
		if not temp.cum_word in cumulative_child_words:
			self.add_child(temp)
		else:
			temp = cumulative_child_words[temp.cum_word]
		word = self.update_word(word)
		temp.add_word2(word)

	def update_word(self, word):
		"""shortens the string"""
		return word[1:]


	def is_real_word(self,word):
		return word.lower() in word_set

	def find_all_words(self,letters):
		possible_words = []
		if self.is_word:
			# print 'is it a real word?', 'true'
			# print "checking if the node is a, word"
			possible_words.append(self.cum_word)
			# print possible_words,
			# print 'possible words'
		# print 'type', type(self.children[0])
		for c in self.children:
			# print c, 'in for loop'
			# print 'letters', letters
			# print type(c.value)
			# print 'value of c', c.value
			# print ''
			if c.value in letters:
				# print 'new'
				# print letters
				# print "in second if statement"
				# print ''
				remaining_letters = self.change_letters(c.value,letters)
				# print ''
				# print 'back in if statement'
				#remove first occurance of letter from letters
				#have a function return the remaining letters
				# print c.find_all_words(remaining_letters)
				# print 1 
				possible_words.extend(c.find_all_words(remaining_letters))
		return possible_words

	# def find_all_words2(self,letters):


	def change_letters(self,value,letters):
		"""takes a letter out of the list of letters after it's been used"""
		# print 'in change letters, removing value:', value
		# print 'type of value', type(value)
		# print 'letters', letters
		# print 'type of letters', type(letters)
		letters = deepcopy(letters)
		letters.remove(value)
		remaining_letters = letters
		# print 'remaining letters', remaining_letters
		return remaining_letters

class Tree(object):

	def __init__(self,root):
		self.root = root
		# print self.root

	def add_single_node(self, parent, child):
		parent.add_child(child)
		self.cache[child.value] = child


	def create_tree_from_words(self):
		for word in word_list:
			print word
			self.root.add_word2(word)


	def print_tree(self,node, indent=0):
		""" prints the tree"""
		print " "*indent + "total word", node.cum_word + " is word ", node.is_word
		for child in node.children:
			thing = []
			thing.append(child.value)
			#print thing
			self.print_tree(child, indent+2)

	def find_all_words(self, letters):
		"""finds all the possible words given the letters"""
		return self.root.find_all_words(letters)



if __name__ == '__main__':
	root = Node('','') # the initial node that starts the whole thing
	tree = Tree(root)
	tree.create_tree_from_words()
	#tree.print_tree(tree.root)
	# print tree.root.children[0]
	# letters = ['a','a','l','i','i','t','t']
	# print tree.find_all_words(letters)
	# node1 = tree.root.children[0].children[1].children[1]
	# print node1
	# print node1.cum_word
	# print node1.is_word
	pickle.dump(tree, open("pickledtree.txt",'wb'), protocol=2)
	print "pickled"