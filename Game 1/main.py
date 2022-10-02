import pygame
import random
import pygame.mixer

pygame.mixer.init()

WIDTH = 1200
HEIGHT = 600
FPS = 60
PLAYERS_PIXEL_OFF_SCREEN = 40
PLAYERS_SPEED = (1, 2)
BACKGROUND_PATH = 'background.png'
BACKGROUND2_PATH = 'backgound2.png'
QUALIFY_AREA = 200
PLAYERS_LEFT = 32
PLAYER_POS = {1: (27, 133), 2: (30, 176), 3: (35, 229), 4: (41, 281), 5: (41, 336), 6: (41, 397), 7: (43, 461), 8: (35, 519), 9: (39, 571), 10: (40, 571), 11: (99, 574), 12: (98, 492), 13: (92, 440), 14: (101, 536), 15: (95, 406), 16: (87, 347), 17: (105, 276), 18: (88, 219), 19: (99, 162), 20: (94, 116), 21: (151, 570), 22: (141, 506), 23: (144, 463), 24: (141, 374), 25: (149, 340), 26: (157, 435), 27: (155, 251), 28: (153, 293), 29: (155, 161), 30: (159, 207), 31: (160, 208), 32: (154, 128)}
PLAYER_NO = random.randint(1, PLAYERS_LEFT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game 1")
clock = pygame.time.Clock()
background_image = pygame.transform.scale(pygame.image.load(BACKGROUND_PATH), (WIDTH-QUALIFY_AREA, HEIGHT))
background2_image = pygame.transform.scale(pygame.image.load(BACKGROUND2_PATH), (QUALIFY_AREA, HEIGHT))
font = pygame.font.Font('freesansbold.ttf', 32)
Music = pygame.mixer.Sound('Red Light Green Light.mp3')
timer = 60
start_ticks = pygame.time.get_ticks()

class Player(pygame.sprite.Sprite):
    def __init__(self, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = PLAYER_POS[id][0]
        self.rect.centery = PLAYER_POS[id][1]
        self.speedx = 0
        self.speed = 0

    def unmove(self):
        self.speed = random.randint(*PLAYERS_SPEED)

    def move(self):
        self.speedx = self.speed

    def update(self):
        self.rect.x += self.speedx

    def if_red_light(self):
        if self.speedx != 0:
            self.kill()

class AI(pygame.sprite.Sprite):
    def __init__(self, id):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = PLAYER_POS[id][0]
        self.rect.centery = PLAYER_POS[id][1]
        self.speedx = 0
        self.speed = 0

    def unmove(self):
        if self.if_die():
            self.speedx = self.speed
        else:
            self.speed = random.randint(*PLAYERS_SPEED)

    def move(self):
        self.speedx = self.speed

    def if_die(self):
        global PLAYERS_LEFT
        die_chance = random.randint(1, 456)
        return die_chance == 1

    def if_red_light(self):
        dies = self.if_die()
        if dies:
            self.move()
            self.update()
        if self.speedx != 0:
            self.kill()

    def update(self):
        self.rect.x += self.speedx


class Doll(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 4
        self.DOLL_ANIMATIONS = [*['doll_animations/0.png'] * self.speed, *['doll_animations/1.png'] * self.speed,
                                *['doll_animations/2.png'] * self.speed, *['doll_animations/3.png'] * self.speed,
                                *['doll_animations/4.png'] * self.speed, *['doll_animations/5.png'] * self.speed]
        self.red_light = True
        self.doll_frame_no = -1
        self.time_counter_light = 0
        self.GREEN_LIGHT_TO_RED_TIME = 100
        self.image = self.doll_animation()
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH-QUALIFY_AREA+(QUALIFY_AREA//2-12)
        self.rect.centery = HEIGHT//2+(QUALIFY_AREA//6)
        self.animation = False

    def doll_animation(self):
        if self.red_light:
            self.doll_frame_no += 1
            if self.doll_frame_no == len(self.DOLL_ANIMATIONS):
                self.doll_frame_no = len(self.DOLL_ANIMATIONS)-1
                self.animation = False
                self.red_light = not self.red_light
                self.GREEN_LIGHT_TO_RED_TIME = random.randint(60, 170)
                Music.play()
            return pygame.image.load(self.DOLL_ANIMATIONS[self.doll_frame_no])
        if not self.red_light:
            self.doll_frame_no -= 1
            if self.doll_frame_no == -1:
                self.doll_frame_no = 0
                self.animation = False
                self.red_light = not self.red_light
                self.GREEN_LIGHT_TO_RED_TIME = random.randint(50, 160)
                Music.stop()
            return pygame.image.load(self.DOLL_ANIMATIONS[self.doll_frame_no])
    def update(self):
        self.time_counter_light += 1
        if self.animation:
            self.image = self.doll_animation()
        if self.time_counter_light == self.GREEN_LIGHT_TO_RED_TIME:
            self.animation = True
            self.time_counter_light = 0
        if self.red_light:
            for i in player_sprites:
                i.if_red_light()

all_sprites = pygame.sprite.Group()
player_sprites = []
n = 1
for i in range(PLAYERS_LEFT):
    if i == PLAYER_NO:
        player = Player(PLAYER_NO)
        all_sprites.add(player)
    else:
        player = AI(i+1)
        all_sprites.add(player)
    player_sprites.append(player)

doll = Doll()
all_sprites.add(doll)

def time_min():
    global timer
    timer -= 1

# Game loop
running = True
while running:
    clock.tick(FPS)
    for p in player_sprites:
        p.speedx = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    mouse_click = pygame.mouse.get_pressed(3)
    if mouse_click[0]:
        for p in player_sprites:
            p.move()
    else:
        for p in player_sprites:
            p.unmove()

    all_sprites.update()
    screen.blit(background_image, (0, 0))
    screen.blit(background2_image, (WIDTH-QUALIFY_AREA, 0))
    timer = 60-(pygame.time.get_ticks()-start_ticks)//1000
    print(timer)
    screen.blit(font.render(f'{timer}', True, RED), (WIDTH-QUALIFY_AREA+10, 25))
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()