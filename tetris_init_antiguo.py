from enum import Enum
import pygame
pygame.init()

screen_width = 600
screen_height = 480

# Set up the drawing window
screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()

x = screen_width / 2
y = screen_height / 2

center_x = screen_width / 2
center_y = screen_height / 2

rx1 = (screen_width / 2) * (1/2)
rx2 = (screen_width / 2) * (1/2)
ry1 = (screen_height / 2) * (1/2)
ry2 = (screen_height / 2) * (1/2)

COLOR = (255, 100, 98)
SURFACE_COLOR = (160, 160, 160)

BLOCK_COLOR = (140, 75, 150)
BLOCK_SIZE = 20
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

OFFSET_X = (screen_width - BOARD_WIDTH * BLOCK_SIZE) / 2
OFFSET_Y = (screen_height - BOARD_HEIGHT * BLOCK_SIZE) / 2

class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()


all_sprites = pygame.sprite.Group()

block = Block(BLOCK_COLOR, BLOCK_SIZE, BLOCK_SIZE)
block.rect.x = 0 + OFFSET_X
block.rect.y = 0 + OFFSET_Y
all_sprites.add(block)


# Run until the user asks to quit
ticks = 0
ticks_side = 0
running = True
blocks = []

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # Did the user click the window close button?
            running = False

    if ticks_side == 15:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and block.rect.x > 0 + OFFSET_X:
            block.rect.x -= BLOCK_SIZE
        if keys[pygame.K_d] and block.rect.x < (BOARD_WIDTH * BLOCK_SIZE - BLOCK_SIZE) + OFFSET_X:
            block.rect.x += BLOCK_SIZE
        ticks_side = 0

    # When block touches the bottom, put it back up
    if ticks == 30:
        block.rect.y += BLOCK_SIZE
        if block.rect.y > BOARD_HEIGHT * BLOCK_SIZE - BLOCK_SIZE + OFFSET_Y:
            block.rect.x = 0 + OFFSET_X
            block.rect.y = 0 + OFFSET_Y
        ticks = 0

    # Update
    all_sprites.update()

    # draw
    # Fill the background with a color
    screen.fill(SURFACE_COLOR)

    # Draw board
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0 + OFFSET_X, 0 + OFFSET_Y, BLOCK_SIZE * BOARD_WIDTH, BLOCK_SIZE * BOARD_HEIGHT))

    all_sprites.draw(screen)
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(60)
    ticks += 1
    ticks_side += 1

# Done! Time to quit.
pygame.quit()
