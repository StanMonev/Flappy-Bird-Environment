import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

from pygame import Rect

from pygame.transform import flip as img_flip

from pygame import image as pyg_image
from pygame.transform import scale as img_scale
from envs.flappy_bird.flappy_bird_gym.constants import BACKGROUND_HEIGHT as win_height
from envs.flappy_bird.flappy_bird_gym.constants import BACKGROUND_WIDTH as win_width
from envs.flappy_bird.flappy_bird_gym.constants import BIRD_WIDTH
from envs.flappy_bird.flappy_bird_gym.constants import BIRD_HEIGHT
from envs.flappy_bird.flappy_bird_gym.constants import PIPE_HEIGHT
from envs.flappy_bird.flappy_bird_gym.constants import PIPE_WIDTH


_BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__))).parent

ASSETS_PATH = str(_BASE_DIR / "flappy_bird_gym/assets")

def pixel_collision(
    rect1: Rect, rect2: Rect, hitmask1: List[List[bool]], hitmask2: List[List[bool]]
) -> bool:
    """Checks if two objects collide and not just their rects."""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                return True
    return False


def get_hitmask(image) -> List[List[bool]]:
    """Returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask

def _load_sprite(filename, normal: bool, inverted: bool = False, scaled_size: Tuple[int, int] = None):
    if normal:
        img = pyg_image.load(f"{ASSETS_PATH}/{filename}.png")
    else:
        img = pyg_image.load(f"{ASSETS_PATH}/{filename}_64x64.png")
        
    if inverted:
        img = img_flip(img, False, True)
    
    if normal:
       img = img_scale(img, scaled_size)
    
    return img


def load_images(normal: bool = True) -> Dict[str, Any]:
    """ Loads and returns the image assets of the game. """
    images = {}

    try:
        # Sprite for the base (ground):
        images["ground"] = _load_sprite("base", normal, scaled_size=(win_width, win_height/3))

        # Background sprite:
        images["background"] = _load_sprite("background", normal, scaled_size=(win_width, win_height))

        # Bird sprites:
        images["bird"] = (
            _load_sprite("flappy_bird_up", normal, scaled_size=(BIRD_WIDTH, BIRD_HEIGHT)),
            _load_sprite("flappy_bird_mid", normal, scaled_size=(BIRD_WIDTH, BIRD_HEIGHT)),
            _load_sprite("flappy_bird_down", normal, scaled_size=(BIRD_WIDTH, BIRD_HEIGHT)),
        )

        # Pipe sprites:
        pipe_bottom_sprite = _load_sprite("pipe", normal, scaled_size=(PIPE_WIDTH, PIPE_HEIGHT))
        pipe_top_sprite = _load_sprite("pipe", normal, inverted=True, scaled_size=(PIPE_WIDTH, PIPE_HEIGHT))
        images["pipe"] = (pipe_top_sprite, pipe_bottom_sprite)
    except FileNotFoundError as ex:
        raise FileNotFoundError("Can't find the sprites folder! No such file or"
                                f" directory: {ASSETS_PATH}") from ex

    return images