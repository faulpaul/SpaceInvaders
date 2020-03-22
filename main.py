import pygame
import math
import random

# init pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# set background
background = pygame.image.load('media/img/background.png')

# set title & icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('media/img/icon.png')
pygame.display.set_icon(icon)

# set font
font = pygame.font.Font('freesansbold.ttf', 32)
gameoverfont = pygame.font.Font('freesansbold.ttf', 64)

# set player icon & location
playerImg = pygame.image.load('media/img/rocket.png')
playerX = 370
playerY = 480
playerXchange = 0
playerbullets = 100
playerbulletsTextX = 600
playerbulletsTextY = 10

# Score
scoreValue = 0
scoreTextX = 10
scoreTextY = 10

# set enemy icon & location
enemyImg = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
numOfEnemy = 6

for i in range(numOfEnemy):
    enemyImg.append(pygame.image.load('media/img/enemy.png'))
    enemyX.append(random.randint(40, 760))
    enemyY.append(random.randint(40, 140))
    enemyXchange.append(4)
    enemyYchange.append(8)

# set bullet icon & location
bulletImg = pygame.image.load('media/img/bullet.png')
bulletX = 0
bulletY = 480
bulletYchange = -10
bullet_state = 'ready'  # 'ready' = no bullet on screen, 'fire' = bullet on screen

# set sound
soundMusic = 'media/wav/music.wav'
soundLaser = pygame.mixer.Sound('media/wav/laser.wav')
soundExplosion = pygame.mixer.Sound('media/wav/explosion.wav')
soundEmpty = pygame.mixer.Sound('media/wav/blip_.wav')
# start music
pygame.mixer.music.load(soundMusic)
pygame.mixer.music.play(-1)  # -1 for infinite loop


def show_score(x, y):
    score = font.render('SCORE: ' + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_bullets(x, y):
    playerbulletcount = font.render('AMMO: ' + str(playerbullets), True, (255, 255, 255))
    screen.blit(playerbulletcount, (x, y))


def game_over_text():
    gameovertext = gameoverfont.render('GAME OVER', True, (255, 0, 0))
    screen.blit(gameovertext, (200, 250))


# draw player
def player(x, y):
    screen.blit(playerImg, (x, y))


# draw enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# draw bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


# collision check
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        print(distance)
        return True
    else:
        return False


# main game loop
running = True
while running:

    screen.fill((0, 0, 0))
    # load background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # if window is closed
        if event.type == pygame.QUIT:
            running = False
        # if key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXchange = -5  # move left
            if event.key == pygame.K_RIGHT:
                playerXchange = +5  # move right
            if event.key == pygame.K_SPACE:  # fire bullet
                if bullet_state is 'ready':
                    if playerbullets > 0:
                        playerbullets -= 1
                        bulletX = playerX
                        pygame.mixer.Sound.play(soundLaser)
                        fire_bullet(bulletX, bulletY)
                    else:
                        pygame.mixer.Sound.play(soundEmpty)

        # if key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerXchange = 0

    # player movement
    playerX += playerXchange
    if playerX > 800:
        playerX = 0
    elif playerX < 0:
        playerX = 800
    player(playerX, playerY)

    # enemy movement
    for i in range(numOfEnemy):

        # Game over
        if enemyY[i] > 440:
            for j in range(numOfEnemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyXchange[i]
        if enemyX[i] >= 768:
            enemyXchange[i] = enemyXchange[i] * -1
            enemyY[i] += enemyYchange[i]

        elif enemyX[i] <= 0:
            enemyXchange[i] = enemyXchange[i] * -1
            enemyY[i] += enemyYchange[i]

        # check collision
        collison = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collison:
            pygame.mixer.Sound.play(soundExplosion)
            print('Treffer')
            bulletY = 480
            bullet_state = 'ready'
            enemyX[i] = random.randint(40, 760)
            enemyY[i] = random.randint(40, 140)
            enemyXchange[i] = enemyXchange[i] + 1
            enemyYchange[i] = enemyYchange[i] + 1
            enemy
            scoreValue += 1
            playerbullets += 2

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= -10:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY += bulletYchange

    show_score(scoreTextX, scoreTextY)
    show_bullets(playerbulletsTextX, playerbulletsTextY)
    pygame.display.update()
