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

PLAYER = 0
BIG_BLIND = 100
HERE = path.abspath(path.dirname(__file__))
# screenshots_path = path.join(HERE, 'screenshots')

# screen = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screenshot.png'),
#                               region=((1166-5, 964-5, 243+10, 21+10)))



# LOGGING
import logging
global logger

formatter = logging.Formatter('%(asctime)s %(name)-6s %(message)s', '%m-%d %H:%M')
def setup_logger(name, log_file, level=logging.DEBUG):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    global logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    # return logger

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
        DELTA = 0
        bets = {}
        regions = {0: (1110 - DELTA, 629 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA),
                   1: (805 - DELTA, 568 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA),
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

    def get_full_pot(self):
        pot = pyautogui.locateOnScreen(path.join(HERE, 'data', 'signs', 'pot.png'),
                                          confidence=0.95,
                                          region=(900, 330, 400, 50),
                                          grayscale=False)
        # print('pot = ', pot)

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
    def __init__(self):
        self.button_position = None
        self.bets = None
        self.folded_players = None
        self.decisions_after_BB = None
        self.player_cards = None
        self.full_pot = None
        self.flop_cards = None
        self.turn_card = None
        self.river_card = None
        self.decisions_before_BB = None
        self.current_street = None
        self.first_round_sign = True

    def start(self):
        self.full_pot = 0
        self.previous_decisions = None
        self.previous_bets = None
        self.set_first_round_sign(True)

        # clear previous logs
        filelist = [f for f in glob(path.join(HERE, 'logs', '*.*'))]
        for f in filelist:
            remove(f)

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

    def set_bet_by_decision(self, player_id):
        if self.decisions[player_id] == 'CALL':
            if player_id == 0:
                self.bets[player_id] = self.bets[5]
            else:
                self.bets[player_id] = self.bets[player_id-1]
        # full_pot = self.get_full_pot()


    def update_full_pot(self):
        if self.full_pot is not None:
            self.full_pot = self.full_pot + sum(filter(lambda x: x is not None, self.bets.values()))
        else:
            sys.exit('Pot firstly must be inited with method game.start()')

    def __increase_pot_by_commission(self, decreased_pot):
        commission_rate = 0.055
        pot = decreased_pot/(1 - commission_rate)
        return pot

    def set_full_pot(self):
        screen = Screen()
        self.full_pot = screen.get_full_pot()

    def get_full_pot(self):
        return self.__increase_pot_by_commission(self.full_pot)

    def set_previous_full_pot(self):
        self.previous_full_pot = self.full_pot

    def get_previous_full_pot(self):
        return self.__increase_pot_by_commission(self.previous_full_pot)

    def get_pot_for_player_decision(self, player_id):
        button_position = self.get_button_position()
        if player_id is not None:
            player_id_list = [x for x in self.bets.keys() if x > button_position and x < player_id]
            bets = [self.bets[player_id] for player_id in player_id_list]

            # self.get_full_pot() must return full pot without bets of current round
            pot = self.get_full_pot() + sum(filter(lambda x: x is not None, bets))
        else:
            sys.exit('Game.get_pot_for_player_decision() player_id is None')
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

    def set_decisions_before_player(self):
        # logging.debug('start set_decisions_after_BB')

        button_position = self.get_button_position()
        bets = self.get_bets()
        full_pot_previous_rounds = self.get_full_pot()
        folded_players = self.get_folded_players()
        self.decisions_before_player = {}

        previous_bet = BIG_BLIND
        # is_previous_allin = False

        logging.debug('set_decisions_before_player button_position = ',button_position)
        logging.debug('set_decisions_before_player bets = ', bets)
        logging.debug('set_decisions_before_player full pot of previous rounds = ', full_pot_previous_rounds)
        logging.debug('set_decisions_before_player folded_players = ', folded_players)

        # we need decisions only after BB position and before ours
        # this decisions we pass to AI
        start_position = (button_position+3)%6
        logging.debug('set_decisions_after_BB start_position = ', start_position)
        if start_position == 0:
            return

        for player_id in range(start_position, 6): # if button position+3 is more then 6 then we have to make it less then 6
            logging.debug('set_decisions_before_player player_id = ', player_id)
            logging.debug('set_decisions_before_player previous_bet = ', previous_bet)
            pot = self.get_pot_for_player_decision(player_id)
            logging.debug('set_decisions_before_player pot = ',pot)
            if player_id in folded_players:
                self.decisions_before_player[player_id] = 'FOLD'
            elif bets[player_id] is None:
                self.decisions_before_player[player_id] = 'CHECK'
            elif 'ALL_IN' in list(self.decisions_after_BB.values()):
            # elif is_previous_allin  == True:
                self.decisions_before_player[player_id] = 'CALL'
            elif bets[player_id] == previous_bet:
                self.decisions_before_player[player_id] = 'CALL'
            elif bets[player_id] > previous_bet and bets[player_id] <= (3 * pot / 4):
                self.decisions_before_player[player_id] = 'RAISE_HALF_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > (3 * pot / 4) and bets[player_id] <= pot + (100 * BIG_BLIND - pot) / 2:
                self.decisions_before_player[player_id] = 'RAISE_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > pot + (100 * BIG_BLIND - pot) / 2:
                self.decisions_before_player[player_id] = 'ALL_IN'
                previous_bet = bets[player_id]
                # is_previous_allin = True
            else:
                sys.exit('Error. Application can not define decision before player!')

            logging.debug('set_decisions_before_player self.decisions_before_player = ',self.decisions_before_player)
        # start_position('finish set_decisions_after_BB')
        # print(' ')
        pass

    def get_decisions_before_player(self):
        return self.decisions_before_player

    def set_decisions_after_player(self):

        button_position = self.get_button_position()
        bets = self.get_bets()
        full_pot_previous_rounds = self.get_full_pot()
        folded_players = self.get_folded_players()

        self.decisions_after_player = self.decisions_before_player

        previous_bet = self.bets[0] # get player's (our) bet
        is_previous_allin = False

        logging.debug('set_decisions_after_player button_position = ',button_position)
        logging.debug('set_decisions_after_player bets = ', bets)
        logging.debug('set_decisions_after_player full pot of previous rounds = ', full_pot_previous_rounds)
        logging.debug('set_decisions_after_player folded_players = ', folded_players)

        start_position = (button_position+3)%6
        logging.debug('set_decisions_after_player start_position = ', start_position)
        if start_position == 0:
            return

        for player_id in range(1, button_position+2):

            logging.debug('set_decisions_after_player player_id = ', player_id)
            logging.debug('set_decisions_after_player previous_bet = ', previous_bet)
            pot = self.get_pot_for_player_decision(player_id)
            logging.debug('set_decisions_after_player pot = ', pot)

            if player_id in folded_players:
                self.decisions_after_player[player_id] = 'FOLD'
            elif 'ALL_IN' in list(self.decisions_before_BB.values()):
                self.decisions_after_player[player_id] = 'CALL'
            elif player_id == button_position + 2 and bets[player_id] == BIG_BLIND: # check on BB position
                self.decisions_after_player[player_id] = 'CHECK'
            # elif is_previous_allin  == True:
            #     self.current_decisions[player_id] = 'CALL'
            elif bets[player_id] == previous_bet:
                self.decisions_after_player[player_id] = 'CALL'
            elif bets[player_id] > previous_bet and bets[player_id] <= (3 * pot / 4):
                self.decisions_after_player[player_id] = 'RAISE_HALF_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > (3 * pot / 4) and bets[player_id] <= pot + (100 * BIG_BLIND - pot) / 2:
                self.decisions_after_player[player_id] = 'RAISE_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > pot + 3*(100 * BIG_BLIND - pot) / 4:
                self.decisions_after_player[player_id] = 'ALL_IN'
                previous_bet = bets[player_id]
                is_previous_allin = True
            else:
                sys.exit('Error. Application can not define decisions after player!')

            logging.debug('set_decisions_after_player self.decisions_after_player = ', self.decisions_after_player)

    def get_decisions_after_player(self):
        return self.decisions_after_player

    def set_decisions_all_players(self):
        # logging.debug('start set_decisions_after_BB')

        button_position = self.get_button_position()
        bets = self.get_bets()
        full_pot_previous_rounds = self.get_full_pot()
        folded_players = self.get_folded_players()
        self.decisions = {} # TODO

        previous_bet = bets[0]
        # is_previous_allin = False

        logging.debug('set_decisions_all_players button_position = ',button_position)
        logging.debug('set_decisions_all_players bets = ', bets)
        logging.debug('set_decisions_all_players full pot of previous rounds = ', full_pot_previous_rounds)
        logging.debug('set_decisions_all_players folded_players = ', folded_players)

        # we need decisions only after BB position and before ours
        # this decisions we pass to AI

        for player_id in range(1, 6):
            logging.debug('set_decisions_all_players player_id = ', player_id)
            logging.debug('set_decisions_all_players previous_bet = ', previous_bet)
            pot = self.get_pot_for_player_decision(player_id)
            logging.debug('set_decisions_before_player pot = ',pot)
            if player_id in folded_players:
                self.decisions[player_id] = 'FOLD'
            elif bets[player_id] is None:
                self.decisions[player_id] = 'CHECK'
            elif 'ALL_IN' in list(self.decisions_after_BB.values()):
            # elif is_previous_allin  == True:
                self.decisions[player_id] = 'CALL'
            elif bets[player_id] == previous_bet:
                self.decisions[player_id] = 'CALL'
            elif bets[player_id] > previous_bet and bets[player_id] <= (3 * pot / 4):
                self.decisions[player_id] = 'RAISE_HALF_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > (3 * pot / 4) and bets[player_id] <= pot + (100 * BIG_BLIND - pot) / 2:
                self.decisions[player_id] = 'RAISE_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > pot + (100 * BIG_BLIND - pot) / 2:
                self.decisions[player_id] = 'ALL_IN'
                previous_bet = bets[player_id]
                # is_previous_allin = True
            else:
                sys.exit('Error. Application can not define decision before player!')

            logging.debug('set_decisions_before_player self.set_decisions_all_players = ',self.decisions)
        # start_position('finish set_decisions_after_BB')
        # print(' ')
        pass

    def set_decision(self, player_id, decision):
        self.decisions[player_id] = decision

    def get_decisions(self):
        return self.decisions

    def set_previous_decisions(self):
        self.previous_decisions = self.decisions

    def get_previous_decisions(self):
        return self.previous_decisions

    def set_previous_bets(self):
        self.previous_bets = self.bets

    def get_previous_bets(self):
        return self.previous_bets

    def set_decisions_first_round(self):
        # logging.debug('start set_decisions_after_BB')

        button_position = self.get_button_position()
        bets = self.get_bets()
        full_pot_previous_rounds = self.get_full_pot()
        folded_players = self.get_folded_players()
        self.decisions = {}

        previous_bet = BIG_BLIND
        # is_previous_allin = False

        logging.debug('set_decisions_first_round button_position = ',button_position)
        logging.debug('set_decisions_first_round bets = ', bets)
        logging.debug('set_decisions_first_round full pot of previous rounds = ', full_pot_previous_rounds)
        logging.debug('set_decisions_first_round folded_players = ', folded_players)

        start_position = (button_position + 3) % 6
        logging.debug('set_decisions_first_round start_position = ', start_position)
        if start_position == 0:
            return

        for player_id in range(start_position, 6):  # if button position+3 is more then 6 then we have to make it less then 6
            logging.debug('set_decisions_first_round player_id = ', player_id)
            logging.debug('set_decisions_first_round previous_bet = ', previous_bet)
            pot = self.get_pot_for_player_decision(player_id)
            logging.debug('set_decisions_first_round pot = ',pot)
            if player_id in folded_players:
                self.decisions[player_id] = 'FOLD'
            elif bets[player_id] is None:
                self.decisions[player_id] = 'CHECK'
            elif 'ALL_IN' in list(self.decisions_after_BB.values()):
            # elif is_previous_allin  == True:
                self.decisions[player_id] = 'CALL'
            elif bets[player_id] == previous_bet:
                self.decisions[player_id] = 'CALL'
            elif bets[player_id] > previous_bet and bets[player_id] <= (3 * pot / 4):
                self.decisions[player_id] = 'RAISE_HALF_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > (3 * pot / 4) and bets[player_id] <= pot + (100 * BIG_BLIND - pot) / 2:
                self.decisions[player_id] = 'RAISE_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > pot + (100 * BIG_BLIND - pot) / 2:
                self.decisions[player_id] = 'ALL_IN'
                previous_bet = bets[player_id]
                # is_previous_allin = True
            else:
                sys.exit('Error. Application can not define decision for first round!')

            logging.debug('set_decisions_first_round self.decisions = ',self.decisions)
        # start_position('finish set_decisions_after_BB')
        # print(' ')
        pass

    def calculate_decisions_after_player(self):

        button_position = self.get_button_position()
        bets = self.get_bets()
        full_pot_previous_rounds = self.get_full_pot()
        folded_players = self.get_folded_players()

        self.decisions_after_player = self.decisions_before_player

        previous_bet = self.bets[0]  # get player's (our) bet

        logging.debug('set_decisions_after_player button_position = ', button_position)
        logging.debug('set_decisions_after_player bets = ', bets)
        logging.debug('set_decisions_after_player full pot of previous rounds = ', full_pot_previous_rounds)
        logging.debug('set_decisions_after_player folded_players = ', folded_players)

        end_position = (button_position + 3) % 6
        # if end_position
        start_position = (button_position + 3) % 6
        logging.debug('set_decisions_after_player start_position = ', start_position)
        if start_position == 0:
            return

        for player_id in range(1, button_position + 3):

            logging.debug('set_decisions_after_player player_id = ', player_id)
            logging.debug('set_decisions_after_player previous_bet = ', previous_bet)
            pot = self.get_pot_for_player_decision(player_id)
            logging.debug('set_decisions_after_player pot = ', pot)

            if player_id in folded_players:
                self.decisions_after_player[player_id] = 'FOLD'
            elif 'ALL_IN' in list(self.decisions_before_BB.values()):
                self.decisions_after_player[player_id] = 'CALL'
            elif player_id == button_position + 2 and bets[player_id] == BIG_BLIND:  # check on BB position
                self.decisions_after_player[player_id] = 'CHECK'
            # elif is_previous_allin  == True:
            #     self.current_decisions[player_id] = 'CALL'
            elif bets[player_id] == previous_bet:
                self.decisions_after_player[player_id] = 'CALL'
            elif bets[player_id] > previous_bet and bets[player_id] <= (3 * pot / 4):
                self.decisions_after_player[player_id] = 'RAISE_HALF_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > (3 * pot / 4) and bets[player_id] <= pot + (100 * BIG_BLIND - pot) / 2:
                self.decisions_after_player[player_id] = 'RAISE_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > pot + 3 * (100 * BIG_BLIND - pot) / 4:
                self.decisions_after_player[player_id] = 'ALL_IN'
                previous_bet = bets[player_id]
                is_previous_allin = True
            else:
                sys.exit('Error. Application can not define decisions after player!')

            logging.debug('set_decisions_after_player self.decisions_after_player = ', self.decisions_after_player)

    def __get_sum_bets(self, bets):
        return sum(filter(lambda x: x is not None, bets.values()))

    def calculate_decisions_after_changing_street(self):

        button_position = self.get_button_position()
        bets = self.get_bets() # bets from current screen
        previous_full_pot = self.get_previous_full_pot() # pot at the previous moment when we asked for pressing button with decision
        full_pot = self.get_full_pot() # it is where we now see on screen: "pot: 123456789" when we asked for pressing button with decision
        current_street_pot = self.__get_sum_bets(bets)
        folded_players = self.get_folded_players()

        pot_previous_round_after_player = full_pot - current_street_pot - previous_full_pot
        bet_previous_round_after_player = self.get_previous_bets()[0]

        # we see folded player after button, he could fold this round or previous
        # we need to decide in wich round hi folded
        num_folded_players_previous_round_after_player = pot_previous_round_after_player/bet_previous_round_after_player

        logging.debug('calculate_decisions_after_changing_street button_position = ', button_position)
        logging.debug('calculate_decisions_after_changing_street folded_players = ', folded_players)
        logging.debug('calculate_decisions_after_changing_street bets = ', bets)
        logging.debug('calculate_decisions_after_changing_street folded_players = ', previous_full_pot)
        logging.debug('calculate_decisions_after_changing_street folded_players = ', full_pot)
        logging.debug('calculate_decisions_after_changing_street folded_players = ', current_street_pot)
        logging.debug('calculate_decisions_after_changing_street folded_players = ', pot_previous_round_after_player)
        logging.debug('calculate_decisions_after_changing_street folded_players = ', bet_previous_round_after_player)
        # logging.debug('calculate_decisions_after_changing_street folded_players = ', num_folded_players_previous_round_after_player)

        # PREVIOUS ROUND
        # player which was the last who raised is the end of previous round
        logging.debug('calculate_decisions_after_changing_street end_position = ', end_position)
        previous_decisions = self.get_previous_decisions()
        logging.debug('calculate_decisions_after_changing_street PREVIOUS ROUND')
        for player_id in previous_decisions.keys().sort(reverse = True):
            if previous_decisions[player_id] == 'RAISE':
                end_position = player_id
                break
        if end_position == 0:
            end_position == 6
        if end_position is None:
            sys.exit('Application. Method calculate_decisions_after_changing_street. Can not define end position!')

        logging.debug('calculate_decisions_after_changing_street end_position = ', end_position)

        for player_id in range(1, end_position):
            if self.previous_decisions[player_id] is not None:
                sys.exit(f'Application. Method calculate_decisions_after_changing_street. Previous_decision for player {player_id} is not None!')
            logging.debug('calculate_decisions_after_changing_street CYCLE player_id = ', player_id)
            logging.debug(
                'calculate_decisions_after_changing_street CYCLE num_folded_players_previous_round_after_player = ',
                num_folded_players_previous_round_after_player)
            if player_id in folded_players and num_folded_players_previous_round_after_player > 0:
                num_folded_players_previous_round_after_player -= 1
                self.previous_decisions[player_id] = 'FOLD'
            else:
                self.previous_decisions[player_id] = 'CALL'

            logging.debug('calculate_decisions_after_changing_street self.previous_decisions = ', self.previous_decisions)

        # CURRENT ROUND
        logging.debug('calculate_decisions_after_changing_street CURRENT ROUND')
        start_position = (button_position + 1) % 6
        logging.debug('calculate_decisions_after_changing_street start_position = ', start_position)
        if start_position == 0:
            return

        previous_bet = 0
        for player_id in range(start_position, 6):
            logging.debug('calculate_decisions_after_changing_street player_id = ', player_id)
            # logging.debug('calculate_decisions_after_changing_street previous_bet = ', previous_bet)
            pot = self.get_pot_for_player_decision(player_id)
            logging.debug('calculate_decisions_after_changing_street pot = ',pot)
            if player_id in folded_players:
                self.decisions[player_id] = 'FOLD'
            elif bets[player_id] is None:
                self.decisions[player_id] = 'CHECK'
            elif 'ALL_IN' in list(self.decisions.values()):
                self.decisions[player_id] = 'CALL'
            elif bets[player_id] == previous_bet:
                self.decisions[player_id] = 'CALL'
            elif bets[player_id] > previous_bet and bets[player_id] <= (3 * pot / 4):
                self.decisions[player_id] = 'RAISE_HALF_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > (3 * pot / 4) and bets[player_id] <= pot + (100 * BIG_BLIND - pot) / 2:
                self.decisions[player_id] = 'RAISE_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > pot + (100 * BIG_BLIND - pot) / 2:
                self.decisions[player_id] = 'ALL_IN'
                previous_bet = bets[player_id]
                # is_previous_allin = True
            else:
                sys.exit('Error. Application can not define decision for first round!')


# class RoundState(object):
#     button_position
#     bets
#     player_cards
#     flop_cards
#     turn_card
#     river_card
#     decisions


if __name__ == '__main__':
    time.sleep(6)

    screen = Screen()
    screen.set_work_position()

    game = Game()


###########
    # print('pot = ',game.get_pot_from_screen())
    # assert 1==6
    # screen = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screenshot.png'), region=(900, 330, 400, 50))
    # pot = pyautogui.locateOnScreen(path.join(HERE, 'data', 'signs', 'pot.png'),
    #                                   confidence=0.95,
    #                                   region=(900, 330, 400, 50),
    #                                   grayscale=False)
    # print('pot = ', pot)
    #
    # screen = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'temp.png'),
    #                               region=(pot[0] + pot[2], pot[1], pot[2] + 300, pot[3]))
    # assert 1==4


    # screen = pyautogui.screenshot(path.join(HERE, 'data', 'screenshots', 'screenshot.png'), region=(1110, 629, 270, 23))
    # sys.exit('hh')
##########
    # print('folded = ', screen.get_folded_players())
    # sys.exit('g')
    # is_first_round = True


    previous_street = None
    n_round = None

    while True:
        if game.wait_for_bet_button(): # waiting for other players finishes placing their bets if necessary

            # read game data from screen
            game.set_community_cards()
            game.set_player_cards()
            game.set_current_street()
            game.set_button_position()
            game.set_bets()
            game.set_folded_players()
            game.set_full_pot()


            # game.set_previous_decisions()
            # game.set_current_decisions()

            street = game.get_current_street()

            # set up logging
            if street != previous_street:
                setup_logger(street, path.join(HERE, 'logs', f'{street}.log'))
                n_round = 1
            else:
                n_round +=1

            if street == 'PREFLOP' and previous_street != 'PREFLOP':
                print('GAME IS STARTED!')
                game.start()
                # print('first_round')
                game.set_decisions_first_round()
                # game.set_decisions_before_player()
            else:
                if street != previous_street:
                    game.calculate_decisions_after_changing_street()
                    # game.set_decisions_after_BB()
                else:
                    game.set_decisions_all_players()
                # game.set_first_round_sign(False)

            screen = pyautogui.screenshot(path.join(HERE, 'logs', f'{street}_{n_round}.png'))

            print(street)
            print('round = ',n_round)

            # we gave data to model
            # model gave us back answer
            # temp answer is CALL
            game.set_decision(PLAYER, 'CALL')
            game.set_bet_by_decision(PLAYER)

            # save data of this round for using it in next round
            game.set_previous_decisions()
            game.set_previous_bets()
            game.set_previous_full_pot()
            previous_street = street

            game.update_full_pot()
            if game.wait_for_player_bet():
                pass

# clear attributres like decisions
