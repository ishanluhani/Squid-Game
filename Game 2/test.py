import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector


cap = cv2.VideoCapture(0)

# Overlay image
overlay_image = cv2.imread('tile002.png')

h, w = overlay_image.shape[:2]

# Create a new np array

# Change this into bool to use it as mask
while True:
    _, image = cap.read()
    background = cv2.flip(image, 1)
    shapes = np.zeros_like(background, np.uint8)

    # Put the overlay at the bottom-right corner
    shapes[0:h, 0:w] = overlay_image
    mask = shapes.astype(bool)
    background[mask] = cv2.addWeighted(background, 1 - .5, shapes,
                                       0.5, 0)[mask]

    cv2.imshow('image', image)
    cv2.waitKey(1)