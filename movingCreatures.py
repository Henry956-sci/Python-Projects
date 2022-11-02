import time
import random

#The function that picks a random item from the kinds of creatures list
def randomPick(l):
	if len(l) <= 0:
		return None
	i = random.randrange(len(l))
	return l[i]

class World:

	#creates a list of creature types that are randomly picked to be the next type
	kinds_of_creatures = ["Creature", "Walker", "Zigzagger", "Runner", "Jumper"]
	#sets the max number of creatures in the world
	maxNumCreatures = 20

	def __init__(self, n=25):
		#sets the size of the world as n
		self.size = n
		#creates an nxn matrix, simulating a 2 dimensional world
		self.locs = [[' ' for i in range(n)] for i in range(n)]
		#creates an empty list of creatures, to be filled by random choice of types later
		self.creatures = []

	def display(self):
		print("\n")
		#initiates the number of each type to 0
		numWalkers = 0
		numZigzaggers = 0
		numRunners = 0
		numJumpers = 0
		#counts the list, and increments the count of each creature
		for creature in self.creatures:
			if type(creature) == Walker:
				numWalkers += 1
			if type(creature) == Zigzagger:
				numZigzaggers += 1
			if type(creature) == Runner:
				numRunners += 1
			if type(creature) == Jumper:
				numJumpers += 1
		#displays the number of creatures for each creature
		print("NUmber of creatures: ", numWalkers, " walkers, ", numZigzaggers, " zigzaggers", numRunners, " Runners", numJumpers, " Jumpers")
		#generates the world border
		print("$  ", " $ " * self.size, "  $")
		for row in self.locs:
			rowStr = "$  "
			for col in row:
				rowStr += " " + col + " "
			rowStr += "   $"
			print(rowStr)
		print("$  ", " $ " * self.size, "  $")

	def checkLoc(self, loc):
		#checks if the location is within the world bounds
		return (loc[0] < self.size) and (loc[0] >= 0) and (loc[1] < self.size) and (loc[1] >= 0)

	#continually generates the world		
	def start(self):
		while True:
			#count variable to be used for counting the amount of jumpers in the world
			count = 0
			self.display()
			# print("press any key to exit")
			#if the number of creatures is less than the maximum number of allowed creatures in the world, then it generates a new creature
			if len(self.creatures) < World.maxNumCreatures:
				nextCreatureKind = randomPick(World.kinds_of_creatures)
				#goes through the creature list and counts the number of Jumpers in it
				for creature in self.creatures:
					if type(creature) == Jumper:
						count = count + 1
					#if the number of jumpers is greater than or equal to 2, it generates a new next creature
					if count >= 2:
						while nextCreatureKind == 'Jumper':
							nextCreatureKind = randomPick(World.kinds_of_creatures)
					#otherwise, it generates the next creature as usual

				# print(nextCreatureKind)
				nextCreatureClass = globals()[nextCreatureKind]
				nextCreature = nextCreatureClass(random.randrange(self.size), random.randrange(self.size))
				print("New creature created: ", nextCreatureKind, "at ", nextCreature.getLoc())
				self.creatures.append(nextCreature)
			#generates an empty list to be filled with creatures that are not jumpers and that are out of bounds
			toRemove = []
			for creature in self.creatures:
				#gets the current location of the creature and the location of where it is supposed to go
				curLoc = creature.getLoc()
				nextLoc = creature.randMove()

				if not self.checkLoc(nextLoc):
					#if the creature is a jumper, it makes it go to the opposite side of the map instead of deleting it
					if type(creature) == Jumper:
						nextLocation = list(nextLoc)
						nextLocation[0] = nextLocation[0] % self.size
						nextLocation[1] = nextLocation[1] % self.size
						nextLoc = tuple(nextLocation)
						#if the next location isn't empty
						if self.locs[nextLoc[0]][nextLoc[1]] != ' ':
							#it stays in its current position
							creature.setLoc(curLoc[0], curLoc[1])
							continue
						#empties out the current location of where the creature is
						self.locs[curLoc[0]][curLoc[1]] = ' '
						#moves the the creature's symbol to the spot it moved to
						self.locs[nextLoc[0]][nextLoc[1]] = creature.getSymbol()
						#sets the creature's current location to the spot it moved to		
						creature.setLoc(nextLoc[0], nextLoc[1])				
						continue
					#otherwise, it just empties out the creature's current spot and puts the creature in the deletion list
					self.locs[curLoc[0]][curLoc[1]] = ' '
					toRemove.append(creature)
					continue
				
				#if the next location isn't empty
				if self.locs[nextLoc[0]][nextLoc[1]] != ' ':
					#it keeps the current location
					creature.setLoc(curLoc[0], curLoc[1])
					continue
				
				#empties out the creature's current location
				self.locs[curLoc[0]][curLoc[1]] = ' '
				#puts the creature's symbol in the location it's moving to
				self.locs[nextLoc[0]][nextLoc[1]] = creature.getSymbol()
			
			#deletes all the creatures in the list
			for creature in toRemove:
				self.creatures.remove(creature)

			# ch = input()
			time.sleep(2)


class Creature:

	#constructs the creature class when its given no coordinates
	def __init__(self):
		self.xCor = 0
		self.yCor = 0

	#constructs the creature class when it is given coordinates
	def __init__(self, xCor, yCor):
		self.xCor = xCor
		self.yCor = yCor

	#returns the creature's current coordinates
	def getLoc(self):
		return self.xCor, self.yCor

	#changes the creature's current location to the location that it is given
	def setLoc(self, xCor, yCor):
		(self.xCor, self.yCor) = (xCor, yCor)

	#returns the creature's symbol
	def getSymbol(self):
		return 'c'

	#moves the creature in a given direction
	def move(self, d):
		return (self.xCor, self.yCor)

	def randMove(self):
		#if the creature is a jumper, it picks between 8 directions instead of 4
		if type(self) == Jumper:
			randNum = random.randrange(8)
			if randNum == 0:
				d = 'n'
			elif randNum == 1:
				d = 'ne'
			elif randNum == 2:
				d = 'e'
			elif randNum == 3:
				d = 'se'
			elif randNum == 4:
				d = 's'
			elif randNum == 5:
				d = 'sw'
			elif randNum == 6:
				d = 'w'
			else:
				d = 'nw'
			return self.move(d)
		#otherwise, it just picks from 4 directions 
		randNum = random.randrange(4)
		if randNum == 0:
			d = 'n'
		elif randNum == 1:
			d = 'e'
		elif randNum == 2:
			d = 's'
		else:
			d = 'w'
		return self.move(d)		


class Walker(Creature):

	#returns the symbol of walker
	def getSymbol(self):
		return 'w'

	#moves the walker in a given direction after calling the walk function
	def move(self, d):
		return self.walk(d)

	#moves the walker in a direction by 1, and returns the values of the coordinates as a tuple
	def walk(self, d):
		if d == 'n':
			self.yCor -= 1
		elif d == 'e':
			self.xCor += 1
		elif d == 's':
			self.yCor += 1
		elif d == 'w':
			self.xCor -= 1
		return (self.xCor, self.yCor)

class Zigzagger(Walker):

	def __init__(self):
		super().__init__() # super() returns the pointer of the entailed parent class object
		self.toLeft = -1

	def __init__(self, xCor, yCor):
		super().__init__(xCor, yCor)
		self.toLeft = -1

	#returns the symbol of the zigzagger
	def getSymbol(self):
		return 'z'

	#moves the zigzagger by calling the zigzag function
	def move(self, d):
		return self.zigzag(d)

	#moves the zigzagger by offsetting the direction by the value of toLeft
	def zigzag(self, d):
		super().walk(d)
		
		if d == 'n':
			self.xCor -= self.toLeft
		elif d == 'e':
			self.yCor += self.toLeft
		elif d == 's':
			self.xCor += self.toLeft
		elif d == 'w':
			self.yCor -= self.toLeft
		else:
			self.toLeft = - self.toLeft
		self.toLeft = - self.toLeft
		return (self.xCor, self.yCor)


class Runner(Walker):

	def __init__(self):
		super().__init__() # super() returns the pointer of the entailed parent class object
		self.speed = 2

	def __init__(self, xCor, yCor):
		super().__init__(xCor, yCor)
		self.speed = 2

	#returns the runner's symbol
	def getSymbol(self):
		return 'r'

	#moves the runner by calling the run function
	def move(self, d):
		return self.run(d)

	#moves the runner by moving it by the value of speed in a given direction
	def run(self, d):
		if d == 'n':
			self.yCor -= self.speed
		elif d == 'e':
			self.xCor += self.speed
		elif d == 's':
			self.yCor += self.speed
		elif d == 'w':
			self.xCor -= self.speed
		return (self.xCor, self.yCor)

class Jumper(Creature):

	def __init__(self):
		super().__init__()
		self.time = 0
		self.speed = 3

	def __init__(self, xCor, yCor):
		super().__init__(xCor, yCor)
		self.time = 0
		self.speed = 3

	#returns the symbol of jumper
	def getSymbol(self):
		return 'j'
	
	#moves the jumper by calling the jump function
	def move(self, d):
		return self.jump(d)

	#moves the jumper by moving in one of 8 directions with the value of speed, which is 3 in this case
	def jump(self, d):
		#jumper moves only every other turn
		if (self.time % 2 == 0):
			self.time += 1
			return (self.xCor, self.yCor)

		if d == 'n':
			self.yCor += self.speed
		elif d == 'ne':
			self.xCor += self.speed
			self.yCor += self.speed
		elif d == 'e':
			self.xCor += self.speed
		elif d == 'se':
			self.xCor += self.speed
			self.yCor -= self.speed
		elif d == 's':
			self.yCor -= self.speed
		elif d == 'sw':
			self.xCor -= self.speed
			self.yCor -= self.speed
		elif d == 'w':
			self.xCor -= self.speed
		elif d == 'nw':
			self.xCor -= self.speed
			self.yCor += self.speed
		self.time += 1
		return(self.xCor, self.yCor)
		
		

# For windows
# from pynput 
# import keyboard
# import keyboard
# def on_press(key):
#	exit()

# listener = keyboard.Listener(on_press=on_press)
# listener.start()  # start to listen on a separate thread
# listener.join()  # remove if main thread is polling self.keys

#initiates world	
world = World()
world.start()