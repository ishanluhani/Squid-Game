import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)
circles = []
cookie_img = cv2.imread('tile002.png')
while True:
    _, image = cap.read()
    image = cv2.flip(image, 1)
    hand = detector.findHands(image, flipType=True)
    if hand[0]:
        a = detector.fingersUp(hand[0][0])
        if a[1]:
            index = hand[0][0]['lmList'][8]
            if a[2]:
                circles.append(index)
    shapes = np.zeros_like(image, np.uint8)
    shapes[180:360, 180:360] = cookie_img
    mask = shapes.astype(bool)
    image[mask] = cv2.addWeighted(image, 1 - .1, shapes,
                                   .1, 0)[mask]
    image[180:360, 180:360] = cookie_img
    for i in circles:
        image = cv2.circle(image, i, 5, (255, 0, 0), cv2.FILLED)
    cv2.imshow('image', image)
    cv2.waitKey(1)