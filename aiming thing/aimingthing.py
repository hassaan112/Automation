'''
This is a Python script that will automatically play through an online aim test, which can be found over at https://dwlim.github.io/apmtest3/
To use this, simply visit the url on your browser, then run the script while having the browser window active.

NOTE: This script is dependant on your resolution and webpage size, I ran this on 1600x900 resolution, in a full-screen browser and 100% size webpage. Also note that your specific browser will change the position of the canvas, so I have usedslightly larger numbers than needed, the actual size of the canvas on which the targets can appear is 500x300. You can tweak these numbers in lines 41, 42, 43, and 44.
'''

import numpy as np
import cv2 as cv
from mss import mss
import keyboard
import win32api, win32con
import ctypes
import os


def click(x,y): # win32api function for clicking on the targets
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0) # pressing down left click
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0) # releasing left click (moved this line to the end of 
                                                                # the program for maximum speeds)


def click_ctypes(x,y): # optional ctype implementation of clicking function
    ctypes.windll.user32.SetCursorPos(x,y)
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)

referenceNum = 1

# loading the reference images into an array of templates for finding on the screen
templates = []
for i in range(1, 51):
    templates.append(cv.imread(f'{os.path.dirname(__file__)}/references/{i}.png', 0))

with mss() as sct:
    monitor = sct.monitors[1]
    left = monitor["left"] + monitor["width"] * 35 // 100  # 35% away from the left
    top = monitor["top"] + monitor["height"] * 15 // 100  # 15% away from the top
    right = left + 520  # 520px chosen width, 500px actual width 
    lower = top + 320 # 320px chosen height, 300px actual height
    bbox = (left, top, right, lower)

    while True:
        screen = sct.grab(bbox) # grabbing current image of screen
        img_gray = np.array(screen)[:,:,1] # since the images we are looking for are already meant to be in grayscale, 
                                            # simply choosing the first color value of the rgba gives the grayscale.

        res = cv.matchTemplate(img_gray, templates[referenceNum-1], cv.TM_CCOEFF_NORMED) # finding target on screen
        min_val, LocatedPrecision, min_loc, (x,y) = cv.minMaxLoc(res)

        if LocatedPrecision > 0.9: # checking if result is precise (play with the integer value to achieve max speed)
                                    # (the lower the number the risk of program failing, but you can escape with 'q' key)
            click(x+left, y+top) # left and top added to compensate for the partial detection window
            referenceNum += 1
            
            if referenceNum > 50: # stopping program after finished

                break 
        if keyboard.is_pressed('q'): # for manually stopping program midway (comment this code out for max speeds)
            break

win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
