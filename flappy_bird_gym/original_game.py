import pygame
from sys import exit
import random

import flappy_bird_gym.constants as CONSTANTS
import flappy_bird_gym.utils as utils

g_clock = pygame.time.Clock()


# Game
g_score = 0
g_scaled = True
g_game_stopped = True
g_images = utils.load_images(g_scaled)

# Window
g_win_height = CONSTANTS.BACKGROUND_HEIGHT if g_scaled else CONSTANTS.PIXELATED_BACKGROUND_HEIGHT
g_win_width = CONSTANTS.BACKGROUND_WIDTH if g_scaled else CONSTANTS.PIXELATED_BACKGROUND_WIDTH
window = pygame.display.set_mode((g_win_width, g_win_height))


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = g_images['bird'][0]
        self.rect = self.image.get_rect()
        self.starting_position = (int(g_win_width * 0.2),
                             int((g_win_height - self.rect.height) / 2))
        self.rect.center = self.starting_position
        self.image_index = 0
        self.vel = 0
        self.flap = False
        self.alive = True

    def update(self, user_input):

        bird_acc = 0
        bird_max_vel_y = 0
        bird_min_vel_y = 0
        bird_max_fall_y = 0

        if g_scaled:
            bird_acc = CONSTANTS.BIRD_ACC
            bird_max_vel_y = CONSTANTS.BIRD_MAX_VEL_Y
            bird_min_vel_y = CONSTANTS.BIRD_MIN_VEL_Y
            bird_max_fall_y = CONSTANTS.BIRD_MAX_FALL_Y
        else:
            bird_acc = CONSTANTS.PIXELATED_BIRD_ACC
            bird_max_vel_y = CONSTANTS.PIXELATED_BIRD_MAX_VEL_Y
            bird_min_vel_y = CONSTANTS.PIXELATED_BIRD_MIN_VEL_Y
            bird_max_fall_y = CONSTANTS.PIXELATED_BIRD_MAX_FALL_Y


        # Animate Bird
        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = g_images['bird'][self.image_index // 10]

        # Gravity and Flap
        self.vel += bird_acc
        if self.vel > bird_max_vel_y:
            self.vel = bird_max_vel_y
        if self.rect.y < bird_max_fall_y:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = False

        # Rotate Bird
        self.image = pygame.transform.rotate(self.image, self.vel * bird_min_vel_y)

        # User Input
        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            self.flap = True
            self.vel = bird_min_vel_y


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type, bird_starting_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.exit, self.passed = False, False, False
        self.pipe_type = pipe_type
        self.bird_starting_x = bird_starting_x

    def update(self):

        scroll_speed = 0

        if g_scaled:
            scroll_speed = CONSTANTS.SCROLL_SPEED
        else:
            scroll_speed = CONSTANTS.PIXELATED_SCROLL_SPEED


        # Move Pipe
        self.rect.x -= scroll_speed
        if self.rect.x <= -g_win_width:
            self.kill()

        # Score
        global g_score
        if self.pipe_type == 'bottom':
            if self.bird_starting_x > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if self.bird_starting_x > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                g_score += 1 


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = g_images['ground']
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):

        scroll_speed = 0

        if g_scaled:
            scroll_speed = CONSTANTS.SCROLL_SPEED
        else:
            scroll_speed = CONSTANTS.PIXELATED_SCROLL_SPEED

        # Move Ground
        self.rect.x -= scroll_speed
        if self.rect.x <= -g_win_width:
            self.kill()


def quit_game():
    # Exit Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


# Game Main Method
def start_game(title_font, title_color, score_font):
    global g_score

    # Instantiate Bird
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    # Setup Pipes
    pipe_timer = 0
    pipes = pygame.sprite.Group()

    ground_offset = CONSTANTS.GROUND_OFFSET if g_scaled else CONSTANTS.PIXELATED_GROUND_OFFSET

    # Instantiate Initial Ground
    x_pos_ground, y_pos_ground = 0, g_win_height * ground_offset
    ground = pygame.sprite.Group()
    ground.add(Ground(x_pos_ground, y_pos_ground))

    run = True
    while run:
        # Quit
        quit_game()

        # Reset Frame
        window.fill((0, 0, 0))

        # User Input
        user_input = pygame.key.get_pressed()

        # Draw Background
        window.blit(g_images['background'], (0, 0))

        # Spawn Ground
        if len(ground) <= 2:
            ground.add(Ground(g_win_width, y_pos_ground))

        # Draw - Pipes, Ground and Bird
        pipes.draw(window)
        ground.draw(window)
        bird.draw(window)

        # Show Score
        score_text = score_font.render('Score: ' + str(g_score), True, pygame.Color(255, 255, 255))
        window.blit(score_text, (20, 20))

        # Update - Pipes, Ground and Bird
        if bird.sprite.alive:
            pipes.update()
            ground.update()
        bird.update(user_input)

        # Collision Detection
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        if collision_pipes or collision_ground:
            bird.sprite.alive = False
            if collision_ground:
                
                end_text = title_font.render('Game Over', True, title_color) 
                score_text = title_font.render('Score: ' + str(g_score), True, title_color)

                end_text_middle = _get_middle_position(end_text)
                score_text_middle = _get_middle_position(score_text)

                offset = 25

                end_text_position = (end_text_middle[0] + offset, 
                                     end_text_middle[1] + offset)
                
                score_text_position = (score_text_middle[0] - offset, 
                                        score_text_middle[1] - offset)

                window.blit(end_text, score_text_position)
                window.blit(score_text, end_text_position)
                if user_input[pygame.K_r]:
                    g_score = 0
                    break

        # Spawn Pipes
        if pipe_timer <= 0 and bird.sprite.alive:
            gap_size = 130 if g_scaled else 20
            
            gap_y = random.randrange(0, int(y_pos_ground * 0.6 - gap_size))
            gap_y += int(y_pos_ground * 0.2)

            pipe_x = g_win_width + 10

            pipe_height = CONSTANTS.PIPE_HEIGHT if g_scaled else CONSTANTS.PIXELATED_PIPE_HEIGHT

            y_top = gap_y - pipe_height
            y_bottom = gap_y + gap_size

            pipes.add(Pipe(pipe_x, y_top, g_images['pipe'][0], 'top', bird.sprite.starting_position[0]))
            pipes.add(Pipe(pipe_x, y_bottom, g_images['pipe'][1], 'bottom', bird.sprite.starting_position[0]))
            pipe_timer = random.randint(180, 250)
        pipe_timer -= 1

        g_clock.tick(60)
        pygame.display.update()


def _get_middle_position(item):
    return (g_win_width // 2 - item.get_width() // 2,
                g_win_height // 2 - item.get_height() // 2)


# Menu
def menu():
    global g_game_stopped

    global g_images

    pygame.init()

    _score_font_size = 26 if g_scaled else 0 # if pixelated do not show score.
    _title_font_size = 50 if g_scaled else 0 # if pixelated do not show title.

    _score_font = pygame.font.SysFont('Segoe', _score_font_size)
    _title_font = pygame.font.SysFont('Arial Bold', _title_font_size)
    _title_color = pygame.Color(255, 165, 0)

    while g_game_stopped:
        quit_game()

        start_text = _title_font.render('Start game with space.', True, _title_color)

        offset = 50
        
        start_text_middle = _get_middle_position(start_text)
        start_text_position = (start_text_middle[0], 
                                start_text_middle[1] - offset)
        
        
        ground_offset = CONSTANTS.GROUND_OFFSET if g_scaled else CONSTANTS.PIXELATED_GROUND_OFFSET

        # Draw Menu
        window.fill((0, 0, 0))
        window.blit(g_images['background'], (0, 0))
        window.blit(g_images['ground'], Ground(0, g_win_height * ground_offset))
        window.blit(g_images['bird'][0], (int(g_win_width * 0.2), int((g_win_height - g_images['bird'][0].get_height())/2)))
        window.blit(start_text, start_text_position)

        # User Input
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            start_game(_title_font, _title_color, _score_font)

        pygame.display.update()

def start():
    menu()