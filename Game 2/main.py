import cv2
from cvzone.HandTrackingModule import HandDetector


cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)
circles = []

while True:
    _, image = cap.read()
    image = cv2.flip(image, 1)
    hand = detector.findHands(image, flipType=True)
    if hand[0] and detector.fingersUp(hand[0][0])[1]:
        index = hand[0][0]['lmList'][8]
        circles.append(index)
    image[180:360, 180:360] = cv2.imread('tile002.png')
    for i in circles:
        image = cv2.circle(image, i, 5, (255, 0, 0))
    cv2.imshow('image', image)
    cv2.waitKey(1)