import pygame
from pygame.locals import *

import sys
import os
 
from meteor import Meteor
import player
import random
import star

pygame.init()
pygame.display.set_caption("PyGame")

pygame.font.init()
myfont = pygame.font.SysFont('Segoe UI', 45)

resolution = (1500, 700)
BLACK = (0,0,0)
WHITE = (255,255,255)

screen = pygame.display.set_mode(resolution)

background = pygame.Surface(resolution)
background.fill((255, 255, 255))

bottom_border = pygame.transform.scale(pygame.image.load(os.path.join(sys.path[0], "assets\\gradient.jfif")), (1800, 100))


clock = pygame.time.Clock()
player = player.Player()

spritegroup = pygame.sprite.Group()
met_spritegroup = pygame.sprite.Group()

max_timer = 100
timer = max_timer

met_maxtimer = 100
met_timer = met_maxtimer

pos = ()  

def ChooseSideAndPos():
	global side
	global pos

	side = random.randint(1,4)
	if side == 1:
		pos = (random.randint(50, resolution[0] - 50), 50)
	elif side == 2:
		pos = (random.randint(50, resolution[0] - 50), resolution[1] - 50)
	elif side == 3:
		pos = (50, random.randint(20, resolution[1] - 50))
	else:
		pos = (resolution[0] - 50, random.randint(20, resolution[1] - 50))


pressed = {}

file = None
def ResetEndless():
	global file, score, score_text, player, met_spritegroup, spritegroup, timer, met_timer

	for met in met_spritegroup:
		met_spritegroup.remove(met)
	for stars in spritegroup:
		spritegroup.remove(stars)

	player.gravity = 0
	player.rect.x = int(screen.get_width() / 2)
	player.rect.y = int(screen.get_height() / 2)

	try:
		if file == None:
			file = open(os.path.join(sys.path[0], "best_score.txt"), "w")
		# file.write(str(score))
	except Exception as e:
		print(f"Internal Error: {e}")
		pygame.quit()
		sys.exit(-1)

	timer = max_timer
	met_timer = met_maxtimer
	score = 0
	score_text = myfont.render(str(score), False, (0, 0, 0))


if __name__ == "__main__":

	
	score = 0
	score_text = myfont.render(str(score), False, (0, 0, 0))

	player.rect.x = int(screen.get_width() / 2)
	player.rect.y = int(screen.get_height() / 2)
	
	running = True

	while running: 

		screen.blit(background, (0,0))
		screen.blit(bottom_border, (-100, 610))
		screen.blit(score_text,(40, 25))
		spritegroup.draw(screen)
		met_spritegroup.draw(screen)
		screen.blit(player.image, player.rect)

		pygame.display.flip()

		player.gravity += 0.08

		# Top border
		if player.rect.y <= 0:
			player.gravity = 1

		# Bottom border
		if player.rect.y >= resolution[1] - 90:
			ResetEndless()

		player.velocity = [player.velocity_x, player.gravity]
		player.rect = player.rect.move(player.velocity)

		for meteor in met_spritegroup:
			# Check if not in screen
			if meteor.rect.x > resolution[0] or meteor.rect.x < 0 or meteor.rect.y > resolution[1] or meteor.rect.y < -50:
				met_spritegroup.remove(meteor)

			# Movement
			if meteor.side == 1:
				meteor.rect = meteor.rect.move([0,3])
			elif meteor.side == 2:
				meteor.rect = meteor.rect.move([0,-3])
			elif meteor.side == 3:
				meteor.rect = meteor.rect.move([3,0])
			else:
				meteor.rect = meteor.rect.move([-3,0])

			# Check if collide with the player
			if pygame.sprite.collide_circle(player, meteor) == True:
				ResetEndless()

		if timer <= 0:
			new_star = star.Star(random.randint(10, resolution[0]), random.randint(50, resolution[1] - 50))
			spritegroup.add(new_star)
			timer = max_timer
		else:
			timer -= 1

		if met_timer <= 0:
			ChooseSideAndPos()
			new_met = Meteor(pos[0], pos[1])
			new_met.side = side
			if side == 1:
				pass
			elif side == 2:
				new_met.image = pygame.transform.rotate(new_met.image, 180)
			elif side == 3:
				new_met.image = pygame.transform.rotate(new_met.image, 90)
			else:
				new_met.image = pygame.transform.rotate(new_met.image, 270)
			met_spritegroup.add(new_met)
			met_timer = met_maxtimer
		else:
			met_timer -= 1

		if pressed.get(pygame.K_RIGHT) and player.rect.x + player.rect.width < screen.get_width():
			player.rect.x += player.speed
		elif pressed.get(pygame.K_LEFT) and player.rect.x > 0:
			player.rect.x -= player.speed

		for test_star in spritegroup:
			if pygame.sprite.collide_circle(player, test_star) == True:
				score += 1
				score_text = myfont.render(str(score), False, (0, 0, 0))
				spritegroup.remove(test_star)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				pressed[event.key] = True

				if event.key == pygame.K_SPACE:
					player.gravity = 0
					player.gravity -= 5

			elif event.type == pygame.KEYUP:
				pressed[event.key] = False    

		if player.rect.y >= 920:
			#print('Dead')
			pass

		clock.tick(60)
