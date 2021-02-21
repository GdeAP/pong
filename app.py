# import

import pygame, sys, random
from settings import *

# init

pygame.init()

class App:
	def __init__(self):
		self.screen = pygame.display.set_mode((screen_width, screen_height))
		self.clock = pygame.time.Clock()
		self.running = True
		self.state = 'start'
		self.title = pygame.display.set_caption('Pong')
		self.ball_speed_x = 7 * random.choice((1, -1))
		self.ball_speed_y = 7 * random.choice((1, -1))
		self.player_speed = 0
		self.opponent_speed = 7
		self.player_score = 0
		self.opponent_score = 0 
		self.ball = pygame.Rect(screen_width/2 - 20, screen_height/2 - 15, 30, 30)
		self.player = pygame.Rect(screen_width - 25, screen_height/2 - 70, 10, 140)
		self.opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)
		self.score_time = None

	def run(self):
		while self.running:
			if self.state == 'start':
				self.start_events()
				self.start_update()
				self.start_draw()
			elif self.state == 'playing':
				self.playing_events()
				self.playing_update()
				self.playing_draw()
			else:
				self.running = False
			self.clock.tick(FPS)
		pygame.quit()
		sys.exit()

	### START FUNCTION ###

	def start_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				self.state = 'playing'

	def start_update(self):
		pass

	def start_draw(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				self.state = 'playing'

		self.screen.fill((0, 0, 0))
		game_font = pygame.font.Font("freesansbold.ttf", 32)
		text = game_font.render("SPACE", False, light_grey)
		self.screen.blit(text, (screen_width/2 - 60, screen_height/2 - 30))
		pygame.display.update()

	### PLAYING FUNCTION ###

	def playing_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					self.player_speed += 7
				if event.key == pygame.K_UP:
					self.player_speed -= 7
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_DOWN:
					self.player_speed -= 7
				if event.key == pygame.K_UP:
					self.player_speed += 7

	def playing_update(self):
		self.ball_animation()
		self.player_animation()
		self.opponent_ai()

		if self.score_time:
			self.ball_restart()

	def playing_draw(self):
		self.screen.fill(bg_color)

		pygame.draw.rect(self.screen, light_grey, self.player)
		pygame.draw.rect(self.screen, light_grey, self.opponent)
		pygame.draw.ellipse(self.screen, light_grey, self.ball)
		pygame.draw.aaline(self.screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

		game_font = pygame.font.Font("freesansbold.ttf", 32)
		player_text = game_font.render(f"{self.player_score}", False, light_grey)
		self.screen.blit(player_text, (screen_width/2 + 20, 50))
		opponent_text = game_font.render(f"{self.opponent_score}", False, light_grey)
		self.screen.blit(opponent_text, (screen_width/2 - 35, 50))

		pygame.display.flip()

	### OTHER FUNCTION ###

	def ball_restart(self):
		global current_time
		self.ball.center = (screen_width/2, screen_height/2)
		self.ball_speed_y *= random.choice((1, -1))
		self.ball_speed_x *= random.choice((1, -1))

		current_time = pygame.time.get_ticks()
		game_font = pygame.font.Font("freesansbold.ttf", 32)

		if current_time - self.score_time < 700:
			number_three = game_font.render("3", False, light_grey)
			self.screen.blit(number_three, (screen_width/2 - 8, screen_height/2 + 20))
		if 700 < current_time - self.score_time < 1400:
			number_two = game_font.render("2", False, light_grey)
			self.screen.blit(number_two, (screen_width/2 - 8, screen_height/2 + 20))
		if 1400 < current_time - self.score_time < 2700:
			number_one = game_font.render("1", False, light_grey)
			self.screen.blit(number_one, (screen_width/2 - 8, screen_height/2 + 20))

		if current_time - self.score_time < 2100:
			self.ball_speed_x, self.ball_speed_y = 0, 0
		else:
			self.ball_speed_x = 7 * random.choice((1, -1))
			self.ball_speed_y = 7 * random.choice((1, -1))
			self.score_time = None
			
		pygame.display.flip()

	def ball_animation(self):
		self.ball.x += self.ball_speed_x
		self.ball.y += self.ball_speed_y		

		if self.ball.top <= 0 or self.ball.bottom >= screen_height:
			self.ball_speed_y *= -1

		if self.ball.left <= 0:
			self.player_score += 1
			self.score_time = pygame.time.get_ticks()

		if self.ball.right >= screen_width:
			self.opponent_score += 1
			self.score_time = pygame.time.get_ticks()

		if self.ball.colliderect(self.player) and self.ball_speed_x > 0:
			if abs(self.ball.right - self.player.left) < 10:
				self.ball_speed_x *= -1
			elif abs(self.ball.bottom - self.player.top) < 10 and self.ball_speed_y > 0:
				self.ball_speed_y *= - 1
			elif abs(self.ball.top - self.player.bottom) < 10 and self.ball_speed_y < 0:
				self.ball_speed_y *= - 1

		if self.ball.colliderect(self.opponent) and self.ball_speed_x < 0:
			if abs(self.ball.left - self.opponent.right) < 10:
				self.ball_speed_x *= -1
			elif abs(self.ball.bottom - self.opponent.top) < 10 and self.ball_speed_y > 0:
				self.ball_speed_y *= - 1
			elif abs(self.ball.top - self.opponent.bottom) < 10 and self.ball_speed_y < 0:
				self.ball_speed_y *= - 1

	def player_animation(self):
		self.player.y += self.player_speed
		if self.player.top <= 0:
			self.player.top = 0
		if self.player.bottom >= screen_height:
			self.player.bottom = screen_height		

	def opponent_ai(self):
		if self.opponent.top < self.ball.y:
			self.opponent.top += self.opponent_speed
		if self.opponent.bottom > self.ball.y:
			self.opponent.bottom -= self.opponent_speed
		if self.opponent.top <= 0:
			self.opponent.top = 0
		if self.opponent.bottom >= screen_height:
			self.opponent.bottom = screen_height