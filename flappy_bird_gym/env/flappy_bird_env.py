from typing import Dict, Tuple, Union

import gymnasium as gym
import numpy as np
import pygame

from flappy_bird_gym.env.game_logic import GameLogic
from flappy_bird_gym.env.renderer import GameRenderer

class FlappyBirdEnv(gym.Env):

  metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60, "render_pixelated_fps": 20, "obs_type": ["pixels", "features"]}

  def __init__(self, render_mode=None, obs_type="features",
               screen_size: Tuple[int, int] = (551, 720)) -> None:

    self._game = None
    self._renderer = None
    if obs_type == 'pixels':
      self._screen_size = (64, 64)
      self.fps = self.metadata['render_pixelated_fps']
    else:
      self._screen_size = screen_size
      self.fps = self.metadata['render_fps']
    self.render_mode = render_mode
    self.obs_type = obs_type
    self.pass_pipe = 0.0

    """
    The Space object corresponding to valid actions, all valid actions should be
    contained with the space.
    """
    self.action_space = gym.spaces.Discrete(2)

    """
    The Space object corresponding to valid observations, all valid observations
    should be contained with the space. It is static across all instances.
    """
    if obs_type == "pixels":
      self.observation_space = gym.spaces.Box(0, 255,
                                              shape=(64, 64, 3),
                                              dtype=np.uint8)
    else:
      self.observation_space = self._initial_feature_space()
  
  def _observation(self):

    if self.obs_type == "pixels":
      if not self._renderer.is_drawn:
        self._renderer.draw_surface()

      #Pixelate the surface
      pixelated = pygame.transform.smoothscale(self._renderer.surface, [64, 64])

      pixels = pygame.surfarray.pixels3d(pixelated)
      return np.transpose(np.array(pixels), axes=(1, 0, 2))
    else:
      return self._feature_space()
    
  def _initial_feature_space(self):
    low = [
      0.0,  # Horizontal Distance
      -1.0, # Vertical Distance
      0.0,  # Bottom Left Point of Top Pipe
      0.0,  # Bottom Right Point of Top Pipe
      0.0,  # Top Left Point of Bottom Pipe
      0.0,  # Top Right Point of Bottom Pipe
      0.0,  # Bottom Left Point of Next Top Pipe
      0.0,  # Bottom Right Point of Next Top Pipe
      0.0,  # Top Left Point of Next Bottom Pipe
      0.0,  # Top Right Point of Next Bottom Pipe
      -1.0, # Velocity
      0.0,  # Top Point of the Bird
      0.0   # Bottom Point of the Bird
    ]

    high = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    return gym.spaces.Box(
              low=np.array(low),
              high=np.array(high),
              dtype=np.float_
          )

  def _feature_space(self):

    h_dist = 1.0
    v_dist = 1.0
    bird_top = 1.0 
    bird_bottom = 1.0 
    visable_top_pipe_bottom_left = 1.0
    visable_top_pipe_bottom_right = 1.0
    visable_bottom_pipe_top_left = 1.0
    visable_bottom_pipe_top_right = 1.0
    
    visable_next_top_pipe_bottom_left = 1.0
    visable_next_top_pipe_bottom_right = 1.0
    visable_next_bottom_pipe_top_left = 1.0
    visable_next_bottom_pipe_top_right = 1.0

    bird_x = self._game.bird.sprite.rect.left
    bird_y = self._game.bird.sprite.rect.top

    pipe_gap = 0

    velocity = self._game.bird.sprite.vel / self._game.constants.BIRD_MAX_VEL_Y

    visable_top_pipe = self._not_passed_top_pipe()

    if visable_top_pipe is not None:

      if self._game is not None:
        pipe_gap = self._game.constants.PIPE_GAP

      visable_top_pipe_right_x = visable_top_pipe.rect.right
      visable_bottom_pipe_top_y = visable_top_pipe.rect.bottom + pipe_gap

      h_dist = visable_top_pipe_right_x  - bird_x

      v_dist = (visable_top_pipe.rect.bottom + visable_bottom_pipe_top_y) / 2 - bird_y

      h_dist /= self._screen_size[0]
      v_dist /= self._screen_size[1]

      bird_top = self._game.bird.sprite.rect.top / self._screen_size[1]
      bird_bottom = self._game.bird.sprite.rect.bottom / self._screen_size[1]

      visable_top_pipe_bottom_left = visable_top_pipe.rect.bottomleft[0] / self._screen_size[0]
      visable_top_pipe_bottom_right = visable_top_pipe.rect.bottomright[0] / self._screen_size[0]
      visable_bottom_pipe_top_left = (visable_top_pipe.rect.bottomleft[0] + pipe_gap) / self._screen_size[0]
      visable_bottom_pipe_top_right = (visable_top_pipe.rect.bottomright[0] + pipe_gap) / self._screen_size[0]

    
    visable_next_top_pipe = self._last_visable_top_pipe()
    
    if visable_next_top_pipe is not None and visable_next_top_pipe != visable_top_pipe:

      if self._game is not None:
        pipe_gap = self._game.constants.PIPE_GAP

      visable_next_top_pipe_bottom_left = visable_next_top_pipe.rect.bottomleft[0] / self._screen_size[0]
      visable_next_top_pipe_bottom_right = visable_next_top_pipe.rect.bottomright[0] / self._screen_size[0]
      visable_next_bottom_pipe_top_left = (visable_next_top_pipe.rect.bottomleft[0] + pipe_gap) / self._screen_size[0]
      visable_next_bottom_pipe_top_right = (visable_next_top_pipe.rect.bottomright[0] + pipe_gap) / self._screen_size[0]

    features = [
      h_dist,
      v_dist,
      visable_top_pipe_bottom_left,
      visable_top_pipe_bottom_right,
      visable_bottom_pipe_top_left,
      visable_bottom_pipe_top_right,
      visable_next_top_pipe_bottom_left, 
      visable_next_top_pipe_bottom_right,
      visable_next_bottom_pipe_top_left, 
      visable_next_bottom_pipe_top_right,
      velocity,
      bird_top,
      bird_bottom
    ]

    features = np.clip(features, self.observation_space.low, self.observation_space.high)

    return np.array(features, dtype=np.float_)
  
  def _pipe_sprites(self):
    return self._game.pipe_group.sprites()
  
  def _not_passed_top_pipe(self):
    
    sprites = self._pipe_sprites()
    for sprite in sprites:
      if sprite.pipe_type == 'top' and sprite.rect.right >= self._game.bird.sprite.rect.left:
        return sprite
      
  def _last_visable_top_pipe(self):

    sprites = self._pipe_sprites()
    if len(sprites) >= 4:
      return sprites[-2] # the second to last pipe is always the next visable top pipe
    else:
      return None
      
  def _bird_hits_top_reward(self, reward):
    bird_upper_bound = self._game.bird_y

    not_passed_top_pipe = self._not_passed_top_pipe()

    if not_passed_top_pipe is None:
      self.close()
      raise RuntimeError("Could not find next available pipe for reward.")

    if bird_upper_bound < 0:
      return -0.5
    
    return reward
  
  def _get_reward(self):
    bird_upper_bound = self._game.bird_y

    not_passed_top_pipe = self._not_passed_top_pipe()

    if not_passed_top_pipe is None:
      self.close()
      raise RuntimeError("Could not find next available pipe for reward.")

    if bird_upper_bound < 0:
      return -0.5
    
    return 0

  def step(self,
            action: Union[GameLogic.Actions, int],
  ) -> Tuple[np.ndarray, float, bool, Dict]:
    """ Given an action, updates the game state.

    Args:
        action (Union[GameLogic.Actions, int]): The action taken by
            the agent. Zero (0) means "do nothing" and one (1) means "flap".
    """

    
    if self._renderer is None or self._game is None:
      self.close()
      raise RuntimeError("Could not find GameRenderer or GameLogic. The environment might not have been reset yet.")
    
    alive = self._game.update_state(action, self.fps)
    observation = self._observation()

    if not alive:
      reward = -1
    else:
      reward = 0.1

    reward = self._bird_hits_top_reward(reward)

    # if pipe passed give reward
    if self.pass_pipe < self._game.score:
      reward = 1
      self.pass_pipe += 1

    done = not alive
    info = {"score": self._game.score}

    if self.render_mode == "human":
      self.render()

    truncated = self._game.score == 100

    return observation, reward, done, truncated, info
  
  def reset(self, seed=None, options=None):
    """ Resets the environment (starts a new game). """
    super().reset(seed=seed, options=options)
    
    self._game = GameLogic(self._screen_size)
    self._renderer = GameRenderer(self._game)
    self.pass_pipe = 0

    observation = self._observation()
    info = {"score": self._game.score}

    return observation, info
  
  def render(self):
    """ Renders the next frame. """

    if self.render_mode not in FlappyBirdEnv.metadata['render_modes']:
      raise ValueError("Invalid render mode!")
    
    if self._renderer is None:
      raise ValueError("Environment has not been reset or has not been initialized.")
    
    self._renderer.draw_surface()

    if self.render_mode == "rgb_array":
      return np.transpose(np.array(pygame.surfarray.pixels3d(self._renderer.surface)), axes=(1,0,2))
    else:
      if self._renderer.display is None:
          self._renderer.make_display()
      self._renderer.update_display()

  
  def close(self):
    """ Closes the environment. """
    if self._renderer is not None:
        pygame.display.quit()
        pygame.quit()
        self._renderer = None
    super().close()