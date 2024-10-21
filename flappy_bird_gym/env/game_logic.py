
import random
from enum import IntEnum
from typing import Tuple, Union, Dict

import pygame
from pygame.sprite import spritecollide as collision
import flappy_bird_gym.utils as utils

from flappy_bird_gym.constants import (
    BACKGROUND_WIDTH, 
    SCROLL_SPEED, 
    BIRD_ACC, 
    BIRD_MAX_VEL_Y,
    BIRD_MIN_VEL_Y,
    BIRD_MAX_FALL_Y,
    PIPE_HEIGHT, 
    BIRD_HEIGHT,
    PIPE_GAP,
    PIXELATED_BACKGROUND_WIDTH,
    PIXELATED_SCROLL_SPEED,
    PIXELATED_BIRD_ACC,
    PIXELATED_BIRD_MAX_VEL_Y,
    PIXELATED_BIRD_MIN_VEL_Y,
    PIXELATED_BIRD_MAX_FALL_Y,
    PIXELATED_PIPE_HEIGHT,
    PIXELATED_BIRD_HEIGHT,
    PIXELATED_PIPE_GAP
)

class BirdSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, images, constants):
        self.bird_images = images
        pygame.sprite.Sprite.__init__(self)
        self.image = self.bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.image_index = 0
        self.vel = 0
        self.flap = False
        self.alive = True
        self.constants = constants

    def update(self, user_input):
        # Animate Bird
        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = self.bird_images[self.image_index // 10]

        # Gravity and Flap
        self.vel += self.constants.BIRD_ACC
        if self.vel > self.constants.BIRD_MAX_VEL_Y:
            self.vel = self.constants.BIRD_MAX_VEL_Y
        if self.rect.y < self.constants.BIRD_MAX_FALL_Y:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = False

        # Rotate Bird
        self.image = pygame.transform.rotate(self.image, self.vel * self.constants.BIRD_MIN_VEL_Y)

        # User Input
        if user_input == GameLogic.Actions.FLAP and not self.flap and self.rect.y > 0 and self.alive:
            self.flap = True
            self.vel = self.constants.BIRD_MIN_VEL_Y

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type, bird_start_x, constants):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.exit, self.passed = False, False, False
        self.pipe_type = pipe_type
        self.bird_start_x = bird_start_x
        self.score_collected = False
        self.constants = constants

    def update(self):
        # Move Pipe
        self.rect.x -= self.constants.SCROLL_SPEED
        if self.rect.x <= -self.constants.BACKGROUND_WIDTH:
            self.kill()

        # Score
        if self.pipe_type == 'top':
            if self.bird_start_x >= self.rect.bottomleft[0] and not self.passed:
                self.enter = True
            if self.bird_start_x >= self.rect.bottomright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, image, constants):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.constants = constants

    def update(self):
        # Move Ground
        self.rect.x -= self.constants.SCROLL_SPEED
        if self.rect.x <= -self.constants.BACKGROUND_WIDTH:
            self.kill()

class GameLogic:
    def __init__(self, screen_size: Tuple[int, int]) -> None:
            
        self.constants = self.Constants(screen_size)

        self.pixelated = screen_size == (64, 64)
        
        self._clock = pygame.time.Clock()

        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]

        self.bird_x = int(self.screen_width * 0.2)
        self.bird_y = int((self.screen_height - self.constants.BIRD_HEIGHT) / 2)

        self.ground_x = 0
        self.ground_y = self.screen_height * 0.7223

        self.score = 0

        self.images = utils.load_images(not self.pixelated)

        self.bird = pygame.sprite.GroupSingle()
        self.bird.add(BirdSprite(self.bird_x, self.bird_y, self.images['bird'], self.constants))

        self.pipe_timer = 0
        self.pipe_group = pygame.sprite.Group()

        self.ground_group = pygame.sprite.Group()
        self.ground_group.add(Ground(self.ground_x, self.ground_y if not self.pixelated else self.ground_y + 2, 
                                     self.images['ground'], self.constants))


    class Actions(IntEnum):
        """ Possible actions for the player to take. """
        IDLE, FLAP = 0, 1

    class Constants:
        def __init__(self, screen_size: Tuple[int, int]) -> None:
            if screen_size == (64, 64):
                self.BACKGROUND_WIDTH = PIXELATED_BACKGROUND_WIDTH
                self.SCROLL_SPEED = PIXELATED_SCROLL_SPEED
                self.BIRD_ACC = PIXELATED_BIRD_ACC
                self.BIRD_MAX_VEL_Y = PIXELATED_BIRD_MAX_VEL_Y
                self.BIRD_MIN_VEL_Y = PIXELATED_BIRD_MIN_VEL_Y
                self.BIRD_MAX_FALL_Y = PIXELATED_BIRD_MAX_FALL_Y
                self.PIPE_HEIGHT = PIXELATED_PIPE_HEIGHT
                self.BIRD_HEIGHT = PIXELATED_BIRD_HEIGHT
                self.PIPE_GAP = PIXELATED_PIPE_GAP
            else:
                self.BACKGROUND_WIDTH = BACKGROUND_WIDTH
                self.SCROLL_SPEED = SCROLL_SPEED
                self.BIRD_ACC = BIRD_ACC
                self.BIRD_MAX_VEL_Y = BIRD_MAX_VEL_Y
                self.BIRD_MIN_VEL_Y = BIRD_MIN_VEL_Y
                self.BIRD_MAX_FALL_Y = BIRD_MAX_FALL_Y
                self.PIPE_HEIGHT = PIPE_HEIGHT
                self.BIRD_HEIGHT = BIRD_HEIGHT
                self.PIPE_GAP = PIPE_GAP

    def update_state(self, action: Union[Actions, int], fps) -> bool:
        """ Given an action taken by the player, updates the game's state.

        Args:
            action (Union[FlappyBirdLogic.Actions, int]): The action taken by
                the player.

        Returns:
            `True` if the player is alive and `False` otherwise.
        """

        # Spawn Ground
        if len(self.ground_group) < 2:
            if self.pixelated:
                ground_y = self.ground_y + 2
            else:
                ground_y = self.ground_y
            self.ground_group.add(Ground(self.screen_width , ground_y, self.images['ground'], self.constants))

        if self.bird.sprite.alive:
            self.pipe_group.update()
            self.ground_group.update()
        self.bird.update(action)
        self._update_bird_coordinates()

        for sprite in self.pipe_group.sprites():
            if sprite.passed and not sprite.score_collected:
                self.score += 1
                sprite.score_collected = True
                break
        
        bird_sprite = self.bird.sprite
        # Collision Detection
        collision_pipes = collision(bird_sprite, self.pipe_group, False)
        collision_ground = collision(bird_sprite,  self.ground_group, False)

        if collision_pipes or collision_ground:
            self.bird.sprite.alive = False

        if self.pipe_timer <= 0 and self.bird.sprite.alive:
            self._add_pipes()
            if self.pixelated:
                self.pipe_timer = random.randint(25, 50)
            else:
                self.pipe_timer = random.randint(180, 250)
        
        self.pipe_timer -= 1
        self._clock.tick(fps)

        return self.bird.sprite.alive
    
    def _update_bird_coordinates(self):
        self.bird_x = self.bird.sprite.rect.center[0]
        self.bird_y = self.bird.sprite.rect.center[1]

    def _add_pipes(self):
        pipe_coordinates = self._get_random_pipe()
        top_pipe_coord = pipe_coordinates[0]
        bottom_pipe_coord = pipe_coordinates[1]
        self.pipe_group.add(Pipe(top_pipe_coord['x'], top_pipe_coord['y'], self.images['pipe'][0], 'top', self.bird_x, self.constants))
        self.pipe_group.add(Pipe(bottom_pipe_coord['x'], bottom_pipe_coord['y'], self.images['pipe'][1], 'bottom', self.bird_x, self.constants))
    
    def _get_random_pipe(self) -> Dict[str, int]:
        """ Returns a randomly generated pipe. """
        # y of gap between upper and lower pipe
        gap_y = random.randrange(0, int(self.ground_y * 0.6 - self.constants.PIPE_GAP))
        gap_y += int(self.ground_y * 0.2)

        pipe_x = self.screen_width + 10
        return [
            {"x": pipe_x, "y": gap_y - self.constants.PIPE_HEIGHT}, # upper pipe
            {"x": pipe_x, "y": gap_y + self.constants.PIPE_GAP},   # lower pipe
        ]