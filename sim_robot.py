import random
import time
import pygame 
from pygame.locals import *
import sys
import thread


#colours
GOLD = (255,215,0)
PURPLE = (75,0,130)
RED = (255,0,0)
WHITE=(255,255,255)
BLACK = (0,0,0)


#USEFUL VARIABLES
WIDTH =500
HEIGHT =500
BACKGROUND = BLACK
SHELTER = WHITE
robot_list = []
plant_list = []
plant_cd = []
plants_on = []


pygame.init()
DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))
textfont = pygame.font.Font("freesansbold.ttf", 16)

def event_check():
	answer = 0
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key <255:
				answer = chr(event.key)
			else:
				answer = event.key
	return answer


class Robot(object):
	def __init__(self):
		global WIDTH
		global HEIGHT
		global BACKGROUND
		self.speed =  random.randint(0,8)
		self.energy =  random.randint(0,10000)
		self.size = 5
		self.counter = 0
		self.direction = "n"
		self.target = (0,0)
		self.target_object = 0
		self.directions = ["n","ne","e","se","s","sw","w","nw","stop"]
		self.distance_to_cords = {}
		self.target_cords = []
		self.state = "hunting"

		self.direction_movementsy = {"n": -1,
									"ne" : -1,
									"e" : 0,
									"se" : 1,
									"s": 1,
									"sw": 1,
									"w": 0,
									"nw": -1,
									"stop":0}

		self.direction_movementsx = {"n": 0,
									"ne" : 1,
									"e" : 1,
									"se" : 1,
									"s": 0,
									"sw": -1,
									"w": -1,
									"nw": -1,
									"stop":0}

		self.x = random.randint(0,WIDTH)
		self.y = random.randint(0,HEIGHT)

	def draw(self,colour):
		pygame.draw.polygon(DISPLAYSURF,colour,((self.x,self.y),(self.x,self.y + self.size ),(self.x + self.size,self.y + self.size),(self.x + self.size,self.y)))
		pygame.display.update()

	def undraw(self):
		pygame.draw.polygon(DISPLAYSURF,BACKGROUND,((self.x,self.y),(self.x,self.y + self.size ),(self.x + self.size,self.y + self.size),(self.x + self.size,self.y)))
		pygame.display.update()

	def direction_decider(self):
		#x stuff

		#w
		if self.target[0] < self.x:
			self.question1 = True
		else:
			self.question1 = False

		#e
		if self.target[0] > self.x:
			self.question2 = True
		else:
			self.question2 = False


		#n
		if self.target[1] < self.y: 
			self.question3 = True
		else:
			self.question3 = False

		#s
		if self.target[1] > self.y:
			self.question4 = True
		else:
			self.question4 = False


		self.answer = (self.question1, self.question2, self.question3, self.question4)


		self.lookup_which_direct = { (True,False,False,False):"w",
								(False,True,False,False):"e",
								(False,False,True,False):"n",
								(False,False,False,True):"s",
								(True,False,True,False):"nw",
								(True,False,False,True):"sw",
								(False,True,True,False):"ne",
								(False,True,False,True):"se",
								(False,False,False,False):"stop"}

		self.direction =self.lookup_which_direct[self.answer]
		


	def move(self):
		if self.energy >0:
			self.undraw()
			self.x = self.x + (self.direction_movementsx[self.direction]*self.speed)

			self.y = self.y + (self.direction_movementsy[self.direction]*self.speed)  

			if self.target[0] -10 < self.x < self.target[0] + 20 and self.target[1] -10 < self.x < self.target[1]+20 and self.target != (0,0):
				self.state = "feeding"
				print self.state

			self.energy -= self.speed**2
			self.draw(RED)
			pygame.display.update()
		else:
			self.x = self.x
			self.y = self.y



	def dist_calc(self,array):
		self.distance_to_cords = {}
		for p in array:
			if p.mode == "on":
				self.x_dist = self.x-p.x
				self.y_dist = self.y - p.y
				self.tot_dist = (self.y_dist**2 + self.x_dist**2)**0.5
				self.distance_to_cords[self.tot_dist] = (p.x,p.y)
		
		self.ordering_list = self.distance_to_cords.keys()
		if len(self.ordering_list) >0:
			self.ordering_list = sorted(self.ordering_list)

			self.one_to_go_for_distance = self.ordering_list[0]
			self.target = self.distance_to_cords[self.ordering_list[0]]
		else:
			pass


		




class Plant(object):

	def __init__(self):
		global WIDTH
		global HEIGHT
		global BACKGROUND
		self.flash_off = random.randrange(1,10)
		self.flash_on = random.randrange(5,10)
		self.colour = PURPLE
		self.second_colour = RED
		self.mode = "off"
		self.size = 10
		self.x = random.randint(0,WIDTH)
		self.y = random.randint(0,HEIGHT)






	def draw(self,colour):
		pygame.draw.polygon(DISPLAYSURF,colour,((self.x,self.y),(self.x,self.y + self.size ),(self.x + self.size,self.y + self.size),(self.x + self.size,self.y)))
		pygame.display.update()

	def undraw(self):
		if self.shelter != True:
			pygame.draw.polygon(DISPLAYSURF,BACKGROUND,((self.x,self.y),(self.x,self.y + self.size ),(self.x + self.size,self.y + self.size),(self.x + self.size,self.y)))
			pygame.display.update()
		else:
			pygame.draw.polygon(DISPLAYSURF,SHELTER,((self.x,self.y),(self.x,self.y + self.size ),(self.x + self.size,self.y + self.size),(self.x + self.size,self.y)))
			pygame.display.update()




	def flash(self):
		while True:
			pygame.draw.polygon(DISPLAYSURF,GOLD,((self.x,self.y),(self.x,self.y + self.size ),(self.x + self.size,self.y + self.size),(self.x + self.size,self.y)))
			self.mode = "on"
			plants_on.append(self)
			pygame.display.update()
			time.sleep(self.flash_on)
			pygame.draw.polygon(DISPLAYSURF,BLACK,((self.x,self.y),(self.x,self.y + self.size ),(self.x + self.size,self.y + self.size),(self.x + self.size,self.y)))
			self.mode = "off"
			plants_on.remove(self)
			pygame.display.update()
			time.sleep(self.flash_off)






for x in xrange(30):
	robot_list.append(Robot())

for x in xrange(5):
	plant_list.append(Plant())
for p in plant_list:
		thread.start_new_thread(p.flash,())


while True:
	for r in robot_list:
		if r.state == "hunting":
			r.draw(RED)
			r.dist_calc(plant_list)
			r.direction_decider()
			r.move()
		if r.state == "feeding":
			print "fuck"
			r.draw(PURPLE)










