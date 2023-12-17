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

rx1 = (screen_width / 2) * (1 / 2)
rx2 = (screen_width / 2) * (1 / 2)
ry1 = (screen_height / 2) * (1 / 2)
ry2 = (screen_height / 2) * (1 / 2)

COLOR = (255, 100, 98)
SURFACE_COLOR = (160, 160, 160)

BLOCK_COLOR = (140, 75, 150)
BLOCK_SIZE = 20
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

OFFSET_X = (screen_width - BOARD_WIDTH * BLOCK_SIZE) / 2
OFFSET_Y = (screen_height - BOARD_HEIGHT * BLOCK_SIZE) / 2

SPAWN_X = (BOARD_WIDTH / 2) * BLOCK_SIZE

class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()


class UserActionType(Enum):
    EXIT = 0
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    DROP = 3


def input_manager():
    """
    Create user actions out of war input
    :return:
    """
    events = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:    # Did the user click the window close button?
            events.append(UserActionType.EXIT)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        events.append(UserActionType.MOVE_LEFT)
    if keys[pygame.K_d]:
        events.append(UserActionType.MOVE_RIGHT)
    
    return events


def parse_inputs(original_events):
    events_x = 0
    for event in original_events:
        if event == UserActionType.MOVE_RIGHT:
            events_x += 1
        elif event == UserActionType.MOVE_LEFT:
            events_x -= 1
    if events_x > 0:
        return [UserActionType.MOVE_RIGHT]
    elif events_x < 0:
        return [UserActionType.MOVE_LEFT]
    elif events_x == 0:
        return []


all_sprites = pygame.sprite.Group()

background = pygame.sprite.Sprite()
background.image = pygame.image.load('tetris/data/tetris_background.png')
background.rect = background.image.get_rect()
background.rect.x = 0 + OFFSET_X
background.rect.y = 0 + OFFSET_Y
all_sprites.add(background)

block = Block(BLOCK_COLOR, BLOCK_SIZE, BLOCK_SIZE)
block.rect.x = SPAWN_X + OFFSET_X
block.rect.y = 0 + OFFSET_Y
all_sprites.add(block)

# Run until the user asks to quit
ticks = 0
ticks_side = 0
running = True
blocks = []


def collision_bottom(pos):
    return pos.y == BOARD_HEIGHT * BLOCK_SIZE + OFFSET_Y


def collision_blocks(pos):
    for block in blocks:
        if pos.y == block.rect.y and pos.x == block.rect.x:
            return True
    return False

input_events = []

while running:
    
    input_events += input_manager()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Did the user click the window close button?
            running = False

    if ticks == 10:
        input_events = parse_inputs(input_events)

        # Calc new pos only with gravity
        newpos = pygame.Rect(block.rect)
        newpos.y += BLOCK_SIZE

        # Check user action
        newpos_user = pygame.Rect(newpos)

        if UserActionType.MOVE_LEFT in input_events and newpos_user.x > 0 + OFFSET_X:
            newpos_user.x -= BLOCK_SIZE
        if (UserActionType.MOVE_RIGHT in input_events
            and newpos_user.x < (BOARD_WIDTH * BLOCK_SIZE - BLOCK_SIZE) + OFFSET_X):
            newpos_user.x += BLOCK_SIZE

        # When block touches the bottom, SAVE IT IN THE VARIABLE
        if collision_bottom(newpos_user) or collision_blocks(newpos_user):
            if collision_bottom(newpos) or collision_blocks(newpos):
                blocks.append(block)
                block = Block(BLOCK_COLOR, BLOCK_SIZE, BLOCK_SIZE)
                block.rect.x = SPAWN_X + OFFSET_X
                block.rect.y = 0 + OFFSET_Y
                all_sprites.add(block)
            else:
                block.rect = newpos
                # print(newpos.y)
        else:
            block.rect = newpos_user
            # print(newpos_user.y)
            
        ticks = 0
        input_events = []

    # Update
    all_sprites.update()

    # draw
    # Fill the background with a color
    screen.fill(SURFACE_COLOR)

    # Draw board
    pygame.draw.rect(
        screen,
        (0, 0, 0),
        pygame.Rect(
            0 + OFFSET_X,
            0 + OFFSET_Y,
            BLOCK_SIZE * BOARD_WIDTH,
            BLOCK_SIZE * BOARD_HEIGHT,
        ),
    )

    all_sprites.draw(screen)
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(60)
    ticks += 1
    ticks_side += 1

# Done! Time to quit.
pygame.quit()



# PROBLEMAS:
# botón exit no funciona
# a veces das click una sola vez y se mueve dos veces
# condiciones de perder una partida