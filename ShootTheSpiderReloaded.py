# Name: Jonah Hoffman
# Date: 4/5/2023

from Constants import *
from time import sleep


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

running = True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load("wizard.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (93, 130))
        self.rect = self.surf.get_rect()
        self.rect.x = 500
        self.rect.y = 800
        self.lives = 3
        self.score = 0
        self.dead = False
    
    def update(self, pressed_keys):
        # Move player based on keypresses
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

    def death(self):
        self.dead = True
        self.lives -= 1


    def respawn(self):
        self.rect.x = 500
        pygame.transform.rotate(self.surf, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("spider.png").convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.x = -600
        self.rect.y = randint(80, 650)
        self.surf = pygame.transform.scale(self.surf, (150, 104))
        self.speed = randint(5, 15)

        # creates hitbox based on spider location
        self.hitbox = (self.rect.x + 35, self.rect.y, 110, 40)

        self.dead = False

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(self.speed, 0)
        self.hitbox = (self.rect.x + 35, self.rect.y, 110, 40)
        pygame.draw.rect(screen, (255,255, 255), self.hitbox,2)
        if self.rect.left > 1200:
            player.death()
            self.respawn()

    def deathAnimation(self):
        if self.rect.y < 880:
            self.rect.move_ip(0, 10)
        else:
            self.respawn()
            self.dead = False

    def respawn(self):
        self.rect.x = -300
        self.rect.y = randint(80, 650)

    # runs when spider is hit by bolt
    def hit(self):
        self.dead = True
        sleep(.5)
        player.score += 1

class Cast:
    def __init__(self):
        # creates surface for bolts
        self.surf = pygame.Surface((10, 40))
        self.surf.fill((200, 200, 200))
        self.rect = self.surf.get_rect()
        self.x = player.rect.x + 15
        self.y = player.rect.y + 25
 
    def update(self):
        # draws bolts on screenn each fre
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(self.x, self.y, 10, 40))
        if self.rect.x < 1200:
            self.y -= 25
        else:
            self.kill()

# instantiating some things
player = Player()
spider = Enemy()
font = pygame.font.SysFont('Comic Sans MS', 40)
bolts = []

# sprites groups player and spider together to make rendering easier
sprites = pygame.sprite.Group()
sprites.add(player)
sprites.add(spider)

clock = pygame.time.Clock()

# Main loop
while running:
    # set frame rate to 60 fps
    clock.tick(60)

    # checks number of lives and quits game if 0
    if player.lives == 0:
        running = False

    # stores what keys are pressed each frame
    pressed_keys = pygame.key.get_pressed()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # quits game when escape is pressed
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

            # casts bolts when spacebar is pressed
            if ((event.key == K_SPACE) & (spider.dead == False)):
                bolts.append(Cast())
                shootin = True

    # make sceen white each frame
    screen.fill((255, 255, 255))

    # update player each frame
    if ((spider.dead == False) & (player.dead == False)):
        player.update(pressed_keys)
    # handles player death, then respawning
    elif player.dead == True:
        sleep(2)
        player.dead = False
    
    # update spider each frame
    if spider.dead == False:
        spider.update()
    else:
        spider.deathAnimation()

    # update bolts each frame
    for bolt in bolts:
        #all_sprites.add(bolt)
        bolt.update()

        # colision detection
        if bolt.y < spider.hitbox[1] + spider.hitbox[3] and bolt.y + 40 > spider.hitbox[1]: # Checks x coords
            if bolt.x + 10 > spider.hitbox[0] and bolt.x < spider.hitbox[0] + spider.hitbox[2]: # Checks y coords
                if spider.dead == False:
                    spider.hit() # calls enemy hit method
                    bolts.clear() # removes bolt from bolts list

    # update the scoreboard/lives counter
    life = font.render(f' Lives: {player.lives}', False, (0, 0, 0))
    scoreboard = font.render(f' Score: {player.score}', False, (0, 0, 0))

    # draw lives counter/scoreboard
    screen.blit(life, (0, 0))
    screen.blit(scoreboard, (0, 45))

    # Draw player and spider
    for entity in sprites:
        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()

pygame.quit()