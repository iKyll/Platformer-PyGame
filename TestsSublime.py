<<<<<<< HEAD
def ResetEndless():

	for met in met_spritegroup:
		met_spritegroup.remove(met)
	for stars in spritegroup:
		spritegroup.remove(stars)

	player.rect.x = screen.get_width() / 2
	player.rect.y = screen.get_height() / 2

	try:
		if file == None:
			file = open(os.path.join(sys.path[0], "best_score.txt"), "w")
		file.write(score)
		file.close()
	except Exception as e:
		print(f"Internal Error: {e}")
		pygame.quit()
		sys.exit(-1)

	timer = max_timer
	met_timer = met_maxtimer
=======
def ResetEndless():

	for met in met_spritegroup:
		met_spritegroup.remove(met)
	for stars in spritegroup:
		spritegroup.remove(stars)

	player.rect.x = screen.get_width() / 2
	player.rect.y = screen.get_height() / 2

	try:
		if file == None:
			file = open(os.path.join(sys.path[0], "best_score.txt"), "w")
		file.write(score)
		file.close()
	except Exception as e:
		print(f"Internal Error: {e}")
		pygame.quit()
		sys.exit(-1)

	timer = max_timer
	met_timer = met_maxtimer
>>>>>>> 6571de9e508e58876eddac8004a3e59f6acda9e6
	score = 0