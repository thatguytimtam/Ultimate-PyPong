import pygame, math

#### PYGAME AND WINDOW INIT. ####
pygame.init()
pygame.font.init()
winWidth, WinHeight = 800, 500

win = pygame.display.set_mode((winWidth, WinHeight))
pygame.display.set_caption('PyPong')
clock = pygame.time.Clock()
font1 = pygame.font.SysFont('Calibri', 25)
#### PYGAME AND WINDOW INIT. ####

#### STATIC SPRITES ####
player_purple = pygame.image.load("assets/sprites/player_purple.png").convert_alpha()
player_red = pygame.image.load("assets/sprites/player_red.png").convert_alpha()

background = pygame.image.load("assets/sprites/background.png").convert_alpha()

ball_surface = pygame.image.load("assets/sprites/ball.png").convert_alpha()
#### STATIC SPRITES ####


#### CLASSES ####
class Players:
	def __init__(self, x1, y1, x2, y2, speed, sprite1, sprite2):
		# x1, y1 => player 1's x and y
		# x2, y2 => player 2's x and y

		self.x1 = x1
		self.y1 = y1

		self.x2 = x2
		self.y2 = y2

		self.sprite1 = sprite1
		self.sprite2 = sprite2

		self.rect1 = self.sprite1.get_rect(center = (self.x1, self.y1)) # create a rectangle around both player sprites
		self.rect2 = self.sprite2.get_rect(center = (self.x2, self.y2)) # to handle collisions and movement

		self.speed = speed

	def draw(self):
		win.blit(self.sprite1, self.rect1) # display player 1
		win.blit(self.sprite2, self.rect2) # display player 2
	
	def handle_movement(self):
		keys = pygame.key.get_pressed() # shortcut for keys
		if keys[pygame.K_w] and self.rect1.midtop[1] >= 0:
			self.rect1.y -= self.speed # increasing the y value while checking if rect is not out of bounds
		if keys[pygame.K_s] and self.rect1.midbottom[1] <= WinHeight:
			self.rect1.y += self.speed 

		if keys[pygame.K_UP] and self.rect2.midtop[1] >= 0:
			self.rect2.y -= self.speed # increasing the y value while checking if rect is not out of bounds
		if keys[pygame.K_DOWN] and self.rect2.midbottom[1] <= WinHeight:
			self.rect2.y += self.speed 
		
class Environment:
	def __init__(self, bgx, bgy):
		self.bgx = bgx
		self.bgy = bgy
		self.bg = background
	def draw(self):
		win.blit(background, (self.bgx, self.bgy))
		self.bgx -= 1
		self.bgy += 1
		if self.bgx <= -1400:
			self.bgx = 0
			self.bgy = -1000

class Ball:
	def __init__(self, x, y, speed, sprite):
		self.x = x
		self.y = y

		self.speed = speed
		
		self.sprite = sprite
		self.rect = self.sprite.get_rect(center = (winWidth/2, WinHeight/2))
	
	def draw(self):
		win.blit(self.sprite, self.rect)

#### CLASSES ####

#### CLASS INIT. ####
players = Players(50, WinHeight/2, winWidth - 50, WinHeight / 2, 4, player_purple, player_red)
env = Environment(0, -1000)
ball = Ball(winWidth/2, WinHeight/2, 2, ball_surface)
#### CLASS INIT. ####

#### STATIC VARIABLES ####
gameActive = True
#song1 = pygame.mixer.Sound('assets/music/song1.mp3')
#song1.play(loops = -1)

#### STATIC VARIABLES ####

#### --------------------------------------------------------------------------------------- GAME LOOP ####
while True:
	win.fill((199, 236, 238))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()

	env.draw()

	#### TITLE SCREEN ####
	if gameActive == False: 
		pass

	#### TITLE SCREEN ####


	
	#### MAIN GAME ####
	else:
		players.draw()
		players.handle_movement()
		ball.draw()

	#### MAIN GAME ####

	pygame.display.update()
	clock.tick(240)
