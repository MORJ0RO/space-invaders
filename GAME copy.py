import pygame
import os.path
import math
import random
import sys

from os import stat_result
from pygame import mixer
from pygame import mixer_music

from components.score import Score
from components.bullet import Bullet
from components.enemy import Enemy
from components.player import Player

BASE_PATH = os.path.dirname(__file__)
ASSETS_PATH = os.path.join(BASE_PATH, "assets")

SCREEN_X = 800
SCREEN_Y = 600
SCREEN = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

COLORS = {
    'darkblue': pygame.Color(12, 20, 69),
    'lightpurple': pygame.Color(92, 84, 164),
    'white': pygame.Color(255, 255, 255)
}

pygame.init()

# Screen
pygame.display.set_caption("SPACE INVADERS")
window = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
window_icon = pygame.image.load(os.path.join(ASSETS_PATH, "icon.png"))

# Score
score_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.Font('freesansbold.ttf', 20)

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 69)

def show_score(x, y):
    score = font.render("Points: " + str(score_val),
                        True, (255,255,255))
    SCREEN.blit(score, (x , y ))
 
def game_over():
    game_over_text = game_over_font.render("GAME OVER",
                                           True, (255,255,255))
    SCREEN.blit(game_over_text, (190, 250))

# Background Sound
mixer.music.load(os.path.join(ASSETS_PATH, "background.wav"))
mixer.music.play(-1)

# Player
player_X = 370
player_Y = 523
player_Xchange = 0
player = Player (
     image = pygame.image.load(os.path.join(ASSETS_PATH, "player.gif")),
     speed = 15
)
 # type: ignore

# Enemy
invaderImage = []
invader_X = []
invader_Y = []
invader_Xchange = []
invader_Ychange = []
no_of_invaders = 8

Enemy_image = pygame.image.load(os.path.join(ASSETS_PATH, "enemy.gif"))

for num in range(no_of_invaders):
    invaderImage.append(pygame.image.load(os.path.join(ASSETS_PATH, "enemy.gif")))
    invader_X.append(random.randint(64, 737))
    invader_Y.append(random.randint(30, 180))
    invader_Xchange.append(1.2)
    invader_Ychange.append(50)

enemy = Enemy (
     image = pygame.image.load(os.path.join(ASSETS_PATH, "enemy.gif"))
)

# Bullet
bullet_X = 0
bullet_Y = 500
bullet_Xchange = 0
bullet_Ychange = 3
bullet_state = "rest"
bullet = Bullet (
     image = pygame.image.load(os.path.join(ASSETS_PATH, "bullet.png"))
)

# Score
score = Score(
     font = pygame.font.SysFont('freesansbold.ttf', 20),
     color = COLORS['lightpurple']
)

# Collision Concept
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2,2)) +
                         (math.pow(y1 - y2,2)))
    if distance <= 50:
        return True
    else:
        return False

def player(x, y):
    SCREEN.blit(Player_image, (x - 16, y + 10))

def enemy(x, y, i):
     SCREEN.blit(Enemy_image[i], (x, y))

def bullet(x, y):
    global bullet_state
    SCREEN.blit(bulletImage, (x, y))
    bullet_state = "fire"


# Game loop
running = True
while running:
    SCREEN.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Player movements
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_Xchange = -1.7
            if event.key == pygame.K_RIGHT:
                player_Xchange = 1.7
            if event.key == pygame.K_SPACE:
                 if bullet_state == "rest":
                      bullet_X = player_X
                      bullet(bullet_X, bullet_Y)
                      bullet_sound = mixer.Sound('data/shoot.wav')
                      bullet_sound.play()
        if event.type == pygame.KEYUP:
             player_Xchange = 0

    player_X += player_Xchange
    for i in range(no_of_invaders):
         invader_X[i] += invader_Xchange[i]

    if bullet_Y <= 0:
         bullet_Y = 600
         bullet_state = "rest"
    if bullet_state == "fire":
         bullet(bullet_X, bullet_Y)
         bullet_Y -= bullet_Ychange

    for i in range(no_of_invaders):
         if invader_Y[i] >= 450:
              if abs(player_X-invader_X[i]) < 80:
                   for j in range (no_of_invaders):
                        invader_Y[j] = 2000
                        explosion_sound = mixer.Sound('data/explosion.wav')
                        explosion_sound.play()
                   game_over()
                   break

    if invader_X[i] >= 735 or invader_X[i] <= 0:
         invader_Xchange[i] *= -1
         invader_Y[i] += invader_Ychange[i]
    collision = isCollision(bullet_X, invader_X[i], bullet_Y, invader_Y[i])
    if collision:
         score_val += 1
         bullet_Y = 600
         bullet_state = "rest"
         invader_X[i] = random.randint(64, 736)
         invader_Y[i] = random.randint(30, 200)
         invader_Xchange[i] *= -1

    enemy(invader_X[i], invader_Y[i], i)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            direction = event.key
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Fire a bullet
            bullet = Bullet(player.rect.x + player.rect.width/2, player.rect.y)
            bullets.append(bullet)
            shoot_sound.play()


if player_X <= 16:
     player_X = 16;
elif player_X >= 750:
    player_X = 750;

player(player_X, player_Y)
show_score(scoreX, scoreY)
pygame.display.update()

pygame.quit()
sys.exit(0)