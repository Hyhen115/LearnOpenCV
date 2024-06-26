import cv2
import mediapipe as mp
import time
import math
import numpy as np


def calculate_angle(x1, y1, z1, x2, y2, z2, x3, y3, z3):

    v1 = np.array([x1 - x2, y1 - y2, z1 - z2])
    v2 = np.array([x3 - x2, y3 - y2, z3 - z2])
    return np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


cap = cv2.VideoCapture(1)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
# hand fingermarks
handLmsStyle = mpDraw.DrawingSpec(color=(79, 78, 73), thickness=5, circle_radius=10)
# hand lines
handConStyle = mpDraw.DrawingSpec(color=(158, 155, 142), thickness=5)
pTime = 0
cTime = 0

touching = False

while True:
    ret, img = cap.read()
    if ret:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        imgHeight = img.shape[0]
        imgWidth = img.shape[1]
        # have hands
        if result.multi_hand_landmarks:
            # for each hand
            for handLms in result.multi_hand_landmarks:
                # draw all connections and dots out
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle)

                xAvg = int(0)
                yAvg = int(0)
                zAvg = int(0)

                count = int(0)

                xThumb = int(0)
                yThumb = int(0)
                zThumb = int(0)

                xMid = int(0)
                yMid = int(0)
                zMid = int(0)

                # loop through all fingermarks
                for i, lm in enumerate(handLms.landmark):
                    # x coordinates
                    xPos = int(lm.x * imgWidth)
                    # y coordinates
                    yPos = int(lm.y * imgHeight)
                    # z coordinates
                    zPos = int(lm.z * imgWidth)
                    # put coordinates besides the circles
                    cv2.putText(img, str(i), (xPos - 50, yPos + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                    # when is the fingertip points
                    if i == 4 or i == 8 or i == 12 or i == 16 or i == 20:
                        # bigger circle and color
                        cv2.circle(img, (xPos, yPos), 15, (54, 53, 50), cv2.FILLED)

                    if i == 8 or i == 12 or i == 16 or i == 20:
                        # calculate avg pt
                        xAvg += xPos
                        yAvg += yPos
                        zAvg += zPos
                        count += 1

                    if i == 4:
                        xThumb += xPos
                        yThumb += yPos
                        zThumb += zPos

                    if i == 0:
                        xMid += xPos
                        yMid += yPos
                        zMid += zPos

                    if i == 20:
                        # last loop
                        # calculate avg pt
                        xAvg = xAvg / count
                        yAvg = yAvg / count
                        zAvg = zAvg / count

                        # show the point
                        cv2.circle(img, (int(xAvg), int(yAvg)), 15, (84, 221, 236), cv2.FILLED)

                        # show line the point and the mid
                        cv2.line(img, (int(xAvg), int(yAvg)), (int(xMid), int(yMid)), (185, 185, 185), 2)
                        # calculate length for point and mid
                        length = math.sqrt((xAvg - xMid) ** 2 + (yAvg - yMid) ** 2 + (zAvg - zMid) ** 2)
                        # show the length point and mid
                        cv2.putText(img, str(int(length)), (int((xAvg + xMid) / 2), int((yAvg + yMid) / 2)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

                        # show the mid and thumb
                        cv2.line(img, (int(xThumb), int(yThumb)), (int(xMid), int(yMid)), (185, 185, 185), 2)
                        # calculate length for point and mid
                        length = math.sqrt((xThumb - xMid) ** 2 + (yThumb - yMid) ** 2 + (zThumb - zMid) ** 2)
                        # show the length point and mid
                        cv2.putText(img, str(int(length)), (int((xMid + xThumb) / 2), int((yMid + yThumb) / 2)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

                        # find the angle
                        angle = calculate_angle(xAvg, yAvg, zAvg, xMid, yMid, zMid, xThumb, yThumb, zThumb)*180/math.pi
                        print(angle)

                        cv2.putText(img,str(int(angle)),(xMid,yMid-50),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2)

                    # print the point position
                    print(i, xPos, yPos)

        # set fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f"FPS : {int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow('img', img)

    if cv2.waitKey(1) == ord('q'):
        break
