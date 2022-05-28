''' 
by: Mohammad Alghrawe
Youtube: Bit by Bit
www.alghrawe-mohammad.com
Color Recognition Machine 
version: 0.01
Software: opencv, pyfirmata
Hardware: Webcam or MobileCam using DroidCam App, Arduino Uno, Servo ,LED
'''

import cv2
# controling hardware.
import pyfirmata
# Servo Config.
from pyfirmata import SERVO
import time
# Arduino configrution.
port = "COM8"
board = pyfirmata.Arduino(port)
# Servo Config.
pin = 8
board.digital[pin].mode = SERVO
# LEDs config.
Pin_13 = board.get_pin('d:13:o')
Pin_12 = board.get_pin('d:12:o')
# controlling the servo.


def rotateServo(pin, angle):
    board.digital[pin].write(angle)
    # time.sleep(0.09)


# capturing the video fro the source.
cap = cv2.VideoCapture(0)
#1280, 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
rotateServo(pin, 0)
while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    cx = int(width / 2)
    cy = int(height / 2)

    # Pick pixel value
    pixel_center = hsv_frame[cy, cx]
    hue_value = pixel_center[0]

    color = "Undefined"
    if hue_value < 5:
        color = "RED"
        rotateServo(pin, 30)
    elif hue_value < 22:
        color = "ORANGE"
        rotateServo(pin, 60)
    elif hue_value < 33:
        color = "YELLOW"
        rotateServo(pin, 90)
    elif hue_value < 78:
        color = "GREEN"
        rotateServo(pin, 120)
        Pin_13.write(1)
    elif hue_value < 131:
        color = "BLUE"
        Pin_12.write(1)
        rotateServo(pin, 140)
    elif hue_value < 170:
        color = "VIOLET"
        rotateServo(pin, 180)
    else:
        color = "RED"
        rotateServo(pin, 0)

    pixel_center_bgr = frame[cy, cx]
    b, g, r = int(pixel_center_bgr[0]), int(
        pixel_center_bgr[1]), int(pixel_center_bgr[2])

    cv2.rectangle(frame, (cx - 220, 10), (cx + 200, 120), (255, 255, 255), -1)
    cv2.putText(frame, color, (cx - 200, 100), 0, 3, (b, g, r), 5)
    cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)

    img_resized = cv2.resize(frame, (960, 540))
    cv2.imshow("Frame", img_resized)
    Pin_13.write(0)
    Pin_12.write(0)
    key = cv2.waitKey(1)
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()
