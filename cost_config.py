# price for page at given coverage
COST_CYAN = 0.55
COST_MAGENTA = 0.55
COST_YELLOW = 0.55
COST_BLACK = 0.55
COST_COVERAGE = 0.05  # should be the usual reference value in Germany

COST_ADDITIONAL = 0.41 + 0.11 + 0.11  # drum-kit, transfer unit, fuser kit

# page sizes in cm
PAGE_HEIGHT = 21
PAGE_WIDTH = 29.7
PAGE_RESOLUTION = 600

###############################

import math

PAGE_PIXEL_HEIGHT = math.floor(PAGE_HEIGHT / 2.54 * PAGE_RESOLUTION)
PAGE_PIXEL_WIDTH = math.floor(PAGE_WIDTH / 2.54 * PAGE_RESOLUTION)
