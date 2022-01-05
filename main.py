##########################################################################
### Imports
##########################################################################
import pygame
from pygame.locals import *

import sys
import os
 
from meteor import Meteor
import player
import random
import star

##########################################################################
###		Main Variables
##########################################################################
pygame.init()
pygame.display.set_caption("PyGame")

pygame.font.init()
score_font = pygame.font.SysFont('Segoe UI', 45)
main_font = pygame.font.SysFont("Helvetica", 50)
main_font_bold = pygame.font.SysFont("Helvetica", 50, True)

resolution = (1500, 700)
BLACK = (0,0,0)
WHITE = (255,255,255)

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

##########################################################################
###		Game Variables
##########################################################################
background = pygame.Surface(resolution)
background.fill((255, 255, 255))

bottom_border = pygame.transform.scale(pygame.image.load(os.path.join(sys.path[0], "assets\\gradient.jfif")), (1800, 100))

player = player.Player()
player.rect.x = int(screen.get_width() / 2)
player.rect.y = int(screen.get_height() / 2)

spritegroup = pygame.sprite.Group()
met_spritegroup = pygame.sprite.Group()

max_timer = 100
timer = max_timer

met_maxtimer = 100
met_timer = met_maxtimer

pos = ()  
pressed = {}
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
            pass
            # file = open(os.path.join(sys.path[0], "best_score.txt"), "w")
        # file.write(str(score))
    except Exception as e:
        print(f"Internal Error: {e}")
        pygame.quit()
        sys.exit(-1)

    timer = max_timer
    met_timer = met_maxtimer
    game.ResetScore()

class EndlessMode():

    def __init__(self, player, timer, max_timer, met_timer, met_maxtimer, spritegroup, met_spritegroup):
        self.player = player
        self.timer = timer
        self.max_timer = max_timer
        self.met_timer = met_timer
        self.met_maxtimer = met_maxtimer
        self.spritegroup = spritegroup
        self.met_spritegroup = met_spritegroup
        self.score_text = score_font.render(str(0), False, (0, 0, 0))

    def ResetScore(self):
        self.score = 0
        self.score_text = score_font.render(str(0), False, (0, 0, 0))

    def Game(self):
        self.score = 0
        self.score_text = score_font.render(str(0), False, (0, 0, 0))

        running = True

        while running: 

            screen.blit(background, (0,0))
            screen.blit(bottom_border, (-100, 610))
            screen.blit(self.score_text,(40, 25))
            self.spritegroup.draw(screen)
            self.met_spritegroup.draw(screen)
            screen.blit(self.player.image, self.player.rect)

            pygame.display.flip()

            self.player.gravity += 0.08

            # Top border
            if self.player.rect.y <= 0:
                self.player.gravity = 1

            # Bottom border
            if self.player.rect.y >= resolution[1] - 90:
                ResetEndless()

            self.player.velocity = [self.player.velocity_x, self.player.gravity]
            self.player.rect = self.player.rect.move(self.player.velocity)

            for meteor in self.met_spritegroup:
                # Check if not in screen
                if meteor.rect.x > resolution[0] or meteor.rect.x < 0 or meteor.rect.y > resolution[1] or meteor.rect.y < -50:
                    self.met_spritegroup.remove(meteor)

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
                if pygame.sprite.collide_circle(self.player, meteor) == True:
                    ResetEndless()

            if self.timer <= 0:
                new_star = star.Star(random.randint(10, resolution[0]), random.randint(50, resolution[1] - 50))
                self.spritegroup.add(new_star)
                self.timer = self.max_timer
            else:
                self.timer -= 1

            if self.met_timer <= 0:
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
                self.met_spritegroup.add(new_met)
                self.met_timer = met_maxtimer
            else:
                self.met_timer -= 1

            if pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
                self.player.rect.x += self.player.speed
            elif pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
                self.player.rect.x -= self.player.speed

            for test_star in self.spritegroup:
                if pygame.sprite.collide_circle(self.player, test_star) == True:
                    self.score += 1
                    self.score_text = score_font.render(str(self.score), False, (0, 0, 0))
                    self.spritegroup.remove(test_star)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    pressed[event.key] = True

                    if event.key == pygame.K_SPACE:
                        self.player.gravity = 0
                        self.player.gravity -= 5

                    elif event.key == pygame.K_ESCAPE:
                        pause()

                elif event.type == pygame.KEYUP:
                    pressed[event.key] = False    

            if self.player.rect.y >= 920:
                ResetEndless()

            clock.tick(60)

def main_menu():
    global game

    endless_button = pygame.Rect((int(resolution[0] / 2 - 100), int(resolution[1] / 2 - 120)),(200, 100))
    levels_button = pygame.Rect((int(resolution[0] / 2 - 100), int(resolution[1] / 2)), (200, 100)) 
    quit_button = pygame.Rect((int(resolution[0] / 2 - 100), int(resolution[1] / 2 + 120)),(200, 100)) 

    # Text
    endless_text = main_font.render('Endless', False, (150, 150, 150))
    levels_text = main_font.render('Levels', False, (150, 150, 150))
    quit_text = main_font.render('Quit', False, (150, 150, 150))

    background = pygame.Surface(resolution)
    background.fill((255, 255, 255))

    isClicking = False

    while True:
        mx, my = pygame.mouse.get_pos()

        screen.blit(background,(0,0))

        pygame.draw.rect(screen, (128, 128, 128, 10), endless_button)
        pygame.draw.rect(screen, (128, 128, 128, 10), levels_button)
        pygame.draw.rect(screen, (128, 128, 128, 10), quit_button)

        screen.blit(endless_text, (int(resolution[0] / 2 - 75), int(resolution[1] / 2 - 120)))
        screen.blit(levels_text, (int(resolution[0] / 2 - 75), int(resolution[1] / 2)))
        screen.blit(quit_text, (int(resolution[0] / 2 - 75), int(resolution[1] / 2 + 120)))

        pygame.display.flip()

        if endless_button.collidepoint((mx ,my)):
            if isClicking:
                game = EndlessMode(player, timer, max_timer, met_timer, met_maxtimer, spritegroup, met_spritegroup)
                game.Game()
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
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    isClicking = True
    
            elif event.type == pygame.MOUSEBUTTONUP:
                isClicking = False

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

    isClicking = False

    while paused:
        mx, my = pygame.mouse.get_pos()
        screen.fill((255,255,255))

        pygame.draw.rect(screen, (128, 128, 128, 10), continue_button)
        pygame.draw.rect(screen, (128, 128, 128, 10), main_menu_button)
        pygame.draw.rect(screen, (128, 128, 128, 10), quit_button)

        screen.blit(paused_text, (int(resolution[0] / 2 - 100), int(resolution[1] / 2 - 300)))
        screen.blit(continue_text, (int(resolution[0] / 2 - 100), int(resolution[1] / 2 - 120)))
        screen.blit(main_menu_text, (int(resolution[0] / 2 - 100), int(resolution[1] / 2)))
        screen.blit(quit_text, (int(resolution[0] / 2 - 100), int(resolution[1] / 2 + 120)))

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

if __name__ == "__main__":
    
    main_menu()
