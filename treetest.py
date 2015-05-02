""" yo this is a tree test that I made so that i can get a handle
 on how to create trees and what the fuck they do"""

class Node(object):
	def __init__(self, value):
		self.value = value		# this is the data of the node
		# self.is_word = is_real_word(value)
		self.children = []		# this is the list of children

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
				self.add_child(Node(word))
				return True
		else:
			child = self.already_exists(word)
			if not child: # aka if word already exists
				self.add_child(Node(word[0]))
				# print word[0]
				#self.child.add_word(word[1:])
				#cuts off first letter then calls add word again
			#else: # if word doesn't already exist
			child = self.already_exists(word)
			child.add_word(word[1:])
				# this line doesn't work yet
				# theoretically goes into the child that already exists
				# and then continues adding word

def is_real_word(word):
	word_list = [line.strip() for line in open("words.txt", 'r')]

	return word.lower() in word_list



class Tree(object):

	def __init__(self,root):
		self.root = root
		self.cache = {}
		# print self.root

	def add_single_node(self, parent, child):
		parent.add_child(child)
		self.cache[child.value] = child

	



	# def add_word(self, word):
	# 	""" i'm runnning into the problem where I am not able to 
	# 		check whether the node i'm testing for is within the children
	# 		of the parent node """
	# 	parent = self.root
	# 	for letter in word:
	# 		child = Node(letter)
	# 		print child,
	# 		if child.value not in self.cache:
	# 			print 'not in here'
	# 			self.add_single_node(parent, child)
	# 			parent = child

	# def find(self,word):
	# 	""" return none if the word is not in the tree or the node if 
	# 		the word is in the tree """


	# def add_to_node(self, parent):
	# 	for word in open("words.txt", 'r'):
	# 		if word[0:1] not in self.cache:
	# 			child = Node(word[0:1])
	# 			if child.value not in parent.children:
	# 				parent.add_child(child)
	# 				self.cache[word[0:1]] = child

	def create_tree_from_words(self):
		for word in open("words.txt", 'r'):
			self.root.add_word(word)

		# self.root.print_kids()

	def print_tree(self,node):
		""" prints the tree"""
		for child in node.children:
			thing = []
			thing.append(child.value)
			print thing
			self.print_tree(child)

root = Node('') # the initial node that starts the whole thing
tree = Tree(root)
tree.create_tree_from_words()
				

	# def create_first_level(self):
	# 	for word in open("words.txt", 'r'):
	# 		if word[0] not in self.root.children:
	# 			child = Node(word[0])
	# 			self.root.add_child(child)

	# 			print self.root.children

	# def create_other_levels(self, parent):
	# 	for child in parent.children:
	# 		if word[0] == child.value:
	# 			if word[0:2] not in child.children:
	# 				self.child.add_child(word[0:2])
	# 				# print child.add_child



	# def print_tree(self, root):
	# 	if (root.children == []):
	# 		print root.value
	# 	else:
	# 		for child in root.children:
	# 			print child.value,
	# 		print ""
	# 		for child in root.children:
	# 			self.print_tree(child)


	# def create_tree_from_words(self, parent):
	# 	for node in parentnode.children:
	# 	print node
	# 	for word in dictlist:
# 			for j in range(len(word)):
	# 		if word[0:1] == node.value:
	# 			if word[0:2] not in node.children:
	# 				print word[0:2]
	# 				node.add_child(word[0:2])
	# 				# print word[0:j]
	# 				node.children = Node(word[0:2])
	# 				print node.value
		# NODE.print_kids

			# Root.children:
			# print word[0:1]
			# Root.add_child(Node(word[0:1]))


# Root = Node('e')
# Tree = Tree(Root)
# Tree.print_tree(Root)
# node2 = tree.root.children[1]
# node3 = node2.children[0]
# node4 = node3.children[4]
# print node2,node3,node4
# for item in tree.cache:
# 	print item,
# tree.print_tree(root)
# print "Print Kids"
# print tree.root.print_kids(),
# tree.root.print_kids()
# tree.root.print_kids()
# print tree.root.children

# nodea = Node('a')
# nodeb = Node('b')
# nodea.add_child(nodeb)
# nodea.print_kids()


# for i in range(len(Root.children)):
# 	Root.children[i] = Node(Root.children[i])

# for elements in Root.children:
# 	print elements

# # print Root.print_kids
# dictlist = open("words.txt", 'r')

# def tree_creator(parentnode):
# 	"""recursively tries *key word here* to create a tree"""

# 	print len(parentnode.children)
# 	for node in parentnode.children:
# 		print node
# 		for word in dictlist:
# 			if word[0:1] == node.value:
# 				if word[0:2] not in node.children:
# 					print word[0:2]
# 					node.add_child(word[0:2])
# 					# print word[0:j]
# 					node.children = Node(word[0:2])
# 					print node.value
# 		# NODE.print_kids
		

# tree_creator(Root)
# 				# print node.children


