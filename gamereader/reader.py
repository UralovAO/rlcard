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

# screen = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screenshot.png'),
#                               region=((1166-5, 964-5, 243+10, 21+10)))


class Screen(object):
    def set_work_position(self):
        game_window = pygetwindow.getActiveWindow()
        # print('win.title= ', win.title)
        width = int(960 * 1.6)
        hight = int(540 * 1.6)
        left = 1920 - width + 30
        top = 0
        game_window.moveTo(left, top)
        game_window.size = (width, hight)

    def get_button_position(self):
        DELTA = 5
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

    def __get_card_by_region(self, region):
        card_screen_PIL = pyautogui.screenshot(region=region)
        # convert PIL image to opencv format
        card_screen_CV = cv2.cvtColor(np.array(card_screen_PIL), cv2.COLOR_RGB2BGR)
        return ocr_cards.get_card(card_screen_CV)

    def get_flop_cards(self):
        DELTA = 0
        cards = {}

        regions = {1: (940 - DELTA, 382 - DELTA, 24 + 2 * DELTA, 48 + 2 * DELTA),
                   2: (1036 - DELTA, 382 - DELTA, 24 + 2 * DELTA, 48 + 2 * DELTA),
                   3: (1132 - DELTA, 382 - DELTA, 24 + 2 * DELTA, 48 + 2 * DELTA)}

        for card_id in regions.keys():
            cards[card_id] = self.__get_card_by_region(regions[card_id])

        return cards

    def get_river_card(self):
        DELTA = 0
        card = self.__get_card_by_region((1323 - DELTA, 382 - DELTA, 24 + 2 * DELTA, 48 + 2 * DELTA))
        return card

    def get_turn_card(self):
        DELTA = 0
        card = self.__get_card_by_region((1228 - DELTA, 382 - DELTA, 24 + 2 * DELTA, 48 + 2 * DELTA))
        return card

    def get_player_cards(self):
        DELTA = 0
        cards = {}
        regions = {1: (1177 - DELTA, 685 - DELTA, 24 + 2 * DELTA, 48 + 2 * DELTA),
                   2: (1087 - DELTA, 686 - DELTA, 24 + 2 * DELTA, 48 + 2 * DELTA)}

        for card_id in regions.keys():
            cards[card_id] = self.__get_card_by_region(regions[card_id])
        return cards

    def get_no_bet_button(self):
        DELTA = 10
        no_bet_button = pyautogui.locateOnScreen(path.join(HERE, 'data', 'signs', 'no_bet_button.png'),
                                                 region=(1756 - DELTA, 970 - DELTA, 153 + 2 * DELTA, 48 + 2 * DELTA),
                                                 grayscale=True,
                                                 confidence=0.95
                                                 )
        return no_bet_button

    def get_folded_players(self):
        # Box(left=1088, top=99, width=79, height=25)
        # Box(left=1178, top=99, width=79, height=25)
        # Box(left=569, top=199, width=79, height=25)
        # Box(left=659, top=199, width=79, height=25)
        # Box(left=1607, top=199, width=79, height=25)
        # Box(left=1697, top=199, width=79, height=25)
        # Box(left=522, top=520, width=79, height=25)
        # Box(left=612, top=520, width=79, height=25)
        # Box(left=1654, top=520, width=79, height=25)
        # Box(left=1744, top=520, width=79, height=25)
        # Box(left=1088, top=709, width=79, height=25)
        # Box(left=1178, top=709, width=79, height=25)
        DELTA = 0
        folded_players = []
        regions = {1: (522 - DELTA, 520 - DELTA, 79 + 2 * DELTA, 25 + 2 * DELTA),
                   2: (569 - DELTA, 199 - DELTA, 79 + 2 * DELTA, 25 + 2 * DELTA),
                   3: (1088 - DELTA, 99 - DELTA, 79 + 2 * DELTA, 25 + 2 * DELTA),
                   4: (1607 - DELTA, 199 - DELTA, 79 + 2 * DELTA, 25 + 2 * DELTA),
                   5: (1654 - DELTA, 520 - DELTA, 79 + 2 * DELTA, 25 + 2 * DELTA)}

        for player_id in regions.keys():
            card = pyautogui.locateOnScreen(path.join(HERE, 'data', 'signs', 'card.png'),
                                              confidence=0.95,
                                              region=regions[player_id],
                                              grayscale=False)
            # print('Button with coordinates =', button, 'is found')
            if card is None:
                folded_players.append(player_id)

        return folded_players

class Game(object):
    # def __init__(self):
    #     self.current_stage
    def set_button_position(self):
        screen = Screen()
        self.button_position = screen.get_button_position()

    def get_button_position(self):
        if self.button_position is not None:
            return self.button_position
        else:
            sys.exit('Buttion position is not initialised!')

    def set_bets(self):
        screen = Screen()
        self.bets = screen.get_bets()

    def get_bets(self):
        return self.bets

    def set_pot(self):
        self.pot = sum(filter(lambda x: x is not None, self.bets.values()))

    def get_pot(self):
        return self.pot


    def wait_for_bet_button(self):
        screen = Screen()
        while True:
            no_bet_button = screen.get_no_bet_button()
            # no_bet_button = pyautogui.locateOnScreen(path.join(HERE, 'data', 'signs', 'no_bet_button.png'),
            #                                       region=(1756 - DELTA, 970 - DELTA, 153 + 2*DELTA, 48 + 2*DELTA),
            #                                       grayscale=True,
            #                                       confidence=0.95
            #                                       )
            if no_bet_button is None:
                return True
            else:
                time.sleep(0.5)


    def wait_for_player_bet(self):
        while True:
            no_bet_button = screen.get_no_bet_button()
            # no_bet_button = pyautogui.locateOnScreen(path.join(HERE, 'data', 'signs', 'no_bet_button.png'),
            #                                          region=(1756 - 10, 970 - 10, 153 + 20, 48 + 20),
            #                                          grayscale=True,
            #                                          confidence=0.95
            #                                          )
            if no_bet_button is None:
                time.sleep(0.5)
                # return False
                pass
            else:
                return True

    def set_community_cards(self):
        screen = Screen()
        self.river_card = screen.get_river_card()
        self.turn_card = screen.get_turn_card()
        self.flop_cards = screen.get_flop_cards()

    def set_current_street(self):
        if self.river_card is not None:
            self.current_street = 'RIVER'
        else:
            if self.turn_card is not None:
                self.current_street = 'TURN'
            else:
                if len(list(filter(lambda x: x is not None, self.flop_cards.values()))) > 0:
                    self.current_street = 'FLOP'
                else:
                    self.current_street = 'PREFLOP'

    def get_current_street(self):
        return self.current_street

    def set_player_cards(self):
        screen = Screen()
        self.player_cards = screen.get_player_cards()

    def get_player_cards(self):
        return self.player_cards

    def get_flop_cards(self):
        if self.flop_cards is not None:
            return self.flop_cards
        else:
            sys.exit('Flop cards is undefined')

    def get_turn_card(self):
        if self.turn_card is not None:
            return self.turn_card
        else:
            sys.exit('Turn card is undefined')

    def get_river_card(self):
        if self.river_card is not None:
            return self.river_card
        else:
            sys.exit('River card is undefined')

    def set_folded_players(self):
        screen = Screen()
        self.folded_players = screen.get_folded_players()

    def get_folded_players(self):
        return self.folded_players

    def set_current_decisions(self):

        button_position = self.get_button_position()
        bets = self.get_bets()
        pot = self.get_pot()
        folded_players = self.get_folded_players()
        self.current_decisions = {}

        previous_bet = BIG_BLIND
        # is_previous_allin = False

        # we need decisions only after BB position and before ours
        # this decisions we pass to AI
        for player_id in range(button_position+2, 6):
            if player_id in folded_players:
                self.current_decisions[player_id] = 'FOLD'
            elif bets[player_id] is None:
                self.current_decisions[player_id] = 'CHECK'
            elif 'ALL_IN' in list(self.current_decisions.values()):
            # elif is_previous_allin  == True:
                self.current_decisions[player_id] = 'CALL'
            elif bets[player_id] == previous_bet:
                self.current_decisions[player_id] = 'CALL'
            elif bets[player_id] > previous_bet and bets[player_id] <= (3 * pot / 4):
                self.current_decisions[player_id] = 'RAISE_HALF_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > (3 * pot / 4) and bets[player_id] <= pot + (100 * BIG_BLIND - pot) / 2:
                self.current_decisions[player_id] = 'RAISE_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > pot + (100 * BIG_BLIND - pot) / 2:
                self.current_decisions[player_id] = 'ALL_IN'
                previous_bet = bets[player_id]
                # is_previous_allin = True
            else:
                sys.exit('Error. Application can not define decision!')

        return current_decisions
        pass

    def get_current_decisions(self):
        return self.current_decisions

    def set_previous_decisions(self):

        button_position = self.get_button_position()
        bets = self.get_bets()
        pot = self.get_pot()
        folded_players = self.get_folded_players()

        self.previous_decisions = self.current_decisions

        previous_bet = self.previous_decisions[0] # get player's (our) bet
        is_previous_allin = False

        for player_id in range(1, button_position+2):
            if player_id in folded_players:
                self.previous_decisions[player_id] = 'FOLD'
            elif 'ALL_IN' in list(self.previous_decisions.values()):
                self.previous_decisions[player_id] = 'CALL'
            elif player_id == button_position + 2 and bets[player_id] == BIG_BLIND: # check on BB position
                self.previous_decisions[player_id] = 'CHECK'
            # elif is_previous_allin  == True:
            #     self.current_decisions[player_id] = 'CALL'
            elif bets[player_id] == previous_bet:
                self.previous_decisions[player_id] = 'CALL'
            elif bets[player_id] > previous_bet and bets[player_id] <= (3 * pot / 4):
                self.previous_decisions[player_id] = 'RAISE_HALF_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > (3 * pot / 4) and bets[player_id] <= pot + (100 * BIG_BLIND - pot) / 2:
                self.previous_decisions[player_id] = 'RAISE_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > pot + 3*(100 * BIG_BLIND - pot) / 4:
                self.previous_decisions[player_id] = 'ALL_IN'
                previous_bet = bets[player_id]
                is_previous_allin = True
            else:
                sys.exit('Error. Application can not define decision!')

    def get_previous_decisions(self):
        return self.previous_decisions

# class RoundState(object):
#     button_position
#     bets
#     player_cards
#     flop_cards
#     turn_card
#     river_card
#     decisions


if __name__ == '__main__':
    time.sleep(4)

    screen = Screen()
    screen.set_work_position()

    game = Game()

    # print('folded = ', screen.get_folded_players())
    # sys.exit('g')
    is_first_round = True
    previous_street = None

    while True:
        if game.wait_for_bet_button(): # waiting for other players finishes placing their bets if necessary

            # read game data from screen
            game.set_community_cards()
            game.set_player_cards()
            game.set_current_street()
            game.set_button_position()
            game.set_bets()
            game.set_folded_players()
            # game.set_previous_decisions()
            # game.set_current_decisions()

            street = game.get_current_street()
            if street == previous_street:
                is_first_round = False

            if is_first_round:
                game.set_decisions_after_BB()
            else:
                game.set_decisions_before_BB()
                game.set_decisions_after_BB()

            print(street)
            print('button = ', game.get_button_position())
            if street == 'PREFLOP':
                print('bets = ', game.get_bets())
                print('player_cards = ', game.get_player_cards())
                # print('community_cards = ', preflop.get_community_cards())
            elif street == 'FLOP':
                print('bets = ', game.get_bets())
                # print('player_cards = ', flop.get_player_cards())
                print('flop_cards = ', game.get_flop_cards())
            elif street == 'TURN':
                print('bets = ', game.get_bets())
                print('turn_cards = ', game.get_turn_card())
            elif street == 'RIVER':
                print('bets = ', game.get_bets())
                # print('player_cards = ', flop.get_player_cards())
                print('river_cards = ', game.get_river_card())

            previous_street = street

            # we gave data to model
            # model gave us back answer
            if game.wait_for_player_bet():
                pass

        # if stage == 'PREFLOP':







    # while True:
    #     time.sleep(1)
    # preflop = Preflop()
    # if preflop.is_started():
    #     print('GAME IS STARTED!')
    #     print('button position = ', game.get_button_position())
    #     print('bets = ', preflop.get_bets())
    #     print('player_cards = ', preflop.get_player_cards())
    #
    #     if preflop.bet_is_placed():
    #         stage = game.get_current_stage()
    #         if stage == 'PREFLOP':
    #
    #
    #
    #         if preflop.is_finished():
    #
    #
    #
    #         flop = Flop()
    #         if flop.is_started():
    #
    #         break

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



