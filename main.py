import numpy as np
import os
import time
from threading import Thread
from pynput import keyboard
import cv2 as cv
from ctypes import *
from time import sleep
from mss import mss
import win32.lib.win32con as win32con
import math

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
    sleep(delay())
    user32.mouse_event(button[0], 0, 0, 0, 0)
    sleep(delay())
    user32.mouse_event(button[1], 0, 0, 0, 0)


# Holds a mouse button
def holdclick(button):
    user32.mouse_event(button[0], 0, 0, 0, 0)


# Releases a mouse button
def releaseclick(button):
    user32.mouse_event(button[1])
    sleep(delay())


def trigger():
    start_time = time.time()
    area = 12
    mon = {"top": int(429 - area / 2), "left": int(959 - 1920 - area / 2), "width": area, "height": area}
    with mss() as sct:
        while True:
            if user32.GetKeyState(win32con.VK_RBUTTON) >= 65408 or user32.GetKeyState(win32con.VK_SPACE) >= 65408:
                last_time = time.time()
                img = sct.grab(mon)
                img = np.array(img)
                imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)

                lower_mask = np.array([144, 160, 149])
                upper_mask = np.array([155, 255, 255])

                mask = cv.inRange(imgHSV, lower_mask, upper_mask)

                borderClamp = cv.bitwise_and(img, img, mask=mask)

                grayImage = cv.cvtColor(borderClamp, cv.COLOR_BGR2GRAY)

                (thresh, blackAndWhiteImage) = cv.threshold(grayImage, 70, 255, cv.THRESH_BINARY)
                cv.imshow("test", blackAndWhiteImage)
                draw("test", blackAndWhiteImage, -100, 60)
                draw("test2", img, -100, 30)
                binMatrix = np.array(blackAndWhiteImage)

                isFullBlack = np.all(binMatrix == 0)
                isFullWhite = np.all(binMatrix == 255)
                print(f"EXPR: is full white: {isFullWhite}, is full black: {isFullBlack}")
                if isFullBlack == isFullWhite:
                    click(mouse.left)
                else:
                    pass

                print("speed in fps: {0}".format((time.time() - last_time) ** (-1)))
            if cv.waitKey(1) == ord("-"):
                cv.destroyAllWindows()
                break

    print("Done!")


def debug():
    # test hsv values with or
    cv.namedWindow("params")
    cv.moveWindow("params", -1920 + 5, 50)
    cv.resizeWindow("params", 640, 320)

    cv.createTrackbar("hue_min", "params", -180, 180, empty)
    cv.createTrackbar("hue_max", "params", 180, 180, empty)

    cv.createTrackbar("val_min", "params", 0, 255, empty)
    cv.createTrackbar("val_max", "params", 255, 255, empty)

    cv.createTrackbar("sat_min", "params", 0, 255, empty)
    cv.createTrackbar("sat_max", "params", 255, 255, empty)

    #

    while True:

        img = cv.imread("hsv.png")
        img = np.array(img)
        imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        hue_min = cv.getTrackbarPos("hue_min", "params")
        hue_max = cv.getTrackbarPos("hue_max", "params")

        sat_min = cv.getTrackbarPos("sat_min", "params")
        sat_max = cv.getTrackbarPos("sat_max", "params")

        val_min = cv.getTrackbarPos("val_min", "params")
        val_max = cv.getTrackbarPos("val_max", "params")

        lower_mask = np.array([hue_min, sat_min, val_min])
        upper_mask = np.array([hue_max, sat_max, val_max])

        mask = cv.inRange(imgHSV, lower_mask, upper_mask)

        result = cv.bitwise_or(img, img, mask=mask)

        cv.namedWindow("result")
        cv.imshow("result", result)

        if cv.waitKey(1) == ord("-"):
            cv.destroyAllWindows()
            break

    print("Done!")


def empty(arg):
    pass


def debug2():
    # debug values

    cv.namedWindow("params")
    cv.moveWindow("params", -1920 + 5, 50)
    cv.resizeWindow("params", 640, 600)
    cv.createTrackbar("threshold1", "params", 150, 255, empty)
    cv.createTrackbar("threshold2", "params", 150, 255, empty)

    cv.createTrackbar("hue_min", "params", 0, 180, empty)
    cv.createTrackbar("hue_max", "params", 180, 180, empty)

    cv.createTrackbar("val_min", "params", 0, 255, empty)
    cv.createTrackbar("val_max", "params", 255, 255, empty)

    cv.createTrackbar("sat_min", "params", 0, 255, empty)
    cv.createTrackbar("sat_max", "params", 255, 255, empty)

    #
    area = 140

    mon = {"top": int(429 - area / 2), "left": int(959 - 1920 - area / 2), "width": area, "height": area}
    with mss() as sct:
        while True:
            # if user32.GetKeyState(win32con.VK_LCONTROL) >= 65408:

            img = sct.grab(mon)
            img = np.array(img)
            imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)

            hue_min = cv.getTrackbarPos("hue_min", "params")
            hue_max = cv.getTrackbarPos("hue_max", "params")

            sat_min = cv.getTrackbarPos("sat_min", "params")
            sat_max = cv.getTrackbarPos("sat_max", "params")

            val_min = cv.getTrackbarPos("val_min", "params")
            val_max = cv.getTrackbarPos("val_max", "params")

            lower_mask = np.array([hue_min, sat_min, val_min])
            upper_mask = np.array([hue_max, sat_max, val_max])

            mask = cv.inRange(imgHSV, lower_mask, upper_mask)

            result = cv.bitwise_and(img, img, mask=mask)

            cv.namedWindow("original")
            cv.moveWindow("original", -200, 100)
            cv.imshow("original", img)

            cv.namedWindow("result")
            cv.moveWindow("result", -200, 300)
            cv.imshow("result", result)

            cv.namedWindow("mask")
            cv.moveWindow("mask", -200, 500)
            cv.imshow("mask", mask)

            if cv.waitKey(1) == ord("-"):
                cv.destroyAllWindows()
                break

    print("Done!")


def draw(windowName, img, x, y):
    cv.namedWindow(windowName)
    cv.moveWindow(windowName, x, y)
    cv.imshow(windowName, img)


def aim():
    # debug values
    kernel = np.ones((3, 3), np.float32) / 9
    area = 200

    mon = {"top": int(429 - area / 2), "left": int(959 - 1920 - area / 2), "width": area, "height": area}
    with mss() as sct:
        while True:
            if user32.GetKeyState(win32con.VK_LCONTROL) >= 65408 or True:

                img = sct.grab(mon)
                img = np.array(img)

                imgHSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)

                lower_mask = np.array([135, 110, 124])
                upper_mask = np.array([160, 255, 255])

                mask = cv.inRange(imgHSV, lower_mask, upper_mask)

                borderClamp = cv.bitwise_and(img, img, mask=mask)

                grayImage = cv.cvtColor(borderClamp, cv.COLOR_BGR2GRAY)

                (thresh, blackAndWhiteImage) = cv.threshold(grayImage, 70, 255, cv.THRESH_BINARY)
                draw("result", blackAndWhiteImage, -300, 400)

                contours, hierarchy = cv.findContours(blackAndWhiteImage, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
                # debug only
                cx = 0
                cy = 0
                for i in contours:
                    area = cv.contourArea(i)
                    if area >= 50 and area <= 90:
                        M = cv.moments(i)
                        if M["m00"] != 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                            cv.drawContours(img, [i], -1, (0, 255, 0), 2)
                            cv.circle(img, (cx, cy), 7, (0, 0, 255), -1)

                    print(f"x: {cx} y: {cy}")

                # only move mouse if relative coords are != (0,0)

                draw("final", img, -300, 100)

            if cv.waitKey(1) == ord("-"):
                cv.destroyAllWindows()
                break

    print("Done!")


if __name__ == "__main__":
    # WindowCapture.list_window_names()
    Thread(target=trigger).start()
