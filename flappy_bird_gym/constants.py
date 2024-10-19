from pathlib import Path
import os

############################ Speed and Acceleration ############################
SCROLL_SPEED = 1

BIRD_MAX_VEL_Y = 7  # max vel along Y, max descend speed
BIRD_MIN_VEL_Y = -7  # min vel along Y, max ascend speed

BIRD_ACC = 0.5       # bird acceleration
BIRD_MAX_FALL_Y = 500  # bird maximum fall distance
################################################################################

########################## Playable Dimensions #################################
BACKGROUND_WIDTH = 551
BACKGROUND_HEIGHT = 720

BIRD_WIDTH = 34
BIRD_HEIGHT = 24

PIPE_WIDTH = 78
PIPE_HEIGHT = BACKGROUND_HEIGHT

BASE_WIDTH = BACKGROUND_WIDTH
BASE_HEIGHT = BACKGROUND_HEIGHT / 3
GROUND_OFFSET = 0.7223

PIPE_GAP = 130
################################################################################

############################ Pixelated Speed and Acceleration ############################
PIXELATED_SCROLL_SPEED = 1

PIXELATED_BIRD_MAX_VEL_Y = 3  # max vel along Y, max descend speed
PIXELATED_BIRD_MIN_VEL_Y = -3  # min vel along Y, max ascend speed

PIXELATED_BIRD_ACC = 0.5      # bird acceleration
PIXELATED_BIRD_MAX_FALL_Y = int(64 * (BIRD_MAX_FALL_Y / BACKGROUND_WIDTH)) # bird maximum fall distance
################################################################################

########################## Pixelated Playable Dimensions #################################
PIXELATED_BACKGROUND_WIDTH = 64
PIXELATED_BACKGROUND_HEIGHT = int(64 * (BACKGROUND_HEIGHT / BACKGROUND_WIDTH))  # Maintain aspect ratio

PIXELATED_BIRD_WIDTH = int(64 * (BIRD_WIDTH / BACKGROUND_WIDTH))  # Maintain aspect ratio
PIXELATED_BIRD_HEIGHT = int(64 * (BIRD_HEIGHT / BACKGROUND_WIDTH))  # Maintain aspect ratio

PIXELATED_PIPE_WIDTH = int(64 * (PIPE_WIDTH / BACKGROUND_WIDTH))  # Maintain aspect ratio
PIXELATED_PIPE_HEIGHT = 64  # Maintain aspect ratio

PIXELATED_BASE_WIDTH = 64
PIXELATED_BASE_HEIGHT = int(64 * (BASE_HEIGHT / BACKGROUND_WIDTH))  # Maintain aspect ratio
PIXELATED_GROUND_OFFSET = 0.7223
PIXELATED_PIPE_GAP = int(64 * (PIPE_GAP / BACKGROUND_WIDTH)) + 5
################################################################################


################################ OLD VARIABLES  ################################


############################ Pixelated Speed and Acceleration ##################
#PIXELATED_SCROLL_SPEED = SCROLL_SPEED / 64

#PIXELATED_BIRD_MAX_VEL_Y = BIRD_MAX_VEL_Y / 64  # max vel along Y, max descend speed
#PIXELATED_BIRD_MIN_VEL_Y = BIRD_MIN_VEL_Y / 64  # min vel along Y, max ascend speed

#PIXELATED_BIRD_ACC = BIRD_ACC / 64                # bird acceleration
#PIXELATED_BIRD_MAX_FALL_Y = BIRD_MAX_FALL_Y / 64  # bird maximum fall distance
################################################################################

########################### Pixelated Dimensions ###############################
#PIXELATED_BACKGROUND_WIDTH = 49
#PIXELATED_BACKGROUND_HEIGHT = 64

#PIXELATED_PIPE_HEIGHT = PIXELATED_BACKGROUND_HEIGHT
#PIXELATED_PIPE_WIDTH = 7
#PIXELATED_GROUND_OFFSET = 0.75
################################################################################


_BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__))).parent

ASSETS_PATH = str(_BASE_DIR / "assets")