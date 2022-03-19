import numpy as np
import os
import time
from threading import Thread
from pynput import keyboard
import cv2 as cv
from mss import mss

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# basic ultra fast screen grabber for python


def bot():
    start_time = time.time()
    mon = {"top": 200, "left": 200, "width": 200, "height": 200}
    with mss() as sct:
        while True:
            last_time = time.time()
            img = sct.grab(mon)
            print("The loop took: {0}".format(time.time() - last_time))
            cv.imshow("test", np.array(img))
            if cv.waitKey(1) == ord("-"):
                cv.destroyAllWindows()
                break

    print("Done!")


if __name__ == "__main__":
    # WindowCapture.list_window_names()
    Thread(target=bot).start()
