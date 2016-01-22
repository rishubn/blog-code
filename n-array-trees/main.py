import pygame
import math
class Tree:
	root = None
	_next_id = -1
	depth = -1
	numChildren = -1
	positions = {} # (index,depth) array

	def __init__(self,depth,numChildren):
		self.depth = depth
		self.numChildren = numChildren
		self.root = self.buildTree(self.depth,self.getNextId)
		self.setIndexes(self.root,self.numChildren)
		

	def getNextId(self):
		self._next_id = self._next_id + 1
		return self._next_id


	# Recursively builds N-array Tree in preorder
	def buildTree(self, depth, lastid):
		children = {}
		if depth > 0:
			for i in range(0,self.numChildren):
				thisid = self.getNextId()
				children[thisid] = self.buildTree(depth-1,thisid)
		self.positions[lastid] = [-1, self.depth-depth]
		n = Node(lastid)
		n.setChildren(children)
		return n

	# Recursively sets serial indexes into positions for tree with N children
	# index = parentindex * numchildren - lateral position in tree
	# split into two loops, one to set indexes of a node's children, the second to traverse the tree


	def setIndexes(self,root,numChildren, parentindex=None):
		if root:
			if self.positions[root.ID][0] == -1 and self.positions[root.ID][1] == 0: # If this is the root of the tree
				parentindex = 1
				self.positions[root.ID][0] = parentindex
			i = numChildren - 1
			for ids,child in root.children.items():
				index = parentindex * numChildren - i
				self.positions[child.ID][0] = index
				i = i -1
			for ids,child in root.children.items():
				self.setIndexes(child,numChildren,self.positions[child.ID][0])

	#iterates over the positions dict and sets x and y for each node
	def mapXY(self, root, numChildren,windowSizeX,windowSizeY):
		for ids, positions in self.positions.items():
			index = positions[0]
			depth = positions[1]
			x = index * windowSizeX / (numChildren ** depth +1)
			y = depth * windowSizeY / self.depth
			actingNode = root.getNode(ids)
			actingNode.coordinates[0] = x
			actingNode.coordinates[1] = y+10 #Added 10 so the drawing is not on the top edge of the window		
	def drawTree(self,root,windowSurface,color,linecolor):
		if root:
			pygame.draw.circle(windowSurface,color,(math.floor(root.coordinates[0]),math.floor(root.coordinates[1])),5,0)
			for id,child in root.children.items():
				pygame.draw.line(windowSurface,linecolor,(root.coordinates[0],root.coordinates[1]),(child.coordinates[0],child.coordinates[1]),2)
				self.drawTree(child,windowSurface,color,linecolor)			
class Node:
	coordinates = None # (x,y) array
	ID = None # Unique identifier
	children = {} # Children dict
	def __init__(self,ID):
		self.pos = [-1,-1] # place holders
		self.coordinates = [-1,-1]
		self.ID = ID

	def setChildren(self, children):
		self.children = children

	def addChild(self, child):
		if child:
			self.children[child.ID] = child

	def getChild(self, ID):
			return self.children.get(ID)	

	def getNode(self, ID, root = None, default = None):
		if root == None:
			root = self
		if root.ID == ID:
			return root
		elif root.children is not None:
			for childID in root.children:
				output = (root.getChild(childID)).getNode(ID)
				if output is not None:
					return output
		return default


if __name__ == "__main__":
	BLACK = (0, 0, 0)
	WHITE = (255,255,255)
	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	BLUE = (0, 0, 255)
	windowSurface = pygame.display.set_mode((1000,600),0,32) #make 800x600 window
	windowSurface.fill(WHITE)
	numChildren = 4
	depth = 3
	t = Tree(depth,numChildren)
	t.mapXY(t.root,numChildren,1000,400)
	t.drawTree(t.root,windowSurface,BLUE,RED)
	pygame.display.update()