import cv2
import numpy as np
import math

cap = cv2.VideoCapture(1)
triangle = 0
square = 0
circle = 0
line = 0
array = []


def capture(srcframe):
    ret, srcframe = cap.read()
    mask(srcframe)


def mask(frame):
    bgr = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
    lower = np.array([0, 0, 0])
    upper = np.array([70, 70, 70])
    mask = cv2.inRange(bgr, lower, upper)
    detection(frame, mask, 1000, 100000, 0.02, square, triangle, circle, line)


def detection(frame, mask, areaval, areaval2, lenval, square, triangle, circle, line):
    FIRST = 0
    BLUE = (255, 0, 0)
    GREEN = (0, 255, 0)
    RED = (0, 0, 255)
    YELLOW = (0, 255, 255)
    THICKNESS = 3
    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_list = []
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        d = calculation(box)
        area = cv2.contourArea(cnt)
        if area > areaval:
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cnt_len = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, lenval * cnt_len, True)
            if len(approx) == 3:
                if triangle >= 6:
                    triangle = 0
                else:
                    triangle = triangle + 1
                cv2.circle(frame, (cX, cY), 7, (229, 83, 0), -1)
                cv2.putText(frame, "triangle", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (215, 228, 41), 2)
                cv2.drawContours(frame, [cnt], FIRST, GREEN, THICKNESS)
            elif len(approx) == 4:
                    #(x, y, w, h) = cv2.boundingRect(approx)
                    #ar = w / float(h)
                    #if ar >= 0.95 and ar <= 1.05:
                    if square >= 6:
                        square = 0
                    else:
                        square = square + 1
                    cv2.circle(frame, (cX, cY), 7, (229, 83, 0), -1)
                    cv2.putText(frame, "sqaure", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (215, 228, 41), 2)
                    cv2.drawContours(frame, [cnt], FIRST, BLUE, THICKNESS)
            elif ((len(approx) > 7) and (len(approx) < 9)):
                if circle >= 6:
                    circle = 0
                else:
                    circle = circle + 1
                cv2.circle(frame, (cX, cY), 7, (229, 83, 0), -1)
                cv2.putText(frame, "circle", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (215, 228, 41), 2)
                cv2.drawContours(frame, [cnt], FIRST, YELLOW, THICKNESS)
                # print("square=", square)
                # print("triangle=", triangle)
                # print("circle=", circle)
                # print("line=", line)
                array.insert(0, [square, triangle, circle, line])

            else:
                if abs(d - area) < 1000:
                    if line >= 6:
                        line = 0
                    else:
                        line = line + 1
                        cv2.circle(frame, (cX, cY), 7, (229, 83, 0), -1)
                        cv2.putText(frame, "line", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (215, 228, 41), 2)
                        cv2.drawContours(frame, [cnt], FIRST, RED, THICKNESS)

            cv2.imshow("detected shapeas", frame)


def calculation(box):
    x1 = box[0][0]
    x2 = box[1][0]
    y1 = box[0][1]
    y2 = box[1][1]
    C1 = math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))

    x3 = box[1][0]
    x4 = box[2][0]
    y3 = box[1][1]
    y4 = box[2][1]
    C2 = math.sqrt(math.pow((x3 - x4), 2) + math.pow((y3 - y4), 2))

    d = C1 * C2
    return d


def show(square, triangle, circle, line):
    img = np.zeros((297, 210, 3), np.uint8)
    cv2.circle(img, (150, 40), 20, (0, 0, 255), -1)
    triangle_cnt = np.array([(150, 90), (130, 120), (170, 120)])
    cv2.line(img, (130, 180), (170, 180), (0, 0, 255), 4)
    cv2.rectangle(img, (170, 230), (130, 270), (0, 0, 255), -1)

    cv2.drawContours(img, [triangle_cnt], 0, (0, 0, 255), -1)
    cv2.putText(img, str(circle), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(img, str(triangle), (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(img, str(line), (50, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(img, str(square), (50, 260), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    for i in range(10):
        cv2.imwrite('ROV{}.png'.format(i), img)
        break


while 1:
    capture(cap)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        show(array[0][0], array[0][1], array[0][2], array[0][3])
        break

cv2.destroyAllWindows()
cap.release()