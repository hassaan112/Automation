import numpy as np
import cv2 as cv
from mss import mss
import keyboard
import win32api, win32con
import ctypes
import os

mouseEvent = 'a'

def click(x,y): # win32api function for clicking on the targets
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0) # pressing down left click
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0) # releasing left click (moved this line at the end of 
                                                                # the program for maximum speeds)


def click_ctypes(x,y): # optional ctype implementation of clicking
    ctypes.windll.user32.SetCursorPos(x,y)
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)

referenceNum = 1

templates = []
for i in range(1, 51):
    templates.append(cv.imread(f'{os.path.dirname(__file__)}/references/{i}.png', 0))

with mss() as sct:
    monitor = sct.monitors[1]
    left = monitor["left"] + monitor["width"] * 36 // 100  # 35% away from the left
    top = monitor["top"] + monitor["height"] * 16 // 100  # 15% away from the top
    right = left + 500  # 500px width
    lower = top + 320 # 320px height
    bbox = (left, top, right, lower)

    while True:

        screen = sct.grab(bbox) # current image of screen
        img_gray = np.array(screen)[:,:,1] # since the images we are looking for are already in grayscale, simply 
                                            # choosing the first color value of the rgba gives us the grayscale 

        res = cv.matchTemplate(img_gray, templates[referenceNum-1], cv.TM_CCOEFF_NORMED) # finding image on screen
        min_val, LocatedPrecision, min_loc, (x,y) = cv.minMaxLoc(res)

        if LocatedPrecision > 0.9: # checking if result is precise (play with the integer value to achieve max speed)
                                    # (at the cost of increasing risk of program failing)
            click(x+left, y+top) # left and top added to compensate for the small detection window

            referenceNum += 1
            if referenceNum > 50:
                break # self-stopping after finished

        if keyboard.is_pressed('q'): # for stopping program midway (comment this code out for max speeds)
            break


win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
