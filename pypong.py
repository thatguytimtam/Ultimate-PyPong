import pygame, random, math, time

#### PYGAME AND WINDOW INIT. ####
pygame.init()
pygame.font.init()
winWidth, WinHeight = 800, 500

win = pygame.display.set_mode((winWidth, WinHeight))
pygame.display.set_caption('PyPong')
clock = pygame.time.Clock()
font = pygame.font.Font('assets/fonts/Market_Deco.ttf', 36)
#### PYGAME AND WINDOW INIT. ####

#### STATIC SPRITES ####
player_purple = pygame.image.load("assets/sprites/player_purple.png").convert_alpha()
player_red = pygame.image.load("assets/sprites/player_red.png").convert_alpha()
player_shadow = pygame.image.load("assets/sprites/player_shadow.png").convert_alpha()

background = pygame.image.load("assets/sprites/background.png").convert_alpha()
title_text = pygame.image.load("assets/fonts/title.png")

ball_surface = pygame.image.load("assets/sprites/ball.png").convert_alpha()
ball_shadow = pygame.image.load("assets/sprites/ball_shadow.png").convert_alpha()

start_btn = pygame.image.load("assets/sprites/start_btn.png").convert_alpha()
start_btn_black = pygame.image.load("assets/sprites/start_btn_black.png").convert_alpha()

vignette = pygame.image.load("assets/sprites/vignette.png").convert_alpha()

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

		win.blit(player_shadow, (self.rect1[0] + 30, self.rect1[1] - 50))
		win.blit(player_shadow, (self.rect2[0] + 30, self.rect2[1] - 50))
	
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
	def __init__(self, bgx, bgy, speed, title_x, title_y):
		self.bgx = bgx
		self.bgy = bgy
		self.bg = background
		self.speed = speed
		self.title_x = title_x
		self.title_y = title_y
		self.title_rect = title_text.get_rect(center = (self.title_x, self.title_y))
		self.btn_rect = start_btn.get_rect(center = (winWidth/2, 400))


	def draw_background(self):
		win.blit(background, (self.bgx, self.bgy))
		self.bgx -= self.speed
		self.bgy += self.speed
		if self.bgx <= -1400:
			self.bgx = 0
			self.bgy = -1000
		
		win.blit(vignette, (0,0))

	def draw_title(self):
		win.blit(title_text, self.title_rect)

	def draw_playbutton(self):
		win.blit(start_btn, self.btn_rect)
		cursor_rect = ball_surface.get_rect(center = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
		
		if cursor_rect.colliderect(self.btn_rect):
			win.blit(start_btn_black, self.btn_rect)
			return True
		else:
			win.blit(start_btn, self.btn_rect)
			return False

players = Players(50, WinHeight/2, winWidth - 50, WinHeight / 2, 5, player_purple, player_red)
class Ball:
	def __init__(self, x, y, yspeed, xspeed, sprite, respawn_timer):
		self.x = x
		self.y = y

		self.xspeed = xspeed
		self.yspeed = yspeed
		
		self.sprite = sprite
		self.rect = self.sprite.get_rect(center = (winWidth/2 + 1000, WinHeight/2))

		self.repsawn_timer = respawn_timer
		self.hasScored = False
	
	def draw(self):
		win.blit(self.sprite, self.rect)
		win.blit(ball_shadow, (self.rect[0] + 30, self.rect[1] - 50))

	
	def move(self):
		global score1, score2
		print(self.rect.x)
		self.rect.x += self.xspeed
		self.rect.y += self.yspeed
		if self.rect.y >= WinHeight-10:
			self.yspeed = -self.yspeed
		#if self.rect.x >= winWidth-10:
		#	self.xspeed = -self.xspeed
		if self.rect.y <= 0:
			self.yspeed = -self.yspeed
		#if self.rect.x <= 0:
		#	self.xspeed = -self.xspeed
		
		if self.rect.colliderect(players.rect1) or self.rect.colliderect(players.rect2):
			if self.rect.colliderect(players.rect1):
				self.rect.x = 60
			elif self.rect.colliderect(players.rect2):
				self.rect.x = winWidth - 80
			self.xspeed = -self.xspeed
			if self.xspeed > 0: self.xspeed += 0.2
			if self.xspeed < 0: self.xspeed -= 0.2
			if self.yspeed > 0: self.yspeed += 0.2
			if self.yspeed < 0: self.yspeed -= 0.2

		if self.rect.x > winWidth or self.rect.x < 0:
			if self.rect.x > winWidth and self.hasScored == False:
				score1 += 1
				self.hasScored = True
			elif self.rect.x < 0 and self.hasScored == False:
				score2 += 1
				self.hasScored = True
			players.speed = 1
			env.speed = 0.1
			self.repsawn_timer += 1
			if self.repsawn_timer > 500 and self.repsawn_timer < 1000:
				self.xspeed = 0
				self.yspeed = 0
				win.blit(ball_surface, (winWidth/2 - 10, WinHeight/2 - 10))
			if self.repsawn_timer > 1000:
				players.speed = 4
				env.speed = 1
				self.repsawn_timer = 0
				if self.rect.x > 1000:
					self.xspeed, self.yspeed = -2, 2
				else:
					self.xspeed, self.yspeed = 2, 2
				self.rect.x, self.rect.y = winWidth/2, WinHeight/2
				self.hasScored = False


ball = Ball(winWidth/2, WinHeight/2, 1, 1, ball_surface, 0)

class ParticlePrinciple:
	def __init__(self):
		self.particles = []

	def emit(self):
		if self.particles:
			self.delete_particles()
			for particle in self.particles:
				particle[0][1] += particle[2][0]
				particle[0][0] += particle[2][1]
				particle[1] -= 0.08
				pygame.draw.circle(win,(255,255,255),particle[0], int(particle[1]))

	def add_particles(self):
		pos_x = ball.rect.x + 10
		pos_y = ball.rect.y + 10
		radius = 10
		direction_x = 0
		direction_y = 0
		

		particle_circle = [[pos_x,pos_y],radius,[direction_x,direction_y]]
		self.particles.append(particle_circle)

	def delete_particles(self):
		particle_copy = [particle for particle in self.particles if particle[1] > 0]
		self.particles = particle_copy

particle1 = ParticlePrinciple()

#### CLASSES ####

#### CLASS INIT. ####
env = Environment(0, -1000, 2, winWidth/2, 100)
#### CLASS INIT. ####

#### STATIC VARIABLES ####
gameActive = False
#song1 = pygame.mixer.Sound('assets/music/song1.mp3')
#song1.play(loops = -1)
FPS = 240

score1, score2 = -1,0
#### STATIC VARIABLES ####

#### --------------------------------------------------------------------------------------- GAME LOOP ####
while True:
	win.fill((199, 236, 238))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		if event.type == pygame.MOUSEBUTTONDOWN and env.draw_playbutton() == True:
			gameActive = True

	env.draw_background()
	env.draw_title()

	#### TITLE SCREEN ####
	if gameActive == False: 
		env.draw_playbutton()

			

	#### TITLE SCREEN ####


	
	#### MAIN GAME ####
	else:
		score_text = font.render(f'{score1}:{score2}', True, (0,0,0))
		win.blit(score_text, (winWidth/2 - score_text.get_width()/2, 100))
		if env.title_rect.y > -500:
			env.title_rect.y -= 1
		
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			gameActive = False

	
		players.draw()
		players.handle_movement()
		particle1.add_particles()
		particle1.emit()
		ball.draw()
		ball.move()

	#### MAIN GAME ####

	pygame.display.update()
	clock.tick(FPS)
