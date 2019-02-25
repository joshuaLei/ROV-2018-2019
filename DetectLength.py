import cv2
import numpy as np
import math

cap = cv2.VideoCapture(1)

def capture(cap):
    ret, cap = cap.read()
    frame = cv2.flip(cap, 1)
    #cv2.imshow('srcframe', frame)
    mask(frame)

def mask(frame):
    bgr = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
    lower = np.array([0,0,0])
    upper = np.array([70,70,70])
    mask = cv2.inRange(bgr, lower, upper)
    #cv2.imshow('binary image', mask)
    detect(frame, mask, 10000)

def detect(frame, mask, areaval):
    im2, contours, hierarcy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > areaval:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
            cv2.imshow('frame', frame)
            calculation(frame, box, 1.8, rect)

def calculation(frame, box, width, center):
    x1 = box[0][0]
    x2 = box[1][0]
    y1 = box[0][1]
    y2 = box[1][1]
    C1 = math.sqrt(math.pow((x1 - x2),2) + math.pow((y1 - y2),2))

    x3 = box[1][0]
    x4 = box[2][0]
    y3 = box[1][1]
    y4 = box[2][1]
    C2 = math.sqrt(math.pow((x3 - x4),2) + math.pow((y3 - y4),2))

    if C1 < C2:
        ratio = abs(width/C1)
        cal = ratio*C2
    else:
        ratio = abs(width/C2)
        cal = ratio*C1

    print('calculation',cal)
    cv2.putText(frame, 'cal = {}'.format(cal), (int(center[0][0]), int(center[0][1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (215, 228, 41), 2)
    cv2.imshow('frame', frame)


while(1):
    capture(cap)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
cap.release()