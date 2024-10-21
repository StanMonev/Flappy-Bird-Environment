# Silencing pygame:
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Exporting envs:
from flappy_bird_gym.env.flappy_bird_env import FlappyBirdEnv

# Exporting gym.make:
from gymnasium import make

# Registering environments:
from gymnasium.envs.registration import register

register(
    id="FlappyBird-features-v1",
    entry_point="flappy_bird_gym.env.flappy_bird_env:FlappyBirdEnv",
    kwargs={
          "obs_type": "features"
     }
)

register(
    id="FlappyBird-pixels-v1",
    entry_point="flappy_bird_gym.env.flappy_bird_env:FlappyBirdEnv",
    kwargs={
          "obs_type": "pixels"
     }
)

# Main names:
__all__ = [
    make.__name__,
    FlappyBirdEnv.__name__
]