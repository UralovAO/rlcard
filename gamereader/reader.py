import pyautogui
from os import path
import time
from datetime import datetime
import pygetwindow
import sys
import numpy as np

HERE = path.abspath(path.dirname(__file__))
# screenshots_path = path.join(HERE, 'screenshots')

class Game(object):
    def set_work_position(self):
        game_window = pygetwindow.getActiveWindow()
        # print('win.title= ', win.title)
        width = int(960 * 1.6)
        hight = int(540 * 1.6)
        left = 1920 - width + 30
        top = 0
        game_window.moveTo(left, top)
        game_window.size = (width, hight)

class Round(object):

    def is_started(self):
        start_time = datetime.now()
        start_sign = pyautogui.locateOnScreen(path.join(HERE, 'data', 'signs', 'start_round.png'),
                                              region=(1756-10, 970-10, 153+20, 48+20),
                                              grayscale=True,
                                              confidence=0.95
                                              )
        # screen = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screenshot.png'),
        #                               region=((1166-5, 964-5, 243+10, 21+10)))
        # screen = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screenshot1.png'))
        # raise_to = pyautogui.locateOnScreen(path.join(HERE, 'pictures', 'raise_to.png'))#,
                                            # region=(1721-20, 778-20, 191+40, 40+40))#, grayscale=True)
        finish_time = datetime.now()
        timedelta = finish_time - start_time
        # print('Start round sign with coordinates =', start_sign, 'is found for', timedelta.microseconds, 'microseconds')
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

        if start_sign is None:
            return True
        else:
            return False

    def get_button_position(self):
        delta = 5
        button = pyautogui.locateOnScreen(path.join(HERE, 'data', 'signs', 'button.png'),
                                          confidence=0.90,
                                          grayscale=True)
        # screen = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screenshot.png'))
        print('Button with coordinates =', button, 'is found')

        # (left=1578, top=355, width=50, height=41) ID=4
        # (left=1214, top=270, width=50, height=41) ID = 3
        # (left=1504, top=601, width=50, height=41) id = 5
        # (left=732, top=363, width=50, height=41) id = 2
        # (left=709, top=495, width=50, height=41) id = 1
        # (left=1006, top=655, width=50, height=41) id = 0
        
        if button is not None:
            if button[0]>1006-delta and button[0]<1006+delta and button[1]>655-delta and button[1]<655+delta:
                button_position = 0
            elif button[0]>709-delta and button[0]<709+delta and button[1]>495-delta and button[1]<495+delta:
                button_position = 1
            elif button[0]>732-delta and button[0]<732+delta and button[1]>363-delta and button[1]<363+delta:
                button_position = 2
            elif button[0]>1214-delta and button[0]<1214+delta and button[1]>270-delta and button[1]<270+delta:
                button_position = 3
            elif button[0]>1578-delta and button<1578+delta and button[1]>355-delta and button[1]<355+delta:
                    button_position = 4
            elif button[0]>1504-delta and button[0]<1504+delta and button[1]>601-delta and button[1]<601-delta:
                button_position = 5
            else:
                pass
                sys.exit('Application did not find buttion position!')
        else:
            pass
            sys.exit('Application did not find buttion position!')
        return button_position

    def get_sitting_out(self):
        sitting_out = pyautogui.locateOnScreen(path.join(HERE, 'data', 'signs', 'sitting_out.png'),
                                          confidence=0.90,
                                          grayscale=True)
        print('Sitting_out with coordinates =', sitting_out, 'is found')
        # (left=1710, top=611, width=131, height=21) id = 5
        # (left=1664, top=290, width=131, height=21) id = 4

        # (left=1073, top=190, width=131, height=21) id = 3
        # (left=553, top=290, width=131, height=21) id = 2
        # (left=1710, top=611, width=131, height=21) id = 5
        # Box(left=507, top=611, width=131, height=21) id = 1

        return sitting_out

def get_initial_data():

    start_time = datetime.now()
    dealer_sign = pyautogui.locateOnScreen(path.join(HERE, 'pictures', 'dealer_sign.png'),
                                           confidence=0.90
                                           # grayscale=True # dont use grascale because such picture can be on avatar of a player
                                           )
    finish_time = datetime.now()
    timedelta = finish_time - start_time
    print('Dealer sign with coordinates =', dealer_sign, 'is found for', timedelta.microseconds, 'microseconds')
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

def get_digits():
    # region = (970, 220, 450, 70) - area for searching digits if player with id 3
    digits = []
    # start_time = datetime.now()
    zeros = pyautogui.locateAllOnScreen(path.join(HERE, 'pictures/digits', '0.png'),
                                        region=(970, 220, 450, 70),
                                        # grayscale=True,
                                        confidence=0.9
                                        )

    digits.append([0 for x in range(len(list(zeros)))])

    ones = pyautogui.locateAllOnScreen(path.join(HERE, 'pictures/digits', '1.png'),
                                        region=(970, 220, 450, 70),
                                        # grayscale=True,
                                        confidence=0.85
                                        )

    digits.append([1 for x in range(len(list(ones)))])

    if len(digits[0]) > 0 and len(digits[1]) > 0:
        print('digits = ', digits)

    # finish_time = datetime.now()
    # timedelta = finish_time - start_time
    # print('zeros with coordinates =', zeros, 'is found for', timedelta.microseconds, 'microseconds')
    # screen = pyautogui.screenshot(path.join(screenshots_path, 'screenshot.png'))
    # n = 0
    # for s in zeros:
    #     print('s=', s)
    #     n = n + 1
    #
    # if n > 0:
    #     sys.exit('ok')


if __name__ == '__main__':
    time.sleep(5)

    game = Game()
    game.set_work_position()

    round = Round()


    # if raise_to is None and 1==2:

    while True:
        time.sleep(1)

        if round.is_started() or 1==1:
            print('ROUND IS STARTED!')
            print('button_position = ', round.get_button_position())
            round.get_sitting_out()


        # screen = pyautogui.screenshot(path.join(screenshots_path, 'screenshot.png'),
        #                               region = (1240, 250, 160, 23))
        screen_digits_1_PIL = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screen_digits_1_PIL.png'),
                                                   region=(805, 568, 270, 23)
                                                   )

        screen_digits_2_PIL = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screen_digits_5_PIL.png'),
                                                   region=(825, 349, 270, 23)
                                                   )
        screen_digits_3_PIL = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screen_digits_5_PIL.png'),
                                                   region=(1240, 250, 270, 23)
                                                   )

        screen_digits_4_PIL = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screen_digits_5_PIL.png'),
                                                   region=(1230, 313, 270, 23)
                                                   )
        screen_digits_5_PIL = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screen_digits_5_PIL.png'),
                                                   region=(1270, 568, 270, 23)
                                                   )

        # break

        # screen_digits_3_PIL = pyautogui.screenshot('screenshots/screen_digits_3_PIL.png', region = (1240, 250, 270, 23))
        # convert PIL image to opencv format
        # screen_digits_3_CV = np.array(screen_digits_3_PIL)
        # import ocr.get_number as ocr
        # print(ocr.get_number(screen_digits_3_CV))


        # break
        # get_digits()
        # get_initial_data()
        # if is_round_started():
        #     print('ROUND IS STARTED!')
        # screen = pyautogui.screenshot(path.join(screenshots_path, 'screenshot.png'),
        #                               region=(970, 220, 450, 70))

        # break



