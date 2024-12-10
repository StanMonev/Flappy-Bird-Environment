# Flappy Bird Gymnasium Environment

## Note
**I do NOT own any of the original game assets** except the 64x64 graphics. You can find the assets <a href="https://github.com/samuelcust/flappy-bird-assets">here</a>.
This repository is currently not in development, so there might be bugs. I have been able to train models with the current environment, so it is functional. Of course fixes, notes and comments are always welcome.

**Description**
* The player is a little bird that tries to get trough the gap between the green pipes.

**Goal of the game**
* Try to get passed as many pipes as possible.

**Action Space**
* 1: Idle
* 2: Spacebar

**Observation Space**
* Pixel space: gym.spaces.Box - 64x64
* Feature space: [Bird X, Bird Y, Next Available Hole Y, Next Available Width] (To fix - probably do not need the X Coordinate of the bird, since it's only moving up and down)

**Libraries**
* gymnasium
* pygame
* numpy

**Setup:**
* Start original game with `python main.py` or `python main.py --mode original`
* Start game in pixelated environment mode with `python main.py --mode pixels`
* Start game in features environment mode with `python main.py --mode features`
