import numpy as np
import os
import time
from threading import Thread
from pynput import keyboard
import cv2 as cv
from ctypes import *
from time import sleep
from mss import mss

os.chdir(os.path.dirname(os.path.abspath(__file__)))

user32 = windll.user32
kernel32 = windll.kernel32


class mouse:
    left = [0x0002, 0x0004]
    right = [0x0008, 0x00010]
    middle = [0x00020, 0x00040]


def delay():
    res = np.random.uniform(0.015, 0.02)
    # print(res)
    return res


# --- Mouse Control Functions ---#


# Moves mouse to a position
def move(x, y):
    user32.SetCursorPos(x, y)


# Presses and releases mouse
def click(button):
    user32.mouse_event(button[0], 0, 0, 0, 0)
    sleep(delay())
    user32.mouse_event(button[1], 0, 0, 0, 0)
    sleep(delay())


# Holds a mouse button
def holdclick(button):
    user32.mouse_event(button[0], 0, 0, 0, 0)


# Releases a mouse button
def releaseclick(button):
    user32.mouse_event(button[1])
    sleep(delay())


def on_change(value):
    print(value)


def bot():

    start_time = time.time()
    mon = {"top": 423, "left": 953 - 1920, "width": 100, "height": 100}
    with mss() as sct:
        while True:
            last_time = time.time()
            img = sct.grab(mon)
            img = np.array(img)
            result = img.copy()
            img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

            lower1 = np.array([0, 100, 0])
            upper1 = np.array([5, 255, 255])

            lower2 = np.array([160, 100, 20])
            upper2 = np.array([179, 255, 255])

            lower_mask = cv.inRange(img, lower1, upper1)
            upper_mask = cv.inRange(img, lower2, upper2)

            full_mask = lower_mask + upper_mask

            result = cv.bitwise_and(result, result, mask=full_mask)
            loop1 = True
            loop2 = True
            cv.imshow("test", result)
            # cv.createTrackbar("slider", "test", 0, 100, on_change)

            # print(f"{len(np.array(img))},{len(np.array(img)[0])}")
            for i in range(0, 10):
                if loop1:
                    for j in range(0, 10):
                        if loop2:
                            triggerB, triggerG, triggerR, triggerA = np.array(result)[i][j]
                            # print(f"[R:{triggerR}, G:{triggerG}, B:{triggerB}]")
                            if (
                                # triggerR in range(200, 240 + 1)
                                # and triggerG in range(20, 91)
                                # and triggerB in range(20, 96)
                                triggerR
                                > 180
                            ):
                                print(f"SEND CLICK")
                                click(mouse.left)
                                # releaseclick(mouse.left)
                                # holdclick(mouse.left)
                                loop1 = False
                                loop2 = False
                        else:

                            break
                else:
                    break
            print("speed in fps: {0}".format((time.time() - last_time) ** (-1)))
            if cv.waitKey(1) == ord("-"):
                cv.destroyAllWindows()
                break

    print("Done!")


if __name__ == "__main__":
    # WindowCapture.list_window_names()
    Thread(target=bot).start()
