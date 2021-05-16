import pyautogui
from os import path
import time
from datetime import datetime
import pygetwindow
import sys
import numpy as np
from glob import glob
# import ocr
from ocr.cards import ocr_cards
from ocr.digits import ocr_digits
import cv2

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
        DELTA = 5
        # TODO specify region for searching
        regions = {0: (1006 - DELTA, 655 - DELTA, 50 + 2 * DELTA, 41 + 2 * DELTA),
                   1: (709 - DELTA, 495 - DELTA, 50 + 2 * DELTA, 41 + 2 * DELTA),
                   2: (732 - DELTA, 363 - DELTA, 50 + 2 * DELTA, 41 + 2 * DELTA),
                   3: (1214 - DELTA, 270 - DELTA, 50 + 2 * DELTA, 41 + 2 * DELTA),
                   4: (1578 - DELTA, 355 - DELTA, 50 + 2 * DELTA, 41 + 2 * DELTA),
                   5: (1504 - DELTA, 601 - DELTA, 50 + 2 * DELTA, 41 + 2 * DELTA)}
        for player_id in regions.keys():
            button = pyautogui.locateOnScreen(path.join(HERE, 'data', 'signs', 'button.png'),
                                              confidence=0.90,
                                              region=regions[player_id],
                                              grayscale=True)
            # print('Button with coordinates =', button, 'is found')
            if button is not None:
                return player_id

        if button is None:
            sys.exit('Application did not find buttion position!')

        # screen = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screenshot.png'))


        # (left=1578, top=355, width=50, height=41) ID=4
        # (left=1214, top=270, width=50, height=41) ID = 3
        # (left=1504, top=601, width=50, height=41) id = 5
        # (left=732, top=363, width=50, height=41) id = 2
        # (left=709, top=495, width=50, height=41) id = 1
        # (left=1006, top=655, width=50, height=41) id = 0

        # if button is not None:
        #     if button[0]>1006-DELTA and button[0]<1006+DELTA and button[1]>655-DELTA and button[1]<655+DELTA:
        #         button_position = 0
        #     elif button[0]>709-DELTA and button[0]<709+DELTA and button[1]>495-DELTA and button[1]<495+DELTA:
        #         button_position = 1
        #     elif button[0]>732-DELTA and button[0]<732+DELTA and button[1]>363-DELTA and button[1]<363+DELTA:
        #         button_position = 2
        #     elif button[0]>1214-DELTA and button[0]<1214+DELTA and button[1]>270-DELTA and button[1]<270+DELTA:
        #         button_position = 3
        #     elif button[0]>1578-DELTA and button<1578+DELTA and button[1]>355-DELTA and button[1]<355+DELTA:
        #             button_position = 4
        #     elif button[0]>1504-DELTA and button[0]<1504+DELTA and button[1]>601-DELTA and button[1]<601-DELTA:
        #         button_position = 5
        #     else:
        #         pass
        #         sys.exit('Application did not find buttion position!')
        # else:
        #     pass
        #     sys.exit('Application did not find buttion position!')
        # return button_position

    def get_sitting_out_players(self):
        DELTA = 5
        sitting_out_players = []
        # TODO specify region for searching
        # key is ID of player. 0 - is our id
        regions = {1:(507-DELTA, 611-DELTA, 131+2*DELTA, 21+2*DELTA),
                   2:(553-DELTA, 290-DELTA, 131+2*DELTA, 21+2*DELTA),
                   3:(1073-DELTA, 190-DELTA, 131+2*DELTA, 21+2*DELTA),
                   4:(1664-DELTA, 290-DELTA, 131+2*DELTA, 21+2*DELTA),
                   5:(1710-DELTA, 611-DELTA, 131+2*DELTA, 21+2*DELTA)}

        for player_id in regions.keys():
            sitting_out = pyautogui.locateOnScreen(path.join(HERE, 'data', 'signs', 'sitting_out.png'),
                                                   confidence=0.90,
                                                   region=regions[player_id],
                                                   grayscale=True)
            # print('Sitting_out with coordinates =', sitting_out, 'is found')

            if sitting_out is not None:
                sitting_out_players.append(player_id)

        # (left=1710, top=611, width=131, height=21) id = 5
        # (left=1664, top=290, width=131, height=21) id = 4

        # (left=1073, top=190, width=131, height=21) id = 3
        # (left=553, top=290, width=131, height=21) id = 2
        # (left=1710, top=611, width=131, height=21) id = 5
        # Box(left=507, top=611, width=131, height=21) id = 1

        # if sitting_out is not None:
        #     if sitting_out[0]>1006-DELTA and sitting_out[0]<1006+delta and sitting_out[1]>655-delta and sitting_out[1]<655+delta:
        #         button_position = 0
        #     elif sitting_out[0]>709-DELTA and sitting_out[0]<709+delta and sitting_out[1]>495-delta and sitting_out[1]<495+delta:
        #         button_position = 1
        #     elif sitting_out[0]>732-DELTA and sitting_out[0]<732+delta and sitting_out[1]>363-delta and sitting_out[1]<363+delta:
        #         button_position = 2
        #     elif sitting_out[0]>1214-delta and sitting_out[0]<1214+delta and sitting_out[1]>270-delta and sitting_out[1]<270+delta:
        #         button_position = 3
        #     elif sitting_out[0]>1578-delta and sitting_out<1578+delta and sitting_out[1]>355-delta and sitting_out[1]<355+delta:
        #             button_position = 4
        #     elif sitting_out[0]>1504-delta and sitting_out[0]<1504+delta and sitting_out[1]>601-delta and sitting_out[1]<601-delta:
        #         button_position = 5
        #     else:
        #         pass
        #         sys.exit('Application did not find buttion position!')
        # else:
        #     pass
        #     sys.exit('Application did not find buttion position!')

        return sitting_out_players

    def get_bets(self):
        DELTA = 0
        bets = {}
        regions = {1: (805 - DELTA, 568 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA),
                   2: (825 - DELTA, 349 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA),
                   3: (1240 - DELTA, 250 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA),
                   4: (1230 - DELTA, 313 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA),
                   5: (1270 - DELTA, 568 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA)}

        for player_id in regions.keys():
            bet_screen_PIL = pyautogui.screenshot(
                path.join(HERE, 'data', 'screenshots', f'bet_screen_{player_id}.png'),
                region=regions[player_id]
            )
            # convert PIL image to opencv format
            bet_screen_CV = np.array(bet_screen_PIL)
            # cv2.imwrite(f'bet_screen_CV{player_id}.png', bet_screen_CV)
            bets[player_id] = ocr_digits.get_number(bet_screen_CV)

        return bets
            # print(ocr.get_number(screen_digits_3_CV))

        # screen = pyautogui.screenshot(path.join(screenshots_path, 'screenshot.png'),
        #                               region = (1240, 250, 160, 23))
        # screen_digits_1_PIL = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screen_digits_1_PIL.png'),
        #                                            region=(805, 568, 270, 23)
        #                                            )
        #
        # screen_digits_2_PIL = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screen_digits_5_PIL.png'),
        #                                            region=(825, 349, 270, 23)
        #                                            )
        # screen_digits_3_PIL = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screen_digits_5_PIL.png'),
        #                                            region=(1240, 250, 270, 23)
        #                                            )
        #
        # screen_digits_4_PIL = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screen_digits_5_PIL.png'),
        #                                            region=(1230, 313, 270, 23)
        #                                            )
        # screen_digits_5_PIL = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screen_digits_5_PIL.png'),
        #                                            region=(1270, 568, 270, 23)
        #                                            )

        # break

        # screen_digits_3_PIL = pyautogui.screenshot('screenshots/screen_digits_3_PIL.png', region = (1240, 250, 270, 23))
        # convert PIL image to opencv format
        # screen_digits_3_CV = np.array(screen_digits_3_PIL)
        # import ocr.get_number as ocr
        # print(ocr.get_number(screen_digits_3_CV))

    def get_cards(self):
        DELTA = 0
        cards = {}
        # (left=940, top=382, width=24, height=48)
        # (left=1036, top=382, width=24, height=48)
        # (left=1132, top=382, width=23, height=48)
        # (left=1228, top=382, width=24, height=48)
        # (left=1323, top=382, width=24, height=48)

        # (left=1177, top=685, width=24, height=48)
        # (left=1087, top=686, width=24, height=48)
        regions = {1: (1177 - DELTA, 685 - DELTA, 24 + 2 * DELTA, 48 + 2 * DELTA),
                   2: (1087 - DELTA, 686 - DELTA, 24 + 2 * DELTA, 48 + 2 * DELTA)}

        for card_id in regions.keys():
            card_screen_PIL = pyautogui.screenshot(
                path.join(HERE, 'data', 'screenshots', f'card_screen_{card_id}.png'),
                region=regions[card_id]
            )
            # convert PIL image to opencv format
            card_screen_CV = cv2.cvtColor(np.array(card_screen_PIL), cv2.COLOR_RGB2BGR)
            # cv2.imwrite(f'bet_screen_CV{player_id}.png', bet_screen_CV)
            cards[card_id] = ocr_cards.get_card_rank_value(card_screen_CV)

        return cards

if __name__ == '__main__':
    time.sleep(4)

    game = Game()
    game.set_work_position()

    round = Round()

    # screen = pyautogui.screenshot('screenshot.png',
    #                               region=(900, 370, 100, 48))

    # sys.exit('ff')

    while True:
        time.sleep(1)

        if round.is_started():
            print('ROUND IS STARTED!')
        #     screen = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screenshot.png'))
            print('button position = ', round.get_button_position())
            print('bets = ', round.get_bets())
            print('cards = ', round.get_cards())
            break

######

        # pictures_path = sorted(glob(path.join(r'D:\Development\PyCharm\rlcard\ocr\cards\data\pictures', '*.png')))
        # print('pictures_path = ', pictures_path)

        # screen = pyautogui.screenshot(path.join(screenshots_path, 'screenshot.png'),
        #                               region=(970, 220, 450, 70))

        # pyautogui.moveTo(50, 100)
        # for picture_path in pictures_path:
        #     print(picture_path)
        #     picture = pyautogui.locateOnScreen(picture_path,
        #                                        confidence=0.90,
        #                                        region=(900, 370, 100, 150),
        #                                        grayscale=False)
        #
        #     if picture is not None:
        #         print('picture = ',picture)
        #         print(f'{datetime.now()} picture_is_found ')
                # (left=940, top=382, width=24, height=48)
                # (left=1036, top=382, width=24, height=48)
                # (left=1132, top=382, width=23, height=48)
                # (left=1228, top=382, width=24, height=48)
                # (left=1323, top=382, width=24, height=48)

                # (left=1177, top=685, width=24, height=48)
                # (left=1087, top=686, width=24, height=48)

                # break


            ######
            # break
        # break
        # get_digits()
        # get_initial_data()
        # if is_round_started():
        #     print('ROUND IS STARTED!')
        # screen = pyautogui.screenshot(path.join(screenshots_path, 'screenshot.png'),
        #                               region=(970, 220, 450, 70))

        # break



