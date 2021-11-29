import pygame
import random
import time
from os import path

img_dir = path.join(path.dirname(__file__), '.')
snd_dir = path.join(path.dirname(__file__), '.')

WIDTH = 1000
HEIGHT = 800
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate rafting")
clock = pygame.time.Clock()


def newmob(mob_type):
	m = Mob(mob_type)
	all_sprites.add(m)
	mobs.add(m)


def newtrash():
	t = Trash()
	all_sprites.add(t)
	trash.add(t)


def newfish(fish_img, dir="left"):
	f = Fish(fish_img, dir)
	all_sprites.add(f)
	fish.add(f)


def draw_shield_bar(surf, x, y, pct):
	if pct < 0:
		pct = 0
	BAR_LENGTH = 300
	BAR_HEIGHT = 10
	fill = (pct / 100) * BAR_LENGTH
	outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
	fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surf, RED, fill_rect)
	pygame.draw.rect(surf, WHITE, outline_rect, 2)


class Player(pygame.sprite.Sprite):
	def __init__(self, rocks=15):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.images.append(pygame.image.load('fisherman1_anim.png'))
		self.images.append(pygame.image.load('fisherman2_anim.png'))
		self.images.append(pygame.image.load('fisherman3_anim.png'))
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0
		self.speedy = 0
		self.shield = 100
		self.rocks = rocks
		self.last_shot = pygame.time.get_ticks()
		self.last_index = pygame.time.get_ticks()
		self.shoot_event = pygame.USEREVENT + 1
		pygame.time.set_timer(self.shoot_event, 500)

	def update(self):
		# when the update method is called, we will increment the index
		now = pygame.time.get_ticks()
		if now - self.last_index > 150:
			self.last_index = now
			self.index += 1

		# if the index is larger than the total images
		if self.index >= len(self.images):
			# we will make the index to 0 again
			self.index = 0

		# finally we will update the image that will be displayed
		self.image = self.images[self.index]

		""" движение лодки с рыбаком
		 Ввверх, вниз, вправо, влево
		            WASD"""
		self.speedx = 0
		self.speedy = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_a]:
			self.speedx = -7
		if keystate[pygame.K_d]:
			self.speedx = 7
		if keystate[pygame.K_w]:
			self.speedy = -7
		if keystate[pygame.K_s]:
			self.speedy = +7
		if keystate[pygame.K_SPACE]:
			if self.rocks > 0:
				self.shoot()
		# if keystate[pygame.K_ESCAPE]:
		# 	pause()
		# if keystate[pygame.K_RETURN]:
		# 	paused=False

		self.rect.x += self.speedx
		self.rect.y += self.speedy

		# Делаем так, чтобы рыбак не выходил за рамки экрана
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.y > WIDTH:
			self.rect.y = WIDTH
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT
		if self.rect.top < 0:
			self.rect.top = 0

	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > 350:
			self.last_shot = now
			bullet = Bullet(self.rect.centerx, self.rect.top)
			all_sprites.add(bullet)
			bullets.add(bullet)
			self.rocks -= 1
			random.choice(thr_sound).play()




class Trash(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = trash_img
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(0, HEIGHT)


class Fish(pygame.sprite.Sprite):
	def __init__(self, fish_type, dir="left"):
		pygame.sprite.Sprite.__init__(self)
		self.image = fish_type
		self.image = pygame.transform.scale(self.image, (100, 50))
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(0, WIDTH)
		self.rect.y = random.randrange(0, HEIGHT)
		if dir == "left":
			self.speedx = random.randrange(-3, 1)
		else:
			self.speedx = random.randrange(1, 3)

	def update(self):
		self.rect.x += self.speedx
		if self.rect.left < -100 or self.rect.right > WIDTH + 100:
			self.rect.x = random.randrange(0, WIDTH)
			self.rect.y = random.randrange(0, HEIGHT)


class Mob(pygame.sprite.Sprite):
	def __init__(self, mob_type):
		pygame.sprite.Sprite.__init__(self)
		self.mob_type = mob_type
		self.images = {1:[pygame.image.load('monster1_anim.png'),pygame.image.load('monster2_anim.png'),pygame.image.load('monster3_anim.png')], 2:[pygame.image.load('monstraka1_anim.png'), pygame.image.load('monstraka2_anim.png')]}
		self.index = 0
		self.image = self.images[self.mob_type][self.index]
		# self.image = pygame.transform.scale(self.image, (100, 50))
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 8)
		self.speedx = random.randrange(-3, 3)
		self.last_index = pygame.time.get_ticks()

	def update(self):
		# when the update method is called, we will increment the index
		now = pygame.time.get_ticks()
		if now - self.last_index > 150:
			self.last_index = now
			self.index += 1

		# if the index is larger than the total images
		if self.index >= len(self.images[self.mob_type]):
			# we will make the index to 0 again
			self.index = 0

		# finally we will update the image that will be displayed
		self.image = self.images[self.mob_type][self.index]
		self.image = pygame.transform.scale(self.image, (130, 81))

		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -4)
			self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10, 20))
		self.image = rock_img
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		# убить, если он заходит за верхнюю часть экрана
		if self.rect.bottom < 0:
			self.kill()


#
# def print_text(message, x, y, font_color=BLACK, font_type='7fonts.ru_Raiders.ttf', font_size=30):
# 	font_type = pygame.font.Font(font_type, font_size)
# 	text = font_type.render(message, True, font_color)
# 	screen.blit(text, (x, y))


# def pause():
# 	paused = True
# 	while paused:
# 		clock.tick(FPS)
# 		for event in pygame.event.get():
# 			if event.type == pygame.QUIT:
# 				paused = False
#
# 		keys = pygame.key.get_pressed()
# 		if keys[pygame.K_RETURN]:
# 			paused = False
# 		print_text('PAUSED. PRESS ENTER TO CONTINUE', 1600, 3000)
# 		all_sprites.update()


font_name = pygame.font.match_font('7fonts.ru_Raiders.ttf')


def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)


def show_go_screen():
	screen.blit(background, background_rect)
	draw_text(screen, "Ultimate rafting", 128, WIDTH / 2, HEIGHT / 4)
	draw_text(screen, "Press Enter to start", 70, WIDTH / 2, HEIGHT / 2)
	draw_text(screen, "548    10R    it_class", 40, WIDTH / 2, HEIGHT * 3 / 4)
	if start_time > 0:
		draw_text(screen, f"Your time: {int(time.time() - start_time)} seconds", 40, WIDTH / 2, HEIGHT * 3 / 5)
	if score_f > 0:
		draw_text(screen, f"Your score: {score_f}", 40, WIDTH / 2, HEIGHT * 3 / 4.5)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RETURN:
					waiting = False


background = pygame.image.load(path.join(img_dir, 'background.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "fisherman1.png")).convert()
monster_img = pygame.image.load(path.join(img_dir, "monsterF.png")).convert()
blue_monster_img = pygame.image.load(path.join(img_dir, "blue_monster.png")).convert_alpha()
green_monster_img = pygame.image.load(path.join(img_dir, "green_monster.png")).convert_alpha()
trash_img = pygame.image.load(path.join(img_dir, "trash.png")).convert()
fish_img1 = pygame.image.load(path.join(img_dir, "gold_fish1.png")).convert_alpha()
fish_img2 = pygame.image.load(path.join(img_dir, "blue_fish.png")).convert_alpha()
fish_img3 = pygame.image.load(path.join(img_dir, "green_fish.png")).convert_alpha()
rock_img = pygame.image.load(path.join(img_dir, "rock.png")).convert_alpha()
icon_img = pygame.image.load(path.join(img_dir, "icon.png")).convert()

pygame.display.set_icon(icon_img)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
trash = pygame.sprite.Group()
fish = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player(10)
all_sprites.add(player)
all_sprites.add(player)
for i in range(1):
	newmob(random.randint(1, 2))
	newtrash()
	newfish(fish_img1)

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'minecraft-death-sound.mp3'))
expl_sounds = []
for snd in ['minecraft-death-sound.mp3']:
	expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

plus_sound = pygame.mixer.Sound(path.join(snd_dir, 'vyibor-nujnogo-deystviya.wav'))
pls_sound = []
for snd in ['vyibor-nujnogo-deystviya.wav']:
	pls_sound.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

throwing_sound = pygame.mixer.Sound(path.join(snd_dir, 'wood-rod-swing-whoosh_f1eqgq4d.mp3'))
thr_sound = []
for snd in ['wood-rod-swing-whoosh_f1eqgq4d.mp3']:
	thr_sound.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

pygame.mixer.music.load(path.join(snd_dir, 'treasure hun2t.mp3'))
pygame.mixer.music.set_volume(0.2)
score = 0
start_time = 0
score_f = 0
fish_dic = {1: (fish_img1, "left"), 2: (fish_img2, "left"), 3: (fish_img3, "right")}
monster_dic = {1: monster_img, 2: green_monster_img}
pygame.mixer.music.play(loops=-1)
running = True
game_over = True
while running:
	if game_over:
		show_go_screen()
		all_sprites = pygame.sprite.Group()
		mobs = pygame.sprite.Group()
		trash = pygame.sprite.Group()
		fish = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		powerups = pygame.sprite.Group()
		start_time = time.time()
		score_f = 0
		game_over = False
		player = Player(10)
		all_sprites.add(player)
		newtrash()
		newfish(fish_img2)

		for i in range(4):
			newmob(random.randint(1, 2))
		score = 0

	# if event.type == pygame.KEYDOWN:
	# 	print("KEYDOWN", event.key)
	# 	# if event.key == pygame.K_e:
	# 	print("K_SPACE")
	# 	player.shoot()
	clock.tick(FPS)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# event_shoot()

	all_sprites.update()

	hits_b = pygame.sprite.groupcollide(bullets, mobs, True, True)
	for hit in hits_b:
		print(hit)
		moster_obj = monster_dic[random.randint(1, 2)]
		newmob(random.randint(1, 2))
	# m = Mob()
	# all_sprites.add(m)
	# mobs.add(m)

	hits_m = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
	for hit in hits_m:
		random.choice(expl_sounds).play()
		player.shield -= 30
		moster_obj = monster_dic[random.randint(1, 2)]
		newmob(random.randint(1, 2))
		if player.shield <= 0:
			game_over = True
	# running = False

	hits_f = pygame.sprite.spritecollide(player, fish, True, pygame.sprite.collide_circle)
	for hit in hits_f:
		random.choice(pls_sound).play()
		score_f += 1
		print(score_f)
		fish_obj = fish_dic[random.randint(1, 3)]
		newfish(fish_obj[0], fish_obj[1])

	hits_t = pygame.sprite.spritecollide(player, trash, True, pygame.sprite.collide_circle)
	for hit in hits_t:
		random.choice(pls_sound).play()
		newtrash()
		if player.shield < 100:
			# player.shield += hit.radius * 1.5
			player.shield = 100

	screen.fill(BLACK)
	screen.blit(background, background_rect)
	all_sprites.draw(screen)
	draw_shield_bar(screen, 5, 5, player.shield)
	draw_text(screen, f"Rocks: {player.rocks}", 35, 930, 10)
	pygame.display.flip()

pygame.quit()