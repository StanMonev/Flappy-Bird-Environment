import flappy_bird_gym.env.flappy_bird_env as FlappyBirdEnv
import flappy_bird_gym.original_game as OriginalGame
from gymnasium.utils.play import play
import gymnasium as gym
import numpy as np
import pygame
import time
import argparse

key_to_action = {(pygame.K_SPACE,): np.array([1])}

def main(mode):
    if mode == 'pixels':
        env = gym.make('FlappyBird-pixels-v0', render_mode="rgb_array")
        play(env, keys_to_action= key_to_action, noop=0) 
    else:
        env = gym.make('FlappyBird-features-v0', render_mode="rgb_array")
        play(env, keys_to_action= key_to_action, noop=0) 


def random_agent_env():
    env = gym.make("FlappyBird-features-v0", render_mode="rgb_array")
    env.reset()
    score = 0
    for _ in range(1000):
        env.render()

        # Getting random action:
        action = env.action_space.sample()

        # Processing:
        obs, reward, done, _, _ = env.step(action)

        score += reward
        print(f"Obs: {obs}\n"
              f"Action: {action}\n"
              f"Score: {score}\n")

        time.sleep(1 / 30)

        if done:
            env.render()
            time.sleep(0.5)
            break
    
    env.close()

def _get_args():
    """ Parses the command line arguments and returns them. """
    parser = argparse.ArgumentParser(description=__doc__)

    # Argument for the mode of execution (human or random):
    parser.add_argument(
        "--mode", "-m",
        type=str,
        default="original",
        choices=['pixels', 'features', 'random', 'original', 'test'],
        help="The execution mode for the game.",
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = _get_args()

    if args.mode == "original":
        OriginalGame.start()
    elif args.mode == "pixels":
        main("pixels")
    elif args.mode == "features":
        main("features")
    elif args.mode == "random":
        random_agent_env()
    elif args.mode == "test":
        test_env.test_flappy_bird()
    else:
        print("Invalid mode!")