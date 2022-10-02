import cv2
from cvzone.HandTrackingModule import HandDetector


cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    _, image = cap.read()
    image = cv2.flip(image, 1)
    hand = detector.findHands(image, flipType=True)
    if hand[0]:
        print(detector.fingersUp(hand[0][0])[1])
    cv2.imshow('image', image)
    cv2.waitKey(1)