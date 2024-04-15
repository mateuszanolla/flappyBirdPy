import pygame
import os
import random

# Step 1 = Define the constants.
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800

IMG_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMG_FLOOR = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMG_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMGS_BIRD = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
    ]

# Define the fonts
pygame.font.init()
POINTS_FONT = pygame.font.SysFont('arial', 50)

# Step 2 = Create the objects of the game.
class Bird:
    IMGS = IMGS_BIRD
    # Rotation animations
    MAX_ROTATION = 25
    ROTATION_SPEED = 20
    MOTION_SPEED = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        # calcular deslocamento
        self.time += 1
        offset = 1.5 * (self.time**2) + self.speed * self.time

        # restringir deslocamento
        if offset > 16:
            offset = 16
        elif offset < 0:
            offset -= 2

        # deslocamento em si
        self.y += offset

        # angle:
        if offset < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION

        else:
            if self.angle > -90:
                self.angle -= self.ROTATION_SPEED

    def draw(self, screen):
        # define which img to use:
        self.img_count += 1

        if self.img_count < self.MOTION_SPEED:
            self.img = self.IMGS[0]
        if self.img_count < self.MOTION_SPEED*2:
            self.img = self.IMGS[1]
        if self.img_count < self.MOTION_SPEED*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.MOTION_SPEED*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.MOTION_SPEED * 4:
            self.img = self.IMGS[0]
            self.img_count = 0

        # IF THE BIRD IS DESCENDING, IT SHOULD NOT SPREAD WINGS
        if self.angle <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.MOTION_SPEED*2

        # draw the image itself
        rotated_img = pygame.transform.rotate(self.img, self.angle)
        center_img = self.img.get_rect(topleft=(self.x, self.y)).center
        rectangle = rotated_img.get_rect(center=center_img)
        screen.blit(rotated_img, rectangle.topleft)

    # criar a mascara pra fazer colisao por pixel perfeito
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    DISTANCE = 200
    SPEED = 5

    def __init__(self,x):
        self.x = x
        self.height = 0
        self.top_position = 0
        self.bottom_position = 0
        self.TOP_PIPE = pygame.transform.flip(IMG_PIPE, False, True)
        self.BOTTOM_PIPE = IMG_PIPE
        self.passed = False
        self.define_height()

    def define_height(self):
        self.height = random.randrange(50, 450)
        self.top_position = self.height - self.TOP_PIPE.get_height()
        self.bottom_position = self.height + self.DISTANCE

    def move_pipe(self):
        self.x -= self.SPEED

    def draw(self, screen):
        screen.blit(self.TOP_PIPE, (self.x, self.top_position))
        screen.blit(self.BOTTOM_PIPE, (self.x, self.bottom_position))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask =  pygame.mask.from_surface(self.TOP_PIPE)
        bottom_mask =  pygame.mask.from_surface(self.BOTTOM_PIPE)

        top_distance = (self.x - round(bird.x), self.top_position - round(bird.y))
        bottom_distance = (self.x - round(bird.x), self.bottom_position - round(bird.y))

        top_collide_point = bird_mask.overlap(top_mask, top_distance)
        base_collide_point = bird_mask.overlap(bottom_mask, bottom_distance)

        if top_collide_point or base_collide_point:
            return True
        else:
            return False


class Floor:
    SPEED = 5
    WIDTH = IMG_FLOOR.get_width()
    IMG = IMG_FLOOR

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, screen):
        screen.blit(self.IMG, (self.x1, self.y))
        screen.blit(self.IMG, (self.x2, self.y))

# Step 3 = Create the draw the screen
def draw_screen(screen, birds, pipes, floor, points):
    screen.blit(IMG_BACKGROUND, (0, 0))
    for bird in birds:
        bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)
    text = POINTS_FONT.render(f'Points: {points}', 1, (255, 255, 255), (0, 0, 0))
    screen.blit(text, (WINDOW_WIDTH-10-text.get_width(), WINDOW_HEIGHT-100-text.get_height()))
    floor.draw(screen)
    pygame.display.update()

#Step4 = Function to create the instances in the game and the functionality
def main():
    birds = [Bird(230, 350)]
    floor = Floor(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    points = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(30)

        #user interaction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.jump()

        #make things move
        for bird in birds:
            bird.move()
        floor.move()

        add_pipe = False
        remove_pipe = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird):
                    birds.pop(i)
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    add_pipe = True
            pipe.move_pipe()
            if pipe.x + pipe.TOP_PIPE.get_width() < 0:
                remove_pipe.append(pipe)
        if add_pipe:
            points += 1
            pipes.append(Pipe(600))
        for pipe in remove_pipe:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if (bird.y + bird.img.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)

        draw_screen(screen, birds, pipes, floor, points)

if __name__ == '__main__':
    main()