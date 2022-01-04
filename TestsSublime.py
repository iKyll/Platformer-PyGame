def main_menu():


	endless_button = pygame.Rect((100, 40),(screen.get_width() / 2 + 50, screen.get_height / 2 + 50)) # Add size and coordinates
	levels_button = pygame.Rect((100, 40),(screen.get_width() / 2 , screen.get_height / 2)) # Add size and coordinates
	quit_button = pygame.Rect((100, 40),(screen.get_width() / 2 - 50, screen.get_height / 2 - 50)) # Add size and coordinates

	pygame.draw.rect(screen, (128, 128, 128, 10), endless_button) # Tuple is Color !! Change
	pygame.draw.rect(screen, (128, 128, 128, 10), levels_button) # Tuple is Color !! Change
	pygame.draw.rect(screen, (128, 128, 128, 10), quit_button) # Tuple is Color !! Change

	# Text
	endless_text = main_font.render('EndlessMode', False, (135, 135, 135))
	levels_text = main_font.render('Levels', False, (135, 135, 135))
	quit_text = main_font.render('Quit', False, (135, 135, 135))

	screen.blit(endless_text, (screen.get_width() / 2 + 50, screen.get_height / 2 + 50))
	screen.blit(levels_text, (screen.get_width() / 2 , screen.get_height / 2 ))
	screen.blit(quit_text, (screen.get_width() / 2 - 50, screen.get_height / 2 - 50))

	while True:
		mx, my = pygame.mouse.get_pos()

		if endless_button.collidepoint((mx ,my)):
			if isClicking:
				pass
		if levels_button.collidepoint((mx ,my)):
			if isClicking:
				pass
		if quit_button.collidepoint((mx ,my)):
			if isClicking:
				pygame.quit()
				sys.exit()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					isClicking = True
	
			elif event.type == pygame.MOUSEBUTTONUP:
				isClicking = False

		clock.tick(60)


class EndlessMode():

	def __init__(self, player, timer, max_timer, met_timer, met_maxtimer, spritegroup, met_spritegroup):
		self.player = player
		self.timer = timer
		self.max_timer = max_timer
		self.met_maxtimer = met_timer
		self.met_maxtimer = met_maxtimer
		self.spritegroup = spritegroup

	def Game(self):
		score = 0
		score_text = score_font.render(str(score), False, (0, 0, 0))

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
					score_text = score_font.render(str(score), False, (0, 0, 0))
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
				ResetEndless()

			clock.tick(60)

def pause():
	paused_text = main_font_bold.render("Game paused", False, (135, 135, 135))
	main_menu_text = main_font.render('Main Menu', False, (150, 150, 150))
	quit_text = main_font.render('Quit', False, (150, 150, 150))
	continue_text = main_font.render('Continue', False, (150, 150, 150))

	continue_button = pygame.Rect((int(resolution[0] / 2 - 100), int(resolution[1] / 2 - 120)),(200, 100))
	main_menu_button = pygame.Rect((int(resolution[0] / 2 - 100), int(resolution[1] / 2)), (200, 100))
	quit_button = pygame.Rect((int(resolution[0] / 2 - 100), int(resolution[1] / 2 + 120)),(200, 100))

	paused = True

	while paused:
		mx, my = pygame.mouse.get_pos()
		screen.fill((0,0,0))

		pygame.draw.rect(screen, (128, 128, 128, 10), continue_button)
		pygame.draw.rect(screen, (128, 128, 128, 10), main_menu_button)
		pygame.draw.rect(screen, (128, 128, 128, 10), quit_button)

		screen.blit(paused_text, (int(resolution[0] / 2 - 75), int(resolution[1] / 2 - 300)))
		screen.blit(continue_text, (int(resolution[0] / 2 - 75), int(resolution[1] / 2 - 120)))
		screen.blit(main_menu_text, (int(resolution[0] / 2 - 75), int(resolution[1] / 2)))
		screen.blit(quit_text, (int(resolution[0] / 2 - 75), int(resolution[1] / 2 + 120)))	 	

		if main_menu_button.collidepoint((mx,my)):
			if isClicking:
				ResetEndless()
				main_menu()
		if continue_button.collidepoint((mx,my)):
            if isClicking:
                paused = False
        if quit_button.collidepoint((mx,my)):
        	if isClicking:		
        		pygame.quit()
        		sys.exit()

		for event in pygame.event.get():
	 		if event.type == pygame.QUIT:
	 			pygame.quit()
	 			sys.exit()
	 		elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					isClicking = True
	
			elif event.type == pygame.MOUSEBUTTONUP:
				isClicking = False

		pygame.display.flip()
		clock.tick(10)