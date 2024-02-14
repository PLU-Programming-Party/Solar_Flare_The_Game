import math
import pygame
import random
from pygame import mixer

TIMESCORE_MULTIPLIER = 100
PARTICLESCORE_MULTIPLIER = 100

class Particle:
    def __init__(self, position, size, velocity):
        self.position = position
        self.size = size
        self.velocity = velocity
        #chai tea, chai means tea, you are saying tea tea bro.


class ParticleManagerSpitter():
    #80mphMonster
    #GarbageIsGood
    def __init__(self, position):
        self.particleArray = []
        self.position = position
        self.rotation = 360

    def spit(self, screen, dt, player):
        velocityVector = pygame.Vector2(150,0)
        self.rotation = random.randint(-180, 0)
        self.particleArray.append(Particle(self.position.copy(), random.uniform(2,8), velocityVector.rotate(self.rotation)))

        for particle in self.particleArray:
            particle.position += particle.velocity * dt
            if (collision_detector(player.size, player.position, particle.size, particle.position)):
                player.score += particle.size * PARTICLESCORE_MULTIPLIER
                particle.position.y = screen.get_width() + 1
                scalar = (particle.size/player.size)
                player.velocity = pygame.Vector2(player.velocity.x + (particle.velocity.x * scalar), player.velocity.y + (particle.velocity.y * scalar))


        self.spitoon(screen)
        for particle in self.particleArray:
            pygame.draw.circle(screen, "orange", particle.position, particle.size)



    def spitoon(self, screen):
        #spitoon
        self.particleArray = [p for p in self.particleArray if not self.spitoonable(screen, p)]



    def spitoonable(self, screen, p):
        if ((p.position.x > screen.get_width()) or (p.position.x < 0) or (p.position.y > screen.get_height()) or (p.position.y < 0)):
            return True
        else:
            return False

class Player:
    def __init__(self, position, velocity, size, image_l, image_r):
        self.position = position
        self.velocity = velocity
        self.size = size
        self.image = image_l
        self.image_l = image_l
        self.image_r = image_r
        self.score = 0

    def tick(self, screen, dt):
        self.velocity = self.velocity + pygame.Vector2(0, 30) * dt
        self.position = self.position + self.velocity * dt
        if (self.position.x > screen.get_width()):
            self.position.x = screen.get_width()

        if (self.position.x < 0):
            self.position.x = 0

        #pygame.draw.circle(screen, "green", self.position, self.size - 5)
        screen.blit(self.image, self.position - pygame.Vector2(self.image.get_width() / 2, self.image.get_height() / 2))

        if self.velocity.x > 0:
            self.image = self.image_r
        else:
            self.image = self.image_l



def backgroundStars():
    allStar = []
    for i in range(250):
        pos1 = random.normalvariate(screen.get_width() / 2, screen.get_width() / 6)
        pos2 = random.normalvariate(screen.get_height() / 2, screen.get_width() / 6)
        starPos = pygame.Vector2(pos1, pos2)
        allStar.append(starPos)
    return allStar

def collision_detector(object1_size, object1_position, object2_size, object2_position):
    dist = math.sqrt((object1_position.x - object2_position.x) ** 2 + (object1_position.y - object2_position.y) ** 2)
    return (dist <= (object2_size + object1_size))


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
saved_time = clock.get_time()
running = True
dt = 0

spaceman = pygame.image.load('img.png')
spaceman = pygame.transform.scale(spaceman, (45, 45))
image_l = spaceman
image_r = pygame.transform.flip(spaceman, True, False)
player = Player(pygame.Vector2(screen.get_width() / 2, 0), pygame.Vector2(0, 150), 25, image_l, image_r)
particleSpitter = ParticleManagerSpitter(pygame.Vector2(screen.get_width() / 2, screen.get_height()))

starPos = backgroundStars()

sun_size = 300
sun_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() + 200)

#Instantiate mixer
mixer.init()

#Load audio file
mixer.music.load('song.mp3')

print("music started playing....")

#Set preferred volume
mixer.music.set_volume(0.2)

#Play the music
mixer.music.play()

mixer.music.rewind()
mixer.music.set_pos(5.0)

oh_no = False
while running:
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    player.score += dt * TIMESCORE_MULTIPLIER


    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    score_text = my_font.render(str(int(player.score)), False, (0, 0, 0))

    if player.position.y < 0 or player.position.y > screen.get_height() or collision_detector(player.size, player.position, sun_size, sun_position):
        if not oh_no:
            mixer.music.rewind()
            mixer.music.set_pos(3.0)
        oh_no = True

        #TODO: fix this
        # if mixer.music.get_pos() > (7.0 * 1000):
        #     mixer.music.rewind()
        #     mixer.music.set_pos(5.0)

        text_surface = my_font.render('Game Over You Lose', False, (255, 255, 255))
        play_again = my_font.render('hold SPACE to play again', False, (255, 255, 255))
        screen.blit(text_surface, (screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(play_again, (screen.get_width() / 2, screen.get_height() / 2 + 40))
        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            oh_no = False
            mixer.music.rewind()
            mixer.music.set_pos(5.0)
            player.score = 0
            player.position = pygame.Vector2(screen.get_width() / 2, 1)
            player.velocity = pygame.Vector2(0, 150)
            particleSpitter.particleArray = []

        continue



    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    for star in starPos:
        pygame.draw.circle(screen, "white", star, 1)

    particleSpitter.spit(screen, dt, player)
    pygame.draw.circle(screen, "yellow", sun_position, sun_size)
    player.tick(screen, dt)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.velocity = player.velocity + pygame.Vector2(-5, 0)
    if keys[pygame.K_d]:
        player.velocity = player.velocity + pygame.Vector2(5, 0)

    score_rect = score_text.get_rect(center=(screen.get_width() / 2, screen.get_height() - 40))
    screen.blit(score_text, score_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()




