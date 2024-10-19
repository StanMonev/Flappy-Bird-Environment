import pygame
import math

import envs.flappy_bird.flappy_bird_gym.utils as utils


class GameRenderer:
  def __init__(self, game) -> None:
    pygame.init()

    self._screen_width = game.screen_width
    self._screen_height = game.screen_height

    self.display = None
    self.surface = pygame.Surface((self._screen_width, self._screen_height))
    self.game = game
    self.images = utils.load_images(not game.pixelated)
    self.is_drawn = False

  def make_display(self):
    pygame.display.init()
    self.display = pygame.display.set_mode((self._screen_width,
                                          self._screen_height))
    for name, value in self.images.items():
      if value is None:
          continue

      if type(value) in (tuple, list):
          self.images[name] = tuple([img.convert_alpha()
                                      for img in value])
      else:
          self.images[name] = (value.convert() if name == "background"
                                else value.convert_alpha())

      
  def _draw_score(self) -> None:
    font = pygame.font.SysFont('Segoe', 26)
    score_text = font.render('Score: ' + str(math.floor(self.game.score)), True, pygame.Color(255, 255, 255))
    self.surface.blit(score_text, (20, 20))
      
  def draw_surface(self, show_score: bool = True):
    if self.game is None:
      raise ValueError("A game logic must be assigned to the renderer!")
    
    # Background
    self.surface.blit(self.images['background'], (0, 0))

    # Pipes
    self.game.pipe_group.draw(self.surface)

    # Ground
    self.game.ground_group.draw(self.surface)

    # Bird
    self.game.bird.draw(self.surface)

    if show_score and not self.game.pixelated:
        self._draw_score()
    
    self.is_drawn = True


  def update_display(self) -> None:
      """ Updates the display with the current surface of the renderer.

      A call to this method is usually preceded by a call to
      :meth:`.draw_surface()`. This method simply updates the display by
      showing the current state of the renderer's surface on it, it doesn't
      make any change to the surface.
      """
      if self.display is None:
          raise RuntimeError(
              "Tried to update the display, but a display hasn't been "
              "created yet! To create a display for the renderer, you must "
              "call the `make_display()` method."
          )

      self.display.blit(self.surface, (0,0))
      pygame.display.update()