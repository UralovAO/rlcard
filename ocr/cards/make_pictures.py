import pyautogui
from os import path
import time
from datetime import datetime
import pygetwindow
import sys
import numpy as np
from glob import glob
from datetime import datetime

HERE = path.abspath(path.dirname(__file__))

time.sleep(4)

game_window = pygetwindow.getActiveWindow()
# print('win.title= ', win.title)
width = int(960 * 1.6)
hight = int(540 * 1.6)
left = 1920 - width + 30
top = 0
game_window.moveTo(left, top)
game_window.size = (width, hight)

while True:
    picture_is_found = False
    pictures_path = sorted(glob(path.join(HERE, 'data', 'pictures', '*.png')))
    # pyautogui.moveTo(50, 100)
    for picture_path in pictures_path:
        # print(picture_path)
        picture = pyautogui.locateOnScreen(picture_path,
                                           confidence=0.90,
                                           region=(1132-5, 382-5, 24+10, 48+10),
                                           grayscale=False)
        if picture is not None:
            picture_is_found = True
            # print(f'{datetime.now()} picture_is_found ')
            break

        # pyautogui.moveTo(100, 200)

    if not picture_is_found:
        screen = pyautogui.screenshot(path.join(HERE, 'data', 'pictures', f'{datetime.timestamp(datetime.now())}.png'),
                                      region=(1132, 382, 24, 48))
        print(f'saved {datetime.timestamp(datetime.now())}.png')


