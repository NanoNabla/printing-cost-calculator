import math
import os

from PIL import Image

PAGE_HEIGHT = 21
PAGE_WIDTH = 29.7
PAGE_RESOLUTION = 600

PAGE_PIXEL_HEIGHT = math.ceil(PAGE_HEIGHT / 2.54 * PAGE_RESOLUTION)
PAGE_PIXEL_WIDTH = math.ceil(PAGE_WIDTH / 2.54 * PAGE_RESOLUTION)

img = Image.new('RGB', (PAGE_PIXEL_WIDTH, PAGE_PIXEL_HEIGHT), color=(255, 255, 255))
pixels = img.load()

i = int(PAGE_PIXEL_HEIGHT * PAGE_PIXEL_WIDTH * 0.05)

jump = False
for x in range(PAGE_PIXEL_WIDTH):
    if jump == True:
        break
    for y in range(PAGE_PIXEL_HEIGHT):
        pixels[x, y] = (255, 0, 255)  # magenta
        i -= 1
        if i <= 0:
            jump = True
            break

img.save(os.path.join("test_img", "5procent_magenta.png"), "PNG")
