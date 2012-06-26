#!/usr/bin/python
import random
import sys

#For debugging, ignore if debug: blocks
debug = False
hashing = False

#These numbers are to do with the generation of 
##monsters with random stats based on what type they are
###The value in the names are the percentage of that monsters stats that are
####Going to be in that attribute
mobTypes 	= [
#    name           dam	  atk   def  
	("Mountain",	0.03, 0.04, 0.02),
	("Cave",		0.02, 0.03, 0.05),
	("Swamp",		0.05, 0.02, 0.03),
	("Mainland",	0.05, 0.03, 0.00),
	("Forest",		0.00, 0.05, 0.00)
	]
mobPrefixes = [
#    name           dam	  atk   def   
	("Enraged",		1.10, 1.10, 1.10),
	("Rabid",		1.15, 1.15, 1.15),
	("Vicious",		1.20, 1.20, 1.20),
	("Savage",		1.25, 1.25, 1.25),
	("Unique",		1.30, 1.30, 1.30)
	]
mobNames    = [
#    name           dam	  atk   def
	("Troll", 		50.0, 15.0, 35.0),
	("Kobold", 		30.0, 35.0, 25.0),
	("Ghast", 		30.0, 50.0, 20.0),
	("Chimera", 	35.0, 35.0, 30.0),
	("Ogre", 		30.0, 25.0, 45.0)
	]

humanoidPrefixes = [
#    name           dam	  atk   def   
	("Elvish",		0.03, 0.04, 0.02),
	("Human",		0.02, 0.03, 0.05),
	("Dwarven",		0.05, 0.02, 0.03),
	("Corrupted",	0.05, 0.03, 0.00),
	("Gnomish",		0.00, 0.05, 0.00)
	]
humanoidTypes 	 = [
#    name           dam	  atk   def   
	("Battle",		1.10, 1.10, 1.10),
	("Guardian",	1.15, 1.15, 1.15),
	("Templar",		1.20, 1.20, 1.20),
	("Brutal",		1.25, 1.25, 1.25),
	("Champion",	1.30, 1.30, 1.30)
	]
humanoidNames 	 = [
#    name           dam	  atk   def   
	("Priest",		50.0, 30.0, 20.0),
	("Knight",		30.0, 30.0, 40.0),
	("Rogue",		50.0, 40.0, 10.0),
	("Mage",		45.0, 30.0, 25.0),
	("Warrior",		30.0, 40.0, 30.0)
	]
	
#Global for players in multiplayer	
players = []

class Potion(object):
	price = 10000000
	name = ""
	 
class HalfPotion(Potion):
	def __init__(self, name):
		self.price = 10
		self.name = "Half Heal"
	def use(self, player):
		player.fightHealth += player.health / 2 
		print "You have been healed for half of your health"
		player.inventory.remove(self)
			
class FullPotion(Potion):
	def __init__(self, name):
		 self.name = "Full Heal"
		 self.price = 20
	def use(self, player):
		player.fightHealth = player.health
		print "You are now on full health"
		player.inventory.remove(self)
		
class MinorPotion(Potion):
	def __init__(self, name):
		self.name = "Minor Heal"
		self.price = 5
	def use(self, player):
		player.fightHealth += player.health / 4
		print "You have been healed for a quarter of you health"
		player.inventory.remove(self)
		
#Class player, fairly straightforward
class Player(object):
	inventory = [] #inventory
	name 	  	= ""
	damage 	  	= 5
	attack 	  	= 5
	defence   	= 5
	health    	= 25
	fightHealth = 0
	level	  	= 1
	gold 	  	= 10
	exp 	  	= 0
	expNeed   	= 10
	points 	  	= 0
	lives 	  	= 3
	turnPoints = 3
	def __init__(self, name):
		self.fightHealth = self.health
		self.name = name
	def takeDamage(self, damage):
		self.fightHealth -= int(damage)
	#This levelling system makes it so that players need slightly more exp every time they level
	def levelling(self,amount):
		print "%s has gained %i Experience" % (self.name, amount)
		self.exp += amount
		#Here, as the player levels, the amount needed to level grows 
		if (self.exp >= self.expNeed): #Check to see if player has levelled
			self.level += 1
			self.points += 6
			print "%s has gained a level, go to Character menu to level up." % (self.name)
			self.exp = (0 + self.exp - self.expNeed)
			#These two make it so that every ten levels, the amount of exp needed increases slightly faster 
			expUp = float(self.level / 100)
			self.health += (5 * (1 + (expUp * 10)))
			self.expNeed = (self.expNeed + (self.expNeed / 3 * (1 + (expUp)))) #Designed so that exp required goes up over time
		if debug:
			print "return:levelling"
	def levelUp(self):
		print "You have %i points to spend" % self.points
		menuitems = ["Damage", "Attack", "Defence", "Health", "Back"]
		select = menu(menuitems)
		if (select <= 4):
			print "Increasing %s's %s by 1 to %d" % (self.name, menuitems[select - 1], getattr(self, menuitems[select - 1].lower()) + 1)
			setattr(self, menuitems[select - 1].lower(), getattr(self, menuitems[select - 1].lower()) + 1)
			self.points -= 1
		else:
			return		
	def getGold(self, amount):
		print "%s has gained %i Gold" % (self.name, amount)
		self.gold += amount
	def seeStats(self):
		print "Name: %s \nLevel: %d\nDamage: %d\nAttack: %d\nDefence: %d\nHealth: %d" % (self.name, self.level, self.damage, self.attack, self.defence, self.health)
	def buyPotion(self, item):
		if (self.gold) >= int(item.price):
			self.gold -= item.price
			print "%s has purchased a %s for %i gold" % (self.name, item.name, item.price)
			print "%s now have %i Gold" % (self.name, self.gold)
			self.inventory.append(item)
		else:
			print "You can't afford that."
	def died(self):
		self.lives -= 1
		self.gold -= self.gold * 0.5
		print "%s has died and lost half of their Gold." % self.name
		if (self.lives == 0):
			print "%s has no more lives" % self.name
			if (len(players) == 0):
				sys.exit()
			players.remove(self)
	def getTotal(self):
		return (self.damage + self.attack + self.defence)
				
#Generates mob stats	
##Base stats held with name in, multiplied by value based on 
###Prefix and type as defined in mob arrays
class Humanoid(Player):
	def __init__(self, player):
		#Get total number of player attribute points
		total = float(player.getTotal())
		nameIndex 	 = (random.randint(0, len(mobNames) - 1))
		prefixIndex  = (random.randint(0, len(mobPrefixes) - 1))
		typeIndex 	 = (random.randint(0, len(mobTypes) - 1))
		self.name 	 = ("%s %s %s") % ((humanoidPrefixes[prefixIndex][0]), (humanoidTypes[typeIndex][0]), (humanoidNames[nameIndex][0])) 
		##Distribute total points between mob attributes
		self.damage  = int(random.gauss((total / 100 * humanoidNames[nameIndex][1]) * (humanoidPrefixes[prefixIndex][1] + humanoidTypes[typeIndex][1]), 0.5))
		self.attack  = int(random.gauss((total / 100 * humanoidNames[nameIndex][2]) * (humanoidPrefixes[prefixIndex][2] + humanoidTypes[typeIndex][2]), 0.5)) 
		self.defence = int(random.gauss((total / 100 * humanoidNames[nameIndex][3]) * (humanoidPrefixes[prefixIndex][3] + humanoidTypes[typeIndex][3]), 0.5))
		self.level = player.level 
		#Stops value error if health < 1 at the start of the game
		try:
			self.fightHealth  = int(random.triangular((player.health * 0.9), (player.health * 1.1), player.health))
		except ValueError:
			self.fightHealth = player.health
	def enemyStats(self):
		print "Name: %s \nLevel: %d\nDamage: %d\nAttack: %d\nDefence: %d\nHealth: %d" % (self.name, self.level, self.damage, self.attack, self.defence, self.fightHealth)
			
class Monster(Player):
	def __init__(self, player):
		total = float(player.getTotal())
		nameIndex 	 = (random.randint(0, len(mobNames) - 1))
		prefixIndex  = (random.randint(0, len(mobPrefixes) - 1))
		typeIndex 	 = (random.randint(0, len(mobTypes) - 1))
		self.name 	 = ("%s %s %s") % ((mobPrefixes[prefixIndex][0]), (mobTypes[typeIndex][0]), (mobNames[nameIndex][0]))
		self.damage  = int(random.gauss((total / 100 * mobNames[nameIndex][1]) * (mobPrefixes[prefixIndex][1] + mobTypes[typeIndex][1]), 0.5))
		self.attack  = int(random.gauss((total / 100 * mobNames[nameIndex][2]) * (mobPrefixes[prefixIndex][2] + mobTypes[typeIndex][2]), 0.5))
		self.defence = int(random.gauss((total / 100 * mobNames[nameIndex][3]) * (mobPrefixes[prefixIndex][3] + mobTypes[typeIndex][3]), 0.5))
		self.level = player.level
		try:
			self.fightHealth  = int(random.triangular((player.health * 0.9), (player.health * 1.1), player.health))
		except ValueError:
			self.fightHealth = player.health
	def enemyStats(self):
		print "Name: %s \nLevel: %d\nDamage: %d\nAttack: %d\nDefence: %d\nHealth: %d" % (self.name, self.level, self.damage, self.attack, self.defence, self.fightHealth)

#Menu template to be used in all other menus
def menu(items):
	if hashing:
		for item in range(0, len(items)):
			#1 based menu, prints everything in items
			print "%d - %s" % (item + 1, items[item])
		return random.randint(1, len(items))
	while 1:
		for item in range(0, len(items)):
			#1 based menu, prints everything in items
			print "%d - %s" % (item + 1, items[item])
		selection = raw_input("> ")
		try:
			#Checks to see if input is a number
			selection = int(selection)
			if ( selection > 0 ) and ( selection <= len(items) ):
				return selection
		except ValueError:
			#Checks to see if input is a word
			for item in range( 0, len(items) ):
				#Checks all items against player selection, if true, returns item
				if ( items[item].lower() == selection.lower() ):
					return item + 1
		print "Invalid selection"

def mainMenu():
	options = [
	"Maths",
	"Game", 
	"Shop", 
	"Character", 
	"Info", 
	"Exit"
	]
	#Allows multiplayer
	while True:
		try:
			numPlayers = int(raw_input("Number of players:"))
			break
		except ValueError:
			print "Invalid Selection"
	if (numPlayers < 1):
		print "YOU LOST THE GAME!"
		return
	for playerindex in range(0, numPlayers):
		players.append(Player(raw_input("Name for player %d: " % (playerindex + 1))))
	while 1: 
		for player in players:
			if (numPlayers > 1):
				print "%s has %i turns left" % (player.name, player.turnPoints)
			if debug:
				print "We got to players"
			while (player.turnPoints > 0):
				if debug:
					print "We got past turnPoints"
				#Stops printing "player's turn" when there is only one player
				if (numPlayers > 1):
					print "*********\n%s's Turn!" % player.name
				else:
					print "*********"
				menuchoice = menu(options)
				#Choose maths
				if (menuchoice == 1):
					mathMenu(player)
				#Choose game
				elif (menuchoice == 2):
					while True:
						try:
							number = int(raw_input("Number of enemies "))
							break
						except ValueError:
							print "Invalid Selection."
					for number in range(0, number):
						x = random.randint(1, 2)
						if (x == 1):
							gameFight(player, Humanoid(player))
						else:
							gameFight(player, Monster(player))
				#Choose Shop
				elif (menuchoice == 3):
					shopMenu(player)
				#Choose Character
				elif (menuchoice == 4):
					player.seeStats()
					levellingMenu(player)
				elif (menuchoice == 5):
					infoMenu(player)
				elif (menuchoice == 6):
					return
		for player in players:
			player.turnPoints = 3

def levellingMenu(player):
	for num in range (0, player.points):
		player.levelUp()
	player.seeStats()
					
def mathMenu(player):
	options = [
	"Addition",
	"Subtraction",
	"Multiplication",
	"Division",
	"Back"
	] 
	mathQuestion(player, menu(options))

#Generates two random numbers in range 1, 10 and their value
##Asks player what their value is, if correct, exp and gold goes up
def mathQuestion(player, type):
	x = random.randint(1, 10)
	y = random.randint(1, 10)
	z = 0
	a = ""
	#if/elif block to allocate question variables with values corresponding to players selection
	if (type == 1):
		z = (x + y)
		a = ("+")
	elif (type == 2):
		z = (x - y)
		a = "-"
	elif (type == 3):
		z = (x * y)
		a = "x"
	elif (type == 4):
		z = (x / float(y))
		a = " / "
		isGreater = False
	else:
		return
	#If block to make sure that x is always greater than y.
	if (type == 4):
		while (isGreater == False): 
			if (x < y):
				x = random.randint(1, 10)
				y = random.randint(1, 10)
				z = (x / float(y))
			else:
				isGreater = True
	smartArse = 0
	isSmart = True
	while True:
		print "What is %d %s %d?" % (x, a, y)
		try:
			answer = float(raw_input("> "))
		except:
			#Just for some fun :P
			if isSmart:
				if (smartArse < 5):
					print "Look, mate, just answer the bloody question."
				if (smartArse == 5):
					print "You think you are pretty clever don't you?"
				elif (smartArse == 10):
					print "You are really starting to piss me off."
				elif (smartArse == 15):
					print "Look, I'll give you an attribute point if you shut up"
					yesNo = menu(["Yes", "No"])
					if (yesNo == 1):
						player.points += 1
						isSmart = False
					else:
						print "Your call."
				elif (smartArse == 16):
						print "Resistance is futile!"
						player.died()
						isSmart = False
				smartArse += 1
		else:
			break		
	#Makes an approximation of float correct
	if ((answer > (z - 0.0001)) and (answer < (z + 0.0001))):
		print "Yes! %d %s %d does equal %g" % (x, a, y, z)
		#Add gold & exp
		player.getGold(10)
		player.levelling(10)
		player.turnPoints -= 1
	else:
		print "Oops, %d %s %d is actually %g" % (x, a, y, z)
		player.turnPoints -= 1

def shopMenu(player):
	options = ["Minor Heal", "Half Heal", "Full Heal", "Back"]
	while 1:
		select = menu(options)
		if (select == 1):
			player.buyPotion(MinorPotion(player))
		elif (select == 2):
			player.buyPotion(HalfPotion(player))
		elif (select == 3):
			player.buyPotion(FullPotion(player))
		elif (select == 4): 
			return
				
def gameFight(player, enemy):
	#So that potions work properly
	player.fightHealth = player.health
	enemy.enemyStats()
	options = ["Attack", "Heal", "Escape"]
	while (enemy.fightHealth > 0) and (player.fightHealth > 0):
		select = menu(options)
		if (select == 1):
			if "Escape" in options:
				options.remove("Escape")
			#Player attacks enemy
			didKill = fighting(player, enemy)
			if (didKill == 1): 
				player.getGold(10)
				player.levelling(10)
				player.turnPoints -= 1
				if debug:
					print "turn points is %d" % player.turnPoints
				return
			#Enemy attacks player
			else:
				didKill = fighting(enemy, player)
				if (didKill == 1):
					player.died()
					player.turnPoints -= 1
					return
		elif (select == 2):
			potions = {}
			#Checks inventory for potions
			for item in player.inventory:
				#Checks to see if we have seen it before
				if item.__class__.__name__ in potions:
					#Add to list of same potion
					potions[item.__class__.__name__].append(item)
				else:
					#Make new list of potions
					potions[item.__class__.__name__] = [item]
			#Get keys
			menuItems = potions.keys()
			menuItems.append("Back")
			select = menu(menuItems)
			if (select < len(menuItems)):
				print "Using %s on %s" % (potions[menuItems[select - 1]][0].name, player.name)
				potions[menuItems[select - 1]][0].use(player)
		elif (select == 3):
			return

def fighting(attacker, defender):
	damage = int(random.triangular((attacker.damage * 0.8), (attacker.damage * 1.2), attacker.damage))
	#Check to see if player hits
	if (random.randint(0, int(attacker.attack)) >= random.randint(0, int(defender.defence))):
		print "%s hits %s for %i damage" % (attacker.name, defender.name, damage)
		defender.takeDamage(damage)
		#Checks to see if player is dead
		if (defender.fightHealth > 1):
			print "%s is on %i health" % (defender.name, defender.fightHealth)
		elif (defender.fightHealth <= 0):
			print "%s has slain %s" % (attacker.name, defender.name)
			return 1
	else:
		print "%s misses" %	attacker.name

def infoMenu(player):
	print "Welcome, %s" % player.name
	print "To select an option, simply enter the name or associated number."
	while 1:
		select = menu(["Maths", "Fighting", "Shop", "Back"])
		if (select == 1):
			print "You will answer questions to gain money and experience when you are too weak."
		elif (select == 2):
			print "You fight monsters to get items, gold and experience."
		elif (select == 3):
			print "You can use the shop to buy potions and (eventually) items"
		else:
			break
			
try:
	mainMenu()
except KeyboardInterrupt:
	print "\nGoodbye"
