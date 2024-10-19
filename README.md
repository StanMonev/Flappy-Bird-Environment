# Flappy Bird Gymnasium Environment

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
* Let a random agent play with `python main.py --mode random` (WIP)
* Run tests with `python env_tests.py` or with `python main.py --mode test`
