import cv2
import numpy as np
from src.simulator.config.config import Config
from matplotlib import pyplot as plt

config = Config()

image = np.zeros((config.MAP_HEIGHT, config.MAP_WIDTH, 1), np.uint8)


cv2.circle(image, (0, 0), config.BASE_RADIUS, 255, -1)
cv2.circle(image, (config.MAP_HEIGHT, config.MAP_WIDTH), config.BASE_RADIUS, 255, -1)

plt.imshow(image)
plt.show()