import pyautogui
from os import path, remove
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

MAX_PLAYERS = 6
PLAYER = 0
BLIND = 50
HERE = path.abspath(path.dirname(__file__))
# FORMAT_STRING = "%Y-%m-%d-%H-%M-%S"
FORMAT_STRING = "%H-%M-%S"
# screenshots_path = path.join(HERE, 'screenshots')

# screen = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screenshot.png'),
#                               region=((1166-5, 964-5, 243+10, 21+10)))


from enum import Enum

class Action(Enum):
    FOLD = 'FOLD'
    CHECK = 'CHECK'
    CALL = 'CALL'
    RAISE_HALF_POT = 'RAISE_HALF_POT'
    RAISE_POT = 'RAISE_POT'
    ALL_IN = 'ALL_IN'

class Street(Enum):
    PREFLOP = 'PREFLOP'
    FLOP = 'FLOP'
    TURN = 'TURN'
    RIVER = 'RIVER'


# clear previous logs
filelist = [f for f in glob(path.join(HERE, 'logs', '*.*'))]
for f in filelist:
    remove(f)

# clear previous screenshots
filelist = [f for f in glob(path.join(HERE, 'data', 'screenshots', '*.*'))]
for f in filelist:
    remove(f)

filelist = [f for f in glob(path.join(HERE, 'data', 'screenshots', 'ocr', '*.*'))]
for f in filelist:
    remove(f)

# LOGGING
import logging
# global logger

# formatter = logging.Formatter('%(asctime)s %(message)s', '%m-%d %H:%M')

#%(name)-6s %(funcName)s


# handler = logging.FileHandler(log_file)
# handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(path.join(HERE, 'logs', 'log.txt'))
handler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(funcName)s %(message)s', '%m-%d %H:%M'))

logger.addHandler(handler)

# def setup_logger(name, log_file, level=logging.DEBUG):
#     """To setup as many loggers as you want"""
#
#     handler = logging.FileHandler(log_file)
#     handler.setFormatter(formatter)
#
#     global logger
#     logger = logging.getLogger(name)
#     logger.setLevel(level)
#     logger.addHandler(handler)
#
    # return logger


class Screen(object):
    def set_work_position(self):

        # game_window = pygetwindow.getActiveWindow()
        # print('game_window.title= ', game_window.title)
        # "No Limit Hold'em - Logged In as'"

        game_window = pygetwindow.getWindowsWithTitle("No Limit Hold'em")[0]
        print(game_window.title)
        try:
            game_window.activate()
        except:
            game_window.minimize()
            game_window.maximize()

        width = int(960 * 1.6)
        hight = int(540 * 1.6)
        left = 1920 - width + 30
        top = 0
        game_window.moveTo(left, top)
        game_window.size = (width, hight)
        time.sleep(0.5)


    def get_button_position(self):
        def get_button_position_from_screen():
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

        button_position = get_button_position_from_screen()
        if button_position is None:
            # lets try again later
            time.sleep(1)
            button_position = get_button_position_from_screen()

        if button_position is None:
            sys.exit('Application did not find buttion position!')
        else:
            return button_position

    def get_bets(self):

        def get_shift(player_id, timestamp):
            # if no chip in picture where we are going to find value of bet then no shift is needed so return 0
            # if chip in picture, so we need to correct region to exclude chip so return shift
            WIDTH_CHIP = 39
            logger.debug(' ')
            logger.debug(f'player_id={player_id} timestamp={timestamp}')
            def locate_chip(player_id, shift):
                DELTA = 0

                regions = {0: (1110 + shift + DELTA, 629, WIDTH_CHIP, 23),
                           1: (805 + shift + DELTA, 568, WIDTH_CHIP, 23),
                           2: (822 + shift + DELTA, 349, WIDTH_CHIP, 23),
                           3: (1239 + shift + DELTA, 249, WIDTH_CHIP, 23),
                           4: (1231 + 270 - shift - WIDTH_CHIP + DELTA, 313, WIDTH_CHIP, 23),
                           5: (1270 + 270 - shift - WIDTH_CHIP + DELTA, 568, WIDTH_CHIP, 23)}

                large_image = pyautogui.screenshot(
                    path.join(HERE, 'data', 'screenshots', f'bet_screen_{player_id}_{timestamp}_{shift}_locate_chip.png'),
                    region=regions[player_id]
                )

                large_image = np.array(large_image)
                large_image = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
                threshold = 80
                _, large_image = cv2.threshold(large_image, threshold, 255, cv2.THRESH_BINARY)
                # cv2.imshow('chip',chip)
                # key = cv2.waitKey(0)
                cv2.imwrite(path.join(HERE, 'data', 'screenshots', f'bet_screen_{player_id}_{timestamp}_{shift}_locate_chip_CV2.png'), large_image)
                # no_chip = pyautogui.locate(path.join(HERE, 'data', 'signs', 'no_chip.png'),
                #                            path.join(HERE, 'data', 'screenshots', f'bet_screen_{player_id}_{timestamp}_locate_no_chip_CV2.png'),
                #                            grayscale=False)

###
                # cv2.imshow('large_image', large_image)
                # key = cv2.waitKey(0)
                small_image = cv2.imread(path.join(HERE, 'data', 'signs', 'no_chip.png'))
                small_image = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)
                # cv2.imshow('small_image', small_image)
                # key = cv2.waitKey(0)

                result = cv2.matchTemplate(small_image,
                                           large_image,
                                           cv2.TM_SQDIFF
                                           )

                min_val, _, min_loc, _ = cv2.minMaxLoc(result)

                if min_val == 0: # we didnt find chip
                    return False
                else:
                    return True

            shift = 0
            while True:
                logger.debug(f'cycle shift={shift}')

                is_chip = locate_chip(player_id, shift)
                logger.debug(f'cycle is_chip={is_chip}')
                # print(f'!!! no_chip = {no_chip}, player_id = {player_id}')
                if not is_chip: # no chip - no shift
                    break
                else:
                    shift += WIDTH_CHIP # width if chip

            logger.debug(f'shift ={shift}')
            logger.debug(' ')
            return shift

        DELTA = 0
        bets = {}

        regions_default = {0: (1110 - DELTA, 629 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA),
                           1: (805 - DELTA, 568 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA),
                           2: (822 - DELTA, 349 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA),
                           3: (1239 - DELTA, 249 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA),
                           4: (1231 - DELTA, 313 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA),
                           5: (1270 - DELTA, 568 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA)}

        for player_id in range(0, 6):

            timestamp = datetime.now().timestamp()
            pyautogui.screenshot(
                path.join(HERE, 'data', 'screenshots', f'bet_screen_{player_id}_{timestamp}.png'),
                region=regions_default[player_id]
            )

            shift = get_shift(player_id, timestamp)
            regions = {0: (1110 + shift - DELTA, 629 - DELTA, 270 + 2 * DELTA - shift, 23 + 2 * DELTA),
                       1: (805 + shift - DELTA, 568 - DELTA, 270 + 2 * DELTA - shift, 23 + 2 * DELTA),
                       2: (822 + shift - DELTA, 349 - DELTA, 270 + 2 * DELTA - shift, 23 + 2 * DELTA), # minus shift made because of phrase "pot:" is caught to picture for bet
                       3: (1239 + shift - DELTA, 249 - DELTA, 270 + 2 * DELTA - shift, 23 + 2 * DELTA),
                       4: (1231 - DELTA, 313 - DELTA, 270 + 2 * DELTA - shift, 23 + 2 * DELTA),
                       5: (1270 - DELTA, 568 - DELTA, 270 + 2 * DELTA- shift, 23 + 2 * DELTA)}

            bet_screen_PIL = pyautogui.screenshot(
                path.join(HERE, 'data', 'screenshots', f'bet_screen_{player_id}_{timestamp}_{shift}.png'),
                region=regions[player_id]
            )
            # convert PIL image to opencv format
            bet_screen_CV = np.array(bet_screen_PIL)
            # cv2.imwrite(f'bet_screen_CV{player_id}.png', bet_screen_CV)
            bet = ocr_digits.get_number(bet_screen_CV, player_id, timestamp, shift)
            if bet is None:
                bet = 0
            bets[player_id] = bet

        return bets

    def get_full_pot(self):

        def get_pot_sign():
            pot = pyautogui.locateOnScreen(path.join(HERE, 'data', 'signs', 'pot.png'),
                                              confidence=0.90,
                                              region=(900, 330, 400, 50),
                                              grayscale=False)
            return pot

        pot = get_pot_sign()
        if pot is None:
            time.sleep(1)
            pot = get_pot_sign()

        if pot is None:
            sys.exit('Application did not find pot sign!')

        pot_screen_PIL = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'temp.png'),
                                              region=(pot[0] + pot[2], pot[1], pot[2] + 300, pot[3]))

        pot_screen_CV = np.array(pot_screen_PIL)
        pot = ocr_digits.get_number(pot_screen_CV)

        return pot

    def __get_card_by_region(self, region):
        card_screen_PIL = pyautogui.screenshot(region=region)
        # convert PIL image to opencv format
        card_screen_CV = cv2.cvtColor(np.array(card_screen_PIL), cv2.COLOR_RGB2BGR)
        return ocr_cards.get_card(card_screen_CV)

    def get_flop_cards(self):
        DELTA = 0
        cards = {}

        regions = {0: (940 - DELTA, 382 - DELTA, 24 + 2 * DELTA, 48 + 2 * DELTA),
                   1: (1036 - DELTA, 382 - DELTA, 24 + 2 * DELTA, 48 + 2 * DELTA),
                   2: (1132 - DELTA, 382 - DELTA, 24 + 2 * DELTA, 48 + 2 * DELTA)}

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
        regions = {0: (1177 - DELTA, 685 - DELTA, 24 + 2 * DELTA, 48 + 2 * DELTA),
                   1: (1087 - DELTA, 686 - DELTA, 24 + 2 * DELTA, 48 + 2 * DELTA)}

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
    def __init__(self):
        self.button_position = None
        self.bets = None
        self.folded_players = None
        # self.actions_after_BB = None
        self.player_cards = None
        self.full_pot = None
        self.flop_cards = None
        self.turn_card = None
        self.river_card = None
        # self.actions_before_BB = None
        self.current_street = None
        # self.first_round_sign = True
        self.previous_full_pot = 0
        self.folded_players_all_before_current_round = []
        self.actions_current_street = {}
        self.actions_previous_street = {}
        self.previous_actions_previous_street = {}
        self.previous_actions_current_street = {}
        self.street_of_previous_round = None

    def debug(self, message):
        current_street = self.get_current_street()
        if current_street is not None:
            logger.debug(f'{current_street.value} {message}')
        else:
            logger.debug(message)

    def start(self):
        pass
        # self.full_pot = 0
        # self.previous_full_pot = 0
        # self.previous_actions = None
        # self.previous_bets = None
        # self.set_first_round_sign(True)

        # clear previous logs
        # filelist = [f for f in glob(path.join(HERE, 'logs', '*.*'))]
        # for f in filelist:
        #     remove(f)
        #
        # clear previous screenshots
        # filelist = [f for f in glob(path.join(HERE, 'data', 'screenshots', '*.*'))]
        # for f in filelist:
        #     remove(f)
        #
        # filelist = [f for f in glob(path.join(HERE, 'data', 'screenshots', 'ocr', '*.*'))]
        # for f in filelist:
        #     remove(f)

    def clear_actions(self):
        self.actions = {}

    def set_first_round_sign(self, first_round_sign):
        self.first_round_sign = first_round_sign

    def get_first_round_sign(self):
        return self.first_round_sign

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

    def set_bet_by_action(self):
        #it works only for player id = 0
        player_id = 0
        button = self.get_button_position()
        full_pot = self.get_full_pot()
        logger.debug(f'full_pot = {full_pot}')
        if self.actions_current_street[player_id] == Action.CALL:
            # since we CALL we need previous player with bet
            folded_players_current_round = self.get_folded_players_current_round()
            active_players = list(set(self.bets.keys()) - set(folded_players_current_round))
            active_players.sort(reverse=True)
            # logger.debug(f'!!! set_bet_by_action active_players = {active_players}')
            self.bets[player_id] = self.bets[active_players[0]]
        elif self.actions_current_street[player_id] == Action.CHECK:
            if self.get_current_street() == Street.PREFLOP:
                if (button + 1) % 6 == player_id:
                    self.bets[player_id] = BLIND
                elif (button + 2) % 6 == player_id:
                    self.bets[player_id] = BLIND * 2
                else:
                    self.bets[player_id] = 0
            else:
                self.bets[player_id] = 0
        elif self.actions_current_street[player_id] == Action.RAISE_HALF_POT:
            self.bets[player_id] = full_pot / 2
        elif self.actions_current_street[player_id] == Action.RAISE_POT:
            self.bets[player_id] = full_pot
        elif self.actions_current_street[player_id] == Action.ALL_IN:
            self.bets[player_id] = BLIND * 2 * 100

        logger.debug(f'self.bets[player_id] = {self.bets[player_id]}')
        # logger.debug(f'!!! set_bet_by_action self.actions[player_id] = {self.actions_current_street[player_id]}')
        # logger.debug(f'!!! set_bet_by_action self.bets[player_id] = {self.bets[player_id]}')

        # full_pot = self.get_full_pot()


    # def update_full_pot(self):
        # if self.full_pot is not None:
        #     self.full_pot = self.full_pot + sum(filter(lambda x: x is not None, self.bets.values()))
        # else:
        #     sys.exit('Pot firstly must be inited with method game.start()')



    def set_full_pot(self):
        screen = Screen()
        full_pot = screen.get_full_pot()
        if full_pot > 0:
            # current_street = self.get_current_street()
            # if current_street == 'FLOP':
            #     full_pot = full_pot - BIG_BLIND - BIG_BLIND/2
            self.full_pot = full_pot
            # print(f'!!! set_full_pot {self.full_pot}')
            # print(f'!!! set_full_pot {full_pot}')
        else:
            sys.exit('set_full_pot full_pot is not more then 0')

    def get_full_pot(self):
        # return self.__increase_pot_by_commission(self.full_pot)
        # logger.debug(f'!!! get_full_pot {self.full_pot}')
        return self.full_pot

    def set_previous_full_pot(self):
        self.previous_full_pot = self.get_full_pot()
        # logger.debug(f'!!! set_previous_full_pot {self.previous_full_pot}')

    def get_previous_full_pot(self):
        # return self.__increase_pot_by_commission(self.previous_full_pot)
        # logger.debug(f'!!! get_previous_full_pot {self.previous_full_pot}')

        return self.previous_full_pot

    def get_pot_for_player_action_old_old(self, player_id):
        button_position = self.get_button_position()
        if player_id is not None:
            player_id_list = [x for x in self.bets.keys() if x > button_position and x < player_id]
            bets = [self.bets[player_id] for player_id in player_id_list]

            # self.get_full_pot() must return full pot without bets of current round
            pot = self.get_previous_full_pot() + sum(filter(lambda x: x is not None, bets))
        else:
            sys.exit('Game.get_pot_for_player_action() player_id is None')
        return pot
    def get_pot_for_player_action_old(self, player_id):
        # button_position = self.get_button_position()
        if player_id is not None:
            player_id_list = [x for x in self.get_bets().keys() if x >=0 and x < player_id]
            bets = [self.get_bets()[player_id] for player_id in player_id_list]

            # self.get_full_pot() must return full pot without bets of current round
            pot = self.get_previous_full_pot() + sum(filter(lambda x: x is not None, bets))
        else:
            sys.exit('Game.get_pot_for_player_action() player_id is None')
        return pot

    def get_pot_for_player_action(self, player_id):
        if player_id is not None:
            player_id_list = [x for x in self.get_bets().keys() if x < 6 and x >= player_id]
            bets = [self.get_bets()[player_id] for player_id in player_id_list]

            # self.get_full_pot() must return full pot without bets of current round
            pot = self.get_full_pot() - sum(filter(lambda x: x is not None, bets))
        else:
            sys.exit('Game.get_pot_for_player_action() player_id is None')
        return pot



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
        screen = Screen()
        while True:
            no_bet_button = screen.get_no_bet_button()
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

    def set_streets(self):
        # logger.debug(f'self.street_of_previous_round = {self.street_of_previous_round}')
        # logger.debug(f'self.current_street = {self.current_street}')

        self.street_of_previous_round = self.current_street


        if self.river_card is not None:
            self.current_street = Street.RIVER
        else:
            if self.turn_card is not None:
                self.current_street = Street.TURN
            else:
                if len(list(filter(lambda x: x is not None, self.flop_cards.values()))) > 0:
                    self.current_street = Street.FLOP
                else:
                    self.current_street = Street.PREFLOP

        # logger.debug(f'self.street_of_previous_round = {self.street_of_previous_round}')
        # logger.debug(f'self.current_street = {self.current_street}')


    def get_current_street(self):
        return self.current_street

    def get_street_of_previous_round(self):
        return self.street_of_previous_round

    def get_previous_street(self):
        current_street = self.get_current_street()
        # previous_street = None
        if current_street == Street.PREFLOP:
            previous_street = None
        elif current_street == Street.FLOP:
            previous_street = Street.PREFLOP
        elif current_street == Street.TURN:
            previous_street == Street.FLOP
        elif current_street == Street.RIVER:
            previous_street == Street.TURN

        return previous_street

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

    def set_folded_players_all(self):
        screen = Screen()
        self.folded_players_all = screen.get_folded_players()

    def get_folded_players_all(self):
        return self.folded_players_all

    def set_folded_players_all_before_current_round(self):
        self.folded_players_all_before_current_round = list(set(self.folded_players_all_before_current_round + self.folded_players_all))

    def get_folded_players_all_before_current_round(self):
        return self.folded_players_all_before_current_round

    def get_folded_players_current_round(self):
        # print('!!! self.get_folded_players_all() = ',self.get_folded_players_all())
        # print('!!! self.get_folded_players_all_before_current_round() = ', self.get_folded_players_all_before_current_round())

        return list(set(self.get_folded_players_all()) - set(self.get_folded_players_all_before_current_round()))

    def set_actions_all_players(self):

        # logging.debug('start set_actions_after_BB')

        button_position = self.get_button_position()
        bets = self.get_bets()
        # previous_full_pot = self.get_previous_full_pot()  # pot at the previous moment when we asked for pressing button with action
        # folded_players = self.get_folded_players()

        folded_players_current_round = self.get_folded_players_current_round()
        folded_players_all_before_current_round = self.get_folded_players_all_before_current_round()

        # self.actions = {} # TODO

        previous_bet = self.get_previous_bets()[0]
        # if previous_bet is None:
        #     previous_bet = 0
        # is_previous_allin = False
        logger.debug(f'button_position = {button_position}')
        logger.debug(f'bets = {bets}')
        # logger.debug(f'set_actions_all_players full pot of previous rounds = ', full_pot_previous_rounds)
        logger.debug(f'folded_players_current_round = {folded_players_current_round}')
        logger.debug(f'folded_players_all_before_current_round = {folded_players_all_before_current_round}')

        self.actions_current_street = {}

        for player_id in range(1, 6):
            logger.debug(f'CYCLE player_id = {player_id}')
            # logger.debug(f'set_actions_all_players CYCLE bets[{player_id}] = {bets[player_id]}')
            logger.debug(f'CYCLE previous_bet = {previous_bet}')
            pot = self.get_pot_for_player_action(player_id)
            logger.debug(f'CYCLE pot = {pot}')
            if player_id in folded_players_all_before_current_round:
                logger.debug(f'CYCLE player {player_id} NO DECISION because he folded before')
                continue
            elif player_id in folded_players_current_round:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.FOLD)
            elif bets[player_id] == 0:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.CHECK)
            elif self.actions_current_street is not None and Action.ALL_IN in [x['action'] for x in
                                                                                   self.actions_current_street.values()]:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.CALL)
            elif bets[player_id] == previous_bet:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.CALL)
            elif bets[player_id] > previous_bet and bets[player_id] <= (3 * pot / 4):
                self.actions_current_street[player_id] = self.__make_action_dict(Action.RAISE_HALF_POT)
                previous_bet = bets[player_id]
            elif bets[player_id] > (3 * pot / 4) and bets[player_id] <= pot + (100 * 2 * BLIND - pot) / 2:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.RAISE_POT)
                previous_bet = bets[player_id]
            elif bets[player_id] > pot + (100 * 2 * BLIND - pot) / 2:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.ALL_IN)
                previous_bet = bets[player_id]
                # is_previous_allin = True
            else:
                sys.exit('Error. Application can not define action before player!')

            logger.debug(f'actions_current_street = {self.actions_current_street}')
        # start_position('finish set_actions_after_BB')
        # print(' ')
        pass

    def set_action_current_street(self, AI_action):
        # made only for player_id = 0
        if str(AI_action) == 'Action.FOLD':
            action = Action.FOLD
        elif str(AI_action) == 'Action.CHECK':
            action = Action.CHECK
        elif str(AI_action) == 'Action.CALL':
            action = Action.CALL
        elif str(AI_action) == 'Action.RAISE_HALF_POT':
            action = Action.RAISE_HALF_POT
        elif str(AI_action) == 'Action.RAISE_POT':
            action = Action.RAISE_POT
        elif str(AI_action) == 'Action.ALL_IN':
            action = Action.ALL_IN

        self.actions_current_street[PLAYER] = self.__make_action_dict(action)

    def get_actions_current_street(self):
        return self.actions_current_street

    def set_previous_actions_current_street(self):
        self.previous_actions_current_street = self.actions_current_street

    def get_previous_actions_current_street(self):
        return self.previous_actions_current_street

    def set_previous_actions_previous_street(self):
        self.previous_actions_previous_street = self.actions_previous_street

    def get_previous_actions_previous_street(self):
        return self.previous_actions_previous_street

    def get_actions_previous_street(self):
        return self.actions_previous_street

    def set_previous_bets(self):
        self.previous_bets = self.bets

    def get_previous_bets(self):
        return self.previous_bets

    def __make_action_dict(self, action, street = None):
        return {'action': action, 'street': self.get_current_street() if street is None else street, 'state': 'NOT_READ'}

    # def __update_state_action_dict(self, new_state, sign_current_street=True):
    #     self.actions_current_street
    #     return {'action': action, 'street': self.get_current_street() if street is None else street, 'state': 'NOT_READ'}


    def set_actions_first_round(self):
        # logger.debug(f'start set_actions_after_BB')
        button_position = self.get_button_position()
        bets = self.get_bets()
        # current_street = self.get_current_street()
        # previous_full_pot = self.get_previous_full_pot()  # pot at the previous moment when we asked for pressing button with action
        # folded_players = self.get_folded_players()

        folded_players_current_round = self.get_folded_players_current_round()

        # self.actions = {}

        previous_bet = 2 * BLIND
        # is_previous_allin = False

        logger.debug(f'button_position = {button_position}')
        logger.debug(f'bets = {bets}')
        # logger.debug(f'set_actions_first_round previous_full_pot = ', previous_full_pot)
        logger.debug(f'folded_players_current_round = {folded_players_current_round}')

        start_position = (button_position + 3) % 6
        logger.debug(f'start_position = {start_position}')

        self.actions_current_street = {}

        if start_position == 0:
            return

        for player_id in range(start_position, 6):
            logger.debug(f'CYCLE player_id = {player_id}')
            logger.debug(f'CYCLE previous_bet = {previous_bet}')
            pot = self.get_pot_for_player_action(player_id)

            logger.debug(f'CYCLE pot = {pot}')
            if player_id in folded_players_current_round:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.FOLD)
            elif bets[player_id] == 0:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.CHECK)
            elif self.actions_current_street is not None and Action.ALL_IN in [x['action'] for x in self.actions_current_street.values()]:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.CALL)
            elif bets[player_id] == previous_bet:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.CALL)
            elif bets[player_id] > previous_bet and bets[player_id] <= (3 * pot / 4):
                self.actions_current_street[player_id] = self.__make_action_dict(Action.RAISE_HALF_POT)
                previous_bet = bets[player_id]
            elif bets[player_id] > (3 * pot / 4) and bets[player_id] <= pot + (100 * 2 * BLIND - pot) / 2:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.RAISE_POT)
                previous_bet = bets[player_id]
            elif bets[player_id] > pot + (100 * 2 * BLIND - pot) / 2:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.ALL_IN)
                previous_bet = bets[player_id]
                # is_previous_allin = True
            else:
                sys.exit('Error. Application can not define action for first round!')

            logger.debug(f'self.actions_current_street = {self.actions_current_street}')
        pass

    def __get_sum_bets(self, bets):
        return sum(filter(lambda x: x is not None, bets.values()))

    def __increase_pot_by_commission(self, decreased_pot):
        commission_rate = 0.055
        pot = decreased_pot/(1 - commission_rate)
        return pot

    def __get_commission(self, full_pot, current_street_pot):
        commission_rate = 0.055
        # commission is got at the begining of the street
        pot_previous_streets = full_pot - current_street_pot
        return pot_previous_streets * commission_rate / (1 - commission_rate)

    def set_actions_after_changing_street(self):
        current_street = self.get_current_street()
        previous_street = self.get_previous_street()
        button_position = self.get_button_position()
        bets = self.get_bets() # bets from current screen
        # previous_full_pot = self.get_previous_full_pot() # pot at the previous moment when we asked for pressing button with action

        #TODO temp check
        # if not previous_full_pot > 0:
        #     sys.exit('calculate_actions_after_changing_street previous_full_pot not more then 0')

        full_pot = self.get_full_pot() # it is where we now see on screen: "pot: 123456789" when we asked for pressing button with action

        folded_players_current_round = self.get_folded_players_current_round()
        folded_players_all_before_current_round = self.get_folded_players_all_before_current_round()
        folded_players_all_before_current_street = [x for x in folded_players_all_before_current_round]

        # pot_previous_street_current_screen = full_pot - current_street_pot - previous_full_pot + pot_commission_value# we dont see on screen bets of previous street that made after our previous action
        # bet_previous_street_current_screen = self.get_previous_bets()[0]

        # we see folded player after button, he could fold this round or previous
        # we need to decide in which round he folded
        logger.debug(f'current_street = {current_street}')
        logger.debug(f'previous_street = {previous_street}')
        logger.debug(f'button_position = {button_position}')
        logger.debug(f'folded_players_current_round = {folded_players_current_round}')
        logger.debug(f'folded_players_all_before_current_round = {folded_players_all_before_current_round}')
        logger.debug(f'bets = {bets}')
        logger.debug(f'previous_bets = {self.get_previous_bets()}')

        # logger.debug(f'set_actions_after_changing_street previous_full_pot = {previous_full_pot}')
        logger.debug(f'full_pot = {full_pot}')
        # logger.debug(f'set_actions_after_changing_street current_street_pot = {current_street_pot}')
        # logger.debug(f'set_actions_after_changing_street pot_previous_street_current_screen = {pot_previous_street_current_screen}')
        # logger.debug(f'set_actions_after_changing_street bet_previous_street_current_screen = {bet_previous_street_current_screen}')
        # logger.debug(f'folded_players_all_before_current_round = {folded_players_all_before_current_round}')
        # logger.debug(f'set_actions_after_changing_street pot_commission_value = {pot_commission_value}')
        # logger.debug(f'calculate_actions_after_changing_street folded_players = ', num_folded_players_previous_round_after_player)

        # PREVIOUS STREET of CURRENT SCREEN
        # if someone raised after us then we wouldnt get into this function
        # and we will get into set_actions_all_players

        # if someone who was last who raised before us then street will finish only after actions all players before last raised
        logger.debug(f'PREVIOUS STREET')
        # player which was the last who raised is the end of previous round
        previous_actions_current_street = self.get_previous_actions_current_street()
        # previous_actions_previous_street = self.get_previous_actions_previous_street()
        logger.debug(f'previous_actions_current_street = {previous_actions_current_street}')
        # logger.debug(f'set_actions_after_changing_street previous_actions_previous_street = {previous_actions_previous_street}')
        end_position = None

        previous_actions_current_street[6] = previous_actions_current_street[0] # player with id 0 must be the first in cycle below
        del previous_actions_current_street[0]

        logger.debug(f'0 to 6 previous_actions_current_street = {previous_actions_current_street}')

        player_id_list = list(previous_actions_current_street.keys())
        player_id_list.sort(reverse=True)
        for player_id in player_id_list:
            if previous_actions_current_street[player_id]['action'] in [Action.RAISE_POT, Action.RAISE_HALF_POT,
                                                                            Action.ALL_IN]:
                # print('!!! previous_actions_current_street[player_id] = ',
            #       previous_actions_current_street[player_id])

            # print('!!! previous_actions_current_street[player_id][action] = ', previous_actions_current_street[player_id]['action'])
            # if previous_actions_current_street[player_id]['action'] == Action.RAISE_POT or \
            #         previous_actions_current_street[player_id]['action'] == Action.RAISE_HALF_POT or \
            #         previous_actions_current_street[player_id]['action'] == Action.ALL_IN:
                end_position = player_id - 1
                break
        if end_position is None: # None of players raised
            if current_street == Street.FLOP:
                end_position = button_position + 2 # end of PREFLOP
                end_position = end_position % 6
            else:
                end_position = button_position

        if end_position == 0:
            end_position = 6

        logger.debug(f'end_position = {end_position}')
        self.actions_previous_street = {}
        for player_id in range(1, end_position + 1):
            logger.debug(f'CYCLE player_id = {player_id}')
            # logger.debug(f'set_actions_after_changing_street CYCLE num_folded_players_previous_street_current_screen = {num_folded_players_previous_street_current_screen}')
            logger.debug(f'CYCLE folded_players_all_before_current_street = {folded_players_all_before_current_street}')
            if player_id in folded_players_all_before_current_round:
                logger.debug(f'CYCLE player {player_id} NO DECISION because he folded before')
                continue
            elif player_id in folded_players_current_round:
                folded_players_all_before_current_street.append(player_id)
                self.actions_previous_street[player_id] = self.__make_action_dict(Action.FOLD, previous_street)
            # below FOLD is defenitly in previous street
            # elif player_id in folded_players_current_round and player_id <= button_position:
            #     num_folded_players_previous_street_current_screen -= 1
            #     folded_players_all_before_current_street.append(player_id)
            #     self.previous_actions[player_id] = 'FOLD'
            # below FOLD is that can be made both in previous and current street
            # we have to decide in which street FOLD is made
            # TODO if after button and before end_position two players were folded
            #  then we cant define which of them folded in previous street and which - in current
            # elif player_id in folded_players_current_round and player_id > button_position and player_id < end_position and num_folded_players_previous_street_current_screen > 0:
            #     num_folded_players_previous_street_current_screen -= 1
            #     folded_players_all_before_current_street.append(player_id)
            #     self.previous_actions[player_id] = 'FOLD'
            elif self.get_previous_bets()[0] == 0: # this is bet of us (player № 0). If our bet = 0 and street has changed then all players after us made CHECK
                self.actions_previous_street[player_id] = self.__make_action_dict(Action.CHECK, previous_street)
            # elif not pot_previous_street_current_screen > 0:
            #     self.previous_actions[player_id] = 'CHECK'
            elif current_street == Street.FLOP and player_id == (button_position + 2) % 6 and end_position == (button_position + 2) % 6:  # player on big blind on preflop
                self.actions_previous_street[player_id] = self.__make_action_dict(Action.CHECK, previous_street)
            else:
                self.actions_previous_street[player_id] = self.__make_action_dict(Action.CALL, previous_street)

            logger.debug(f'CYCLE self.actions_previous_street = {self.actions_previous_street}')

        # CURRENT ROUND
        logger.debug(f'CURRENT STREET')
        start_position = (button_position + 1) % 6
        logger.debug(f'start_position = {start_position}')
        if start_position == 0: # we are the first player to make action in current round, so no players made action
            return

        self.actions_current_street = {}
        previous_bet = 0
        for player_id in range(start_position, 6):
            logger.debug(f'CYCLE player_id = {player_id}')
            # logger.debug(f'calculate_actions_after_changing_street previous_bet = ', previous_bet)
            pot = self.get_pot_for_player_action(player_id)
            logger.debug(f'CYCLE pot = {pot}')
            logger.debug(f'CYCLE previous_bet = {previous_bet}')
            if player_id in folded_players_all_before_current_street:
                logger.debug(f'CYCLE player {player_id} NO DECISION because he folded before')
                continue
            elif player_id in folded_players_current_round:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.FOLD)
            elif bets[player_id] == 0:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.CHECK)
            elif self.actions_current_street is not None and Action.ALL_IN in [x['action'] for x in self.actions_current_street.values()]:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.CALL)
            elif bets[player_id] == previous_bet:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.CALL)
            elif bets[player_id] > previous_bet and bets[player_id] <= (3 * pot / 4):
                self.actions_current_street[player_id] = self.__make_action_dict(Action.RAISE_HALF_POT)
                previous_bet = bets[player_id]
            elif bets[player_id] > (3 * pot / 4) and bets[player_id] <= pot + (100 * 2 * BLIND - pot) / 2:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.RAISE_POT)
                previous_bet = bets[player_id]
            elif bets[player_id] > pot + (100 * 2 * BLIND - pot) / 2:
                self.actions_current_street[player_id] = self.__make_action_dict(Action.ALL_IN)
                previous_bet = bets[player_id]
                # is_previous_allin = True
            else:
                sys.exit('Error. Application can not define action for first round!')

            logger.debug(f'CYCLE self.actions_current_street = {self.actions_current_street}')

    def init_game(self):
        screen = Screen()
        screen.set_work_position()

        time = datetime.now().strftime(FORMAT_STRING)
        setup_logger('PREFLOP', path.join(HERE, 'logs', f'{PREFLOP}_{time}.log'))

    def init_game_old(self):

        self.wait_for_bet_button()  # waiting for other players finishes placing their bets if necessary

        print('REAL GAME IS STARTED!')
        self.start()
        current_street = Street.PREFLOP
        n_round = 1
        # set up logger
        setup_logger(current_street.value, path.join(HERE, 'logs', f'{current_street.value}.log'))

        # read game data from screen
        self.set_community_cards()
        self.set_current_street()
        self.set_player_cards()
        self.set_button_position()
        self.set_bets()
        self.set_folded_players_all()
        self.set_full_pot()

        pyautogui.screenshot(path.join(HERE, 'logs', f'{current_street.value}_{n_round}.png'))

        print(current_street.value)
        print('round = ', n_round)

        self.set_actions_first_round()

    def process_screen(self):
        logger.debug('\n')

        time = datetime.now().strftime(FORMAT_STRING)
        logger.debug(f'############# started time = {time} #############')
        self.wait_for_bet_button()

        self.set_community_cards()
        self.set_streets()

        current_street = self.get_current_street()
        logger.debug(f'############# {current_street.value} #############')
        street_of_previous_round = self.get_street_of_previous_round()
        # logger.debug(f'street_of_previous_round {self.street_of_previous_round}')
        # logger.debug(f'street_of_previous_round {street_of_previous_round}')
        logger.debug(f'street_of_previous_round {street_of_previous_round.value if street_of_previous_round is not None else None}')

        # print('!!! 2 game.full_pot = ', game.full_pot)
        if current_street == Street.PREFLOP and street_of_previous_round != Street.PREFLOP:
            logger.debug('GAME IS STARTED!')
            print('GAME IS STARTED!')
            self.start()

        # set up logger
        # print('!!! current street = ', current_street)

        # if current_street != street_of_previous_round:
        #     setup_logger(current_street.value, path.join(HERE, 'logs', f'{current_street.value}_{time}.log'))
        # read game data from screen

        self.set_player_cards()
        self.set_button_position()
        self.set_bets()
        self.set_folded_players_all()
        self.set_full_pot()


        pyautogui.screenshot(path.join(path.dirname(HERE), 'logs', f'{current_street.value}_{time}.png'))

        # logger.debug(f'current street {current_street.value}')
        # logger.debug(f'previous street {street_of_previous_round.value}')

        print(current_street.value)
        # print('round = ', n_round)
        # print('!!! 3 game.full_pot = ', game.full_pot)
        # street_of_previous_round = self.get_street_of_previous_round()

        if current_street == Street.PREFLOP and street_of_previous_round is None:
            self.set_actions_first_round()
        else:
            if current_street != street_of_previous_round:
                self.set_actions_after_changing_street()
            else:
                self.set_actions_all_players()

    def postprocess_screen(self, AI_action):
        logger.debug('\n')
        # button = game.get_button_position()
        # current_street = self.get_current_street()

        # set action and bet for us e.g player with id = 0
        logger.debug('set action and bet for us e.g for player with id = 0')
        self.set_action_current_street(AI_action)
        self.set_bet_by_action()
        logger.debug(f'actions_current_street = {self.get_actions_current_street()}')
        logger.debug(f'bets = {self.get_bets()}')

        # save data of this round for using it in next round
        self.set_previous_actions_current_street()
        self.set_previous_actions_previous_street()
        self.set_previous_bets()
        # self.set_street_of_previous_round()
        # print('!!! 5 game.full_pot = ', game.full_pot)
        self.set_previous_full_pot()
        # previous_street = current_street

        self.set_folded_players_all_before_current_round()

    def get_action_for_AI(self, player_id):

        def get_action_from_attributes(player_id):
            action_for_AI = None
            actions_previous_street = self.get_actions_previous_street()
            if player_id in actions_previous_street:
                if actions_previous_street[player_id]['state'] == 'NOT_READ':
                    action_for_AI = actions_previous_street[player_id]
                    self.actions_previous_street[player_id]['state'] = 'READ'
                    return action_for_AI

            actions_current_street = self.get_actions_current_street()
            if player_id in actions_current_street:
                if actions_current_street[player_id]['state'] == 'NOT_READ':
                    action_for_AI = actions_current_street[player_id]
                    self.actions_current_street[player_id]['state'] = 'READ'

            return action_for_AI

        folded_players_all = self.get_folded_players_all()

        logger.debug(f'player_id = {player_id}')
        logger.debug(f'folded_players_all = {folded_players_all}')
        logger.debug(f'self.get_actions_previous_street = {self.get_actions_previous_street}')
        logger.debug(f'self.get_actions_current_street = {self.get_actions_current_street}')

        if player_id in folded_players_all:
            return Action.FOLD

        action_for_AI = get_action_from_attributes(player_id)
        if action_for_AI is None:
            self.process_screen()
            action_for_AI = get_action_from_attributes(player_id)
            if action_for_AI is None:
                sys.exit(f'reader.get_action_for_AI() player_id = {player_id} action_for_AI is None!')

        logger.debug(f'player_id = {player_id}, action_for_AI = {action_for_AI}')

        return action_for_AI['action']


if __name__ == '__main__':

    # ss = pygetwindow.getWindowsWithTitle("No Limit Hold'em")[0]
    # print('ss = ', ss)
    # ss.activate()
    # assert 1==3

    time.sleep(5)

    screen = Screen()
    screen.set_work_position()

    game = Game()

    previous_street = None
    n_round = None

    # game.set_bets()

    while True:
        if game.wait_for_bet_button(): # waiting for other players finishes placing their bets if necessary

            game.set_community_cards()
            game.set_streets()

            current_street = game.get_current_street()
            # print('!!! 2 game.full_pot = ', game.full_pot)
            if current_street == Street.PREFLOP and previous_street != Street.PREFLOP:
                print('GAME IS STARTED!')
                game.start()

            # set up logger
            # print('!!! current street = ', current_street)

            if current_street != previous_street:
                setup_logger(current_street.value, path.join(HERE, 'logs', f'{current_street.value}.log'))
                n_round = 1
            else:
                n_round += 1

            # read game data from screen

            game.set_player_cards()
            game.set_button_position()
            game.set_bets()
            game.set_folded_players_all()
            game.set_full_pot()
            # print('!!! 1 game.full_pot = ',game.full_pot)

            # game.clear_actions()
            # game.set_previous_actions()
            # game.set_current_actions()



            screen = pyautogui.screenshot(path.join(HERE, 'logs', f'{current_street.value}_{n_round}.png'))

            logger.debug(f'current street {current_street.value}')
            logger.debug(f'previous street {previous_street}')
            logger.debug(f'round = {n_round}')
            print(current_street)
            print('round = ', n_round)
            # print('!!! 3 game.full_pot = ', game.full_pot)

            if current_street == Street.PREFLOP and previous_street != Street.PREFLOP:
                game.set_actions_first_round()
            else:
                if current_street != previous_street:
                    game.set_actions_after_changing_street()
                else:
                    game.set_actions_all_players()
            # print('!!! 4 game.full_pot = ', game.full_pot)
            # we gave data to model
            # model gave us back answer
            # temp answer is CALL
            button = game.get_button_position()
            if current_street == Street.PREFLOP and n_round == 1 and (button + 2) % 6 == 0:
                game.set_action_current_street(PLAYER, Action.CHECK)
            elif current_street != Street.PREFLOP and (button + 1) % 6 == 0:
                game.set_action_current_street(PLAYER, Action.CHECK)
            else:
                game.set_action_current_street(PLAYER, Action.CALL)

            game.set_bet_by_action()

            # save data of this round for using it in next round
            game.set_previous_actions_current_street()
            game.set_previous_actions_previous_street()
            game.set_previous_bets()
            # print('!!! 5 game.full_pot = ', game.full_pot)
            game.set_previous_full_pot()
            previous_street = current_street

            game.set_folded_players_all_before_current_round()
            # game.update_full_pot()
            if game.wait_for_player_bet():
                pass

            logger.debug(' ')


# clear attributres like actions
