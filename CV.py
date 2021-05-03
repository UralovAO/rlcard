import pyautogui
from os import path
import time
from datetime import datetime
import pygetwindow
import sys


time.sleep(5)


# win = pygetwindow.getWindowsWithTitle('Notepad')[0]
# gw.getActiveWindow().title
win = pygetwindow.getActiveWindow()
print('win.title= ', win.title)
win.moveTo(0, 0)
win.size = (960, 540)

print('__file__ = ', __file__)
HERE = path.abspath(path.dirname(__file__))
screenshots_path = path.join(HERE, 'screenshots')




def is_round_started():
    start_time = datetime.now()

    bet_button = pyautogui.locateOnScreen(path.join(HERE, 'pictures', 'bet_button.png'),
                                          region=(792-10, 621-10, 150+20, 14+20),
                                          grayscale=True,
                                          confidence=0.90
                                          )

    # raise_to = pyautogui.locateOnScreen(path.join(HERE, 'pictures', 'raise_to.png'))#,
                                        # region=(1721-20, 778-20, 191+40, 40+40))#, grayscale=True)
    finish_time = datetime.now()
    timedelta = finish_time - start_time
    print('Bet_button with coordinates =', bet_button, 'is found for', timedelta.microseconds, 'microseconds')
    # if raise_to is None and 1==2:
    #     start_time = datetime.now()
    #     call = pyautogui.locateOnScreen(path.join(HERE, 'pictures', 'call.png'))#,
    #                                     region=(1721-20, 778-20, 191+40, 40+40))#, grayscale=True)
        # finish_time = datetime.now()
        # timedelta = finish_time - start_time
        # print('Button "Call" with coordinates =', call, 'is found for', timedelta.microseconds, 'microseconds')
        # if call is None:
        #     result = False
        # else:
        #     result = True
    # else:
    #     result = True

    if bet_button is None:
        return False
    else:
        return True

def get_initial_data():

    start_time = datetime.now()
    dealer_sign = pyautogui.locateOnScreen(path.join(HERE, 'pictures', 'dealer_sign.png'),
                                           confidence=0.90
                                           # grayscale=True # dont use grascale because such picture can be on avatar of a player
                                           )
    finish_time = datetime.now()
    timedelta = finish_time - start_time
    # print('Dealer sign with coordinates =', dealer_sign, 'is found for', timedelta.microseconds, 'microseconds')
    if dealer_sign[0] == 377 and dealer_sign[1] == 429:
        dealer_id = 0
    elif dealer_sign[0] == 191 and dealer_sign[1] == 326:
        dealer_id = 1
    elif dealer_sign[0] == 205 and dealer_sign[1] == 243:
        dealer_id = 2
    elif dealer_sign[0] == 507 and dealer_sign[1] == 185:
        dealer_id = 3
    elif dealer_sign[0] == 736 and dealer_sign[1] == 239:
        dealer_id = 4
    elif dealer_sign[0] == 689 and dealer_sign[1] == 393:
        dealer_id = 5
    else:
        pass
        screen = pyautogui.screenshot(path.join(screenshots_path, 'screenshot.png'))
        sys.exit('Can not define dealer_id!')

    print('dealer_id = ',dealer_id)

    # print('dealer_sign[left] = ',dealer_sign[0])
    # Box(left=507, top=185, width=29, height=25) - highest (3)
    # Box(left=191, top=326, width=29, height=25) - lower left (1)
    # Box(left=377, top=427, width=29, height=25) - lowest (0)
    # Box(left=205, top=243, width=29, height=25) - upper left (2)
    # Box(left=736, top=239, width=29, height=25) - upper right (4)
    # Box(left=689, top=393, width=29, height=25) - lower right (5)


    start_time = datetime.now()
    sitting_out = pyautogui.locateAllOnScreen(path.join(HERE, 'pictures', 'sitting_out.png'),
                                           # region=(792 - 10, 621 - 10, 150 + 20, 14 + 20),
                                           grayscale=True,
                                           confidence=0.90
                                           )
    for s in sitting_out:
        print('s=',s)
    finish_time = datetime.now()
    timedelta = finish_time - start_time
    print('sitting_out with coordinates =', sitting_out, 'is found for', timedelta.microseconds, 'microseconds')
    # Box(left=61, top=398, width=85, height=18) - id 1
    # Box(left=90, top=197, width=85, height=18) - id 2
    # Box(left=416, top=133, width=85, height=18) - id 3
    # Box(left=787, top=197, width=85, height=18) - id 4
    # Box(left=817, top=398, width=85, height=18) - id 5



    # if dealer_sign is None:
    #     screen = pyautogui.screenshot(path.join(screenshots_path, 'screenshot.png'))
        # assert 1==3


while True:
    time.sleep(1)
    get_initial_data()
    # if is_round_started():
    #     print('ROUND IS STARTED!')


        # break



