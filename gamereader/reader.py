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

        def get_shift(player_id):
            # if no chip in picture where we are going to find value of bet then no shift is needed so return 0
            # if chip in picture, so we need to correct region to exclude chip so return shift
            WIDTH_CHIP = 39
            def locate_no_chip(player_id, shift):
                DELTA = 0

                regions = {0: (1110 + shift + DELTA, 629, WIDTH_CHIP, 23),
                           1: (805 + shift + DELTA, 568, WIDTH_CHIP, 23),
                           2: (825 + shift + DELTA, 349, WIDTH_CHIP, 23),
                           3: (1239 + shift + DELTA, 250, WIDTH_CHIP, 23),
                           4: (1230 + shift + DELTA, 313, WIDTH_CHIP, 23),
                           5: (1270 + shift + DELTA, 568, WIDTH_CHIP, 23)}

                chip = pyautogui.screenshot(
                    path.join(HERE, 'data', 'screenshots', f'chip_{player_id}.png'),
                    region=regions[player_id]
                )

                chip = np.array(chip)
                chip = cv2.cvtColor(chip, cv2.COLOR_BGR2GRAY)
                threshold = 170
                _, thresh = cv2.threshold(chip, threshold, 255, cv2.THRESH_BINARY)
                # cv2.imshow('thresh',thresh)
                # key = cv2.waitKey(0)
                cv2.imwrite(path.join(HERE, 'data', 'screenshots', f'chip_{player_id}.png'), chip)

                no_chip = pyautogui.locate(path.join(HERE, 'data', 'signs', 'no_chip.png'),
                                           path.join(HERE, 'data', 'screenshots', f'thresh_{player_id}.png'),
                                           grayscale=True)

                return no_chip

            shift = 0
            while True:
                no_chip = locate_no_chip(player_id, shift)

                if no_chip is None:
                    break
                else:
                    shift += WIDTH_CHIP # width if chip

            return shift

        DELTA = 0
        bets = {}


        for player_id in regions.keys():

            shift = get_shift(player_id)
            regions = {0: (1110 + shift - DELTA, 629 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA),
                       1: (805 + shift - DELTA, 568 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA),
                       2: (825 + shift - DELTA, 349 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA),
                       3: (1239 + shift - DELTA, 250 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA),
                       4: (1230 - shift - DELTA, 313 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA),
                       5: (1270 - shift - DELTA, 568 - DELTA, 270 + 2 * DELTA, 23 + 2 * DELTA)}

            bet_screen_PIL = pyautogui.screenshot(
                path.join(HERE, 'data', 'screenshots', f'bet_screen_{player_id}_{datetime.now().timestamp()}.png'),
                region=regions[player_id]
            )
            # convert PIL image to opencv format
            bet_screen_CV = np.array(bet_screen_PIL)
            # cv2.imwrite(f'bet_screen_CV{player_id}.png', bet_screen_CV)
            bets[player_id] = ocr_digits.get_number(bet_screen_CV)

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
        self.previous_full_pot = 0
        self.folded_players_all_before_current_round = []

    def start(self):
        # self.full_pot = 0
        # self.previous_full_pot = 0
        # self.previous_decisions = None
        # self.previous_bets = None
        # self.set_first_round_sign(True)

        # clear previous logs
        filelist = [f for f in glob(path.join(HERE, 'logs', '*.*'))]
        for f in filelist:
            remove(f)

    def clear_decisions(self):
        self.decisions = {}

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

    def set_bet_by_decision(self):
        #it works only for player id = 0
        player_id = 0
        if self.decisions[player_id] == 'CALL':
            # since we CALL we need previous player with bet
            folded_players_current_round = self.get_folded_players_current_round()
            active_players = list(set(self.bets.keys()) - set(folded_players_current_round))
            active_players.sort(reverse=True)
            logger.debug(f'!!! set_bet_by_decision active_players = {active_players}')
            self.bets[player_id] = self.bets[active_players[0]]
        logger.debug(f'!!! set_bet_by_decision self.decisions[player_id] = {self.decisions[player_id]}')
        logger.debug(f'!!! set_bet_by_decision self.bets[player_id] = {self.bets[player_id]}')

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

    def get_pot_for_player_decision_old(self, player_id):
        button_position = self.get_button_position()
        if player_id is not None:
            player_id_list = [x for x in self.bets.keys() if x > button_position and x < player_id]
            bets = [self.bets[player_id] for player_id in player_id_list]

            # self.get_full_pot() must return full pot without bets of current round
            pot = self.get_previous_full_pot() + sum(filter(lambda x: x is not None, bets))
        else:
            sys.exit('Game.get_pot_for_player_decision() player_id is None')
        return pot
    def get_pot_for_player_decision(self, player_id):
        # button_position = self.get_button_position()
        if player_id is not None:
            player_id_list = [x for x in self.get_bets().keys() if x >=0 and x < player_id]
            bets = [self.get_bets()[player_id] for player_id in player_id_list]

            # self.get_full_pot() must return full pot without bets of current round
            pot = self.get_previous_full_pot() + sum(filter(lambda x: x is not None, bets))
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

    def set_decisions_all_players(self):

        def get_pot_for_player(player_id):
            # only for
            # button_position = self.get_button_position()
            if player_id is not None:
                player_id_list = [x for x in self.get_bets().keys() if x < 6 and x > player_id]
                bets = [self.get_bets()[player_id] for player_id in player_id_list]

                # self.get_full_pot() must return full pot without bets of current round
                pot = self.get_full_pot() - sum(filter(lambda x: x is not None, bets))
            else:
                sys.exit('Game.get_pot_for_player_decision() player_id is None')
            return pot

        # logging.debug('start set_decisions_after_BB')

        button_position = self.get_button_position()
        bets = self.get_bets()
        # previous_full_pot = self.get_previous_full_pot()  # pot at the previous moment when we asked for pressing button with decision
        # folded_players = self.get_folded_players()

        folded_players_current_round = self.get_folded_players_current_round()
        folded_players_all_before_current_round = self.get_folded_players_all_before_current_round()

        # self.decisions = {} # TODO

        previous_bet = self.get_previous_bets()[0]
        # is_previous_allin = False
        logger.debug(f'set_decisions_all_players button_position = {button_position}')
        logger.debug(f'set_decisions_all_players bets = {bets}')
        # logger.debug(f'set_decisions_all_players full pot of previous rounds = ', full_pot_previous_rounds)
        logger.debug(f'set_decisions_all_players folded_players_current_round = {folded_players_current_round}')
        logger.debug(f'set_decisions_all_players folded_players_all_before_current_round = {folded_players_all_before_current_round}')

        for player_id in range(1, 6):
            logger.debug(f'set_decisions_all_players CYCLE player_id = {player_id}')
            # logger.debug(f'set_decisions_all_players CYCLE bets[{player_id}] = {bets[player_id]}')
            logger.debug(f'set_decisions_all_players CYCLE previous_bet = {previous_bet}')
            pot = get_pot_for_player(player_id)
            logger.debug(f'set_decisions_all_players CYCLE pot = {pot}')
            if player_id in folded_players_all_before_current_round:
                logger.debug(f'set_decisions_all_players CYCLE player {player_id} NO DECISION because he folded before')
                continue
            elif player_id in folded_players_current_round:
                self.decisions[player_id] = 'FOLD'
            elif bets[player_id] is None:
                self.decisions[player_id] = 'CHECK'
            elif self.decisions is not None and 'ALL_IN' in list(self.decisions.values()):
            # elif is_previous_allin  == True:
                self.decisions[player_id] = 'CALL'
            elif bets[player_id] == previous_bet:
                self.decisions[player_id] = 'CALL'
            elif bets[player_id] > previous_bet and bets[player_id] <= (3 * pot / 4):
                self.decisions[player_id] = 'RAISE_HALF_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > (3 * pot / 4) and bets[player_id] <= pot + (100 * 2 * BLIND - pot) / 2:
                self.decisions[player_id] = 'RAISE_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > pot + (100 * 2 * BLIND - pot) / 2:
                self.decisions[player_id] = 'ALL_IN'
                previous_bet = bets[player_id]
                # is_previous_allin = True
            else:
                sys.exit('Error. Application can not define decision before player!')

            logger.debug(f'set_decisions_all_players decisions = {self.decisions}')
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
        # logger.debug(f'start set_decisions_after_BB')
        button_position = self.get_button_position()
        bets = self.get_bets()
        # previous_full_pot = self.get_previous_full_pot()  # pot at the previous moment when we asked for pressing button with decision
        # folded_players = self.get_folded_players()

        folded_players_current_round = self.get_folded_players_current_round()

        # self.decisions = {}

        previous_bet = 2 * BLIND
        # is_previous_allin = False

        logger.debug(f'set_decisions_first_round button_position = {button_position}')
        logger.debug(f'set_decisions_first_round bets = {bets}')
        # logger.debug(f'set_decisions_first_round previous_full_pot = ', previous_full_pot)
        logger.debug(f'set_decisions_first_round folded_players_current_round = {folded_players_current_round}')

        start_position = (button_position + 3) % 6
        logger.debug(f'set_decisions_first_round start_position = {start_position}')
        if start_position == 0:
            return

        for player_id in range(start_position, 6):
            logger.debug(f'set_decisions_first_round CYCLE player_id = {player_id}')
            logger.debug(f'set_decisions_first_round CYCLE previous_bet = {previous_bet}')
            pot = self.get_pot_for_player_decision(player_id)
            logger.debug(f'set_decisions_first_round CYCLE pot = {pot}')
            if player_id in folded_players_current_round:
                self.decisions[player_id] = 'FOLD'
            elif bets[player_id] is None:
                self.decisions[player_id] = 'CHECK'
            elif self.decisions is not None and 'ALL_IN' in list(self.decisions.values()):
                self.decisions[player_id] = 'CALL'
            elif bets[player_id] == previous_bet:
                self.decisions[player_id] = 'CALL'
            elif bets[player_id] > previous_bet and bets[player_id] <= (3 * pot / 4):
                self.decisions[player_id] = 'RAISE_HALF_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > (3 * pot / 4) and bets[player_id] <= pot + (100 * 2 * BLIND - pot) / 2:
                self.decisions[player_id] = 'RAISE_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > pot + (100 * 2 * BLIND - pot) / 2:
                self.decisions[player_id] = 'ALL_IN'
                previous_bet = bets[player_id]
                # is_previous_allin = True
            else:
                sys.exit('Error. Application can not define decision for first round!')

            logger.debug(f'set_decisions_first_round self.decisions = {self.decisions}')
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

    def set_decisions_after_changing_street(self):
        current_street = self.get_current_street()
        button_position = self.get_button_position()
        bets = self.get_bets() # bets from current screen
        # previous_full_pot = self.get_previous_full_pot() # pot at the previous moment when we asked for pressing button with decision

        #TODO temp check
        # if not previous_full_pot > 0:
        #     sys.exit('calculate_decisions_after_changing_street previous_full_pot not more then 0')

        full_pot = self.get_full_pot() # it is where we now see on screen: "pot: 123456789" when we asked for pressing button with decision
        # current_street_pot = self.__get_sum_bets(bets)

        # if current_street == 'FLOP':
        #     previous_full_pot = previous_full_pot - 2 * BLIND - BLIND + self.previous_bets[0]
        # Site gets commission after changing street
        # pot_commission_value = self.__get_commission(full_pot, current_street_pot)

        # folded_players_all = self.get_folded_players_all() # all folded players that we see on a screen now
        folded_players_current_round = self.get_folded_players_current_round()
        folded_players_all_before_current_round = self.get_folded_players_all_before_current_round()
        folded_players_all_before_current_street = [x for x in folded_players_all_before_current_round]

        # pot_previous_street_current_screen = full_pot - current_street_pot - previous_full_pot + pot_commission_value# we dont see on screen bets of previous street that made after our previous decision
        # bet_previous_street_current_screen = self.get_previous_bets()[0]

        # we see folded player after button, he could fold this round or previous
        # we need to decide in which round he folded
        logger.debug(f'set_decisions_after_changing_street current_street = {current_street}')
        logger.debug(f'set_decisions_after_changing_street button_position = {button_position}')
        logger.debug(f'set_decisions_after_changing_street folded_players_current_round = {folded_players_current_round}')
        logger.debug(f'set_decisions_after_changing_street folded_players_all_before_current_round = {folded_players_all_before_current_round}')
        logger.debug(f'set_decisions_after_changing_street bets = {bets}')
        # logger.debug(f'set_decisions_after_changing_street previous_full_pot = {previous_full_pot}')
        logger.debug(f'set_decisions_after_changing_street full_pot = {full_pot}')
        # logger.debug(f'set_decisions_after_changing_street current_street_pot = {current_street_pot}')
        # logger.debug(f'set_decisions_after_changing_street pot_previous_street_current_screen = {pot_previous_street_current_screen}')
        # logger.debug(f'set_decisions_after_changing_street bet_previous_street_current_screen = {bet_previous_street_current_screen}')
        logger.debug(f'set_decisions_after_changing_street folded_players_all_before_current_round = {folded_players_all_before_current_round}')
        # logger.debug(f'set_decisions_after_changing_street pot_commission_value = {pot_commission_value}')
        # logger.debug(f'calculate_decisions_after_changing_street folded_players = ', num_folded_players_previous_round_after_player)

        # PREVIOUS STREET of CURRENT SCREEN
        # if someone raised after us then we wouldnt get into this function
        # and we will get into set_decisions_all_players

        # if someone who was last who raised before us then street will finish only after decisions all players before last raised
        logger.debug(f'set_decisions_after_changing_street PREVIOUS ROUND')
        # player which was the last who raised is the end of previous round
        previous_decisions = self.get_previous_decisions()
        logger.debug(f'set_decisions_after_changing_street previous_decisions = {previous_decisions}')
        end_position = None
        player_id_list = list(previous_decisions.keys())
        player_id_list.sort(reverse=True)
        for player_id in player_id_list:
            if previous_decisions[player_id] == 'RAISE':
                end_position = player_id - 1
                break
        if end_position is None: # None of players raised
            if current_street == 'FLOP':
                end_position = button_position + 2 # end of PREFLOP
                end_position = end_position % 6
            else:
                end_position = button_position

        if end_position == 0:
            end_position = 6

        logger.debug(f'set_decisions_after_changing_street end_position = {end_position}')

        # Check.
        # If not pot_previous_street_current_screen > 0 then all players of previous street CHECKED
        # If end_position != button_position + 1 then at least one player RAISED
        # If end_position > 1 then previous street of current screen is exist so this check is reasonable
        # if not pot_previous_street_current_screen > 0 and end_position != button_position + 1 and end_position > 1:
        #     sys.exit(f'set_decisions_after_changing_street pot_previous_street_current_screen = {pot_previous_street_current_screen} and end_position = {end_position}')

        # if pot_previous_street_current_screen > 0:
        #
        #     num_active_players_previous_street_current_screen = pot_previous_street_current_screen / bet_previous_street_current_screen
        #     logger.debug(f'set_decisions_after_changing_street CYCLE num_active_players_previous_street_current_screen = {num_active_players_previous_street_current_screen}')
        #
        #     if num_active_players_previous_street_current_screen%1 >0.0001:
        #         sys.exit('set_decisions_after_changing_street num_active_players_previous_street_current_screen must be integer')
            # (end_position - 1) = is full number of players of previous street after us (that is of current screen)
            # num_folded_players_previous_street_current_screen = end_position - 1 - num_active_players_previous_street_current_screen

        for player_id in range(1, end_position + 1):
            logger.debug(f'set_decisions_after_changing_street CYCLE player_id = {player_id}')
            logger.debug(f'set_decisions_after_changing_street CYCLE num_folded_players_previous_street_current_screen = {num_folded_players_previous_street_current_screen}')
            logger.debug(f'set_decisions_after_changing_street CYCLE folded_players_all_before_current_street = {folded_players_all_before_current_street}')
            if player_id in folded_players_all_before_current_round:
                logger.debug(f'set_decisions_all_players CYCLE player {player_id} NO DECISION because he folded before')
                continue
            elif player_id in folded_players_current_round:
                folded_players_all_before_current_street.append(player_id)
                self.previous_decisions[player_id] = 'FOLD'
            # below FOLD is defenitly in previous street
            # elif player_id in folded_players_current_round and player_id <= button_position:
            #     num_folded_players_previous_street_current_screen -= 1
            #     folded_players_all_before_current_street.append(player_id)
            #     self.previous_decisions[player_id] = 'FOLD'
            # below FOLD is that can be made both in previous and current street
            # we have to decide in which street FOLD is made
            # TODO if after button and before end_position two players were folded
            #  then we cant define which of them folded in previous street and which - in current
            # elif player_id in folded_players_current_round and player_id > button_position and player_id < end_position and num_folded_players_previous_street_current_screen > 0:
            #     num_folded_players_previous_street_current_screen -= 1
            #     folded_players_all_before_current_street.append(player_id)
            #     self.previous_decisions[player_id] = 'FOLD'
            elif not pot_previous_street_current_screen > 0:
                self.previous_decisions[player_id] = 'CHECK'
            elif current_street == 'FLOP' and player_id == (button_position + 2) % 6 and end_position == (button_position + 2) % 6:  # player on big blind on preflop
                self.previous_decisions[player_id] = 'CHECK'
            else:
                self.previous_decisions[player_id] = 'CALL'

            logger.debug(f'set_decisions_after_changing_street CYCLE self.previous_decisions = {self.previous_decisions}')

        # CURRENT ROUND
        logger.debug(f'set_decisions_after_changing_street CURRENT ROUND')
        start_position = (button_position + 1) % 6
        logger.debug(f'set_decisions_after_changing_street start_position = {start_position}')
        if start_position == 0:
            return

        previous_bet = 0
        for player_id in range(start_position, 6):
            logger.debug(f'set_decisions_after_changing_street CYCLE player_id = {player_id}')
            # logger.debug(f'calculate_decisions_after_changing_street previous_bet = ', previous_bet)
            pot = self.get_pot_for_player_decision(player_id)
            logger.debug(f'set_decisions_after_changing_street CYCLE pot = {pot}')
            logger.debug(f'set_decisions_after_changing_street CYCLE previous_bet = {previous_bet}')
            if player_id in folded_players_all_before_current_street:
                logger.debug(f'set_decisions_all_players CYCLE player {player_id} NO DECISION because he folded before')
                continue
            elif player_id in folded_players_current_round:
                self.decisions[player_id] = 'FOLD'
            elif bets[player_id] is None:
                self.decisions[player_id] = 'CHECK'
            elif self.decisions is not None and 'ALL_IN' in list(self.decisions.values()):
                self.decisions[player_id] = 'CALL'
            elif bets[player_id] == previous_bet:
                self.decisions[player_id] = 'CALL'
            elif bets[player_id] > previous_bet and bets[player_id] <= (3 * pot / 4):
                self.decisions[player_id] = 'RAISE_HALF_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > (3 * pot / 4) and bets[player_id] <= pot + (100 * 2 * BLIND - pot) / 2:
                self.decisions[player_id] = 'RAISE_POT'
                previous_bet = bets[player_id]
            elif bets[player_id] > pot + (100 * 2 * BLIND - pot) / 2:
                self.decisions[player_id] = 'ALL_IN'
                previous_bet = bets[player_id]
                # is_previous_allin = True
            else:
                sys.exit('Error. Application can not define decision for first round!')

            logger.debug(f'set_decisions_after_changing_street CYCLE self.decisions = {self.decisions}')


# class RoundState(object):
#     button_position
#     bets
#     player_cards
#     flop_cards
#     turn_card
#     river_card
#     decisions


if __name__ == '__main__':
    time.sleep(3)

    screen = Screen()
    screen.set_work_position()

    game = Game()

####
    # street = 'test1'
    # setup_logger(street, path.join(HERE, 'logs', f'{street}.log'))
    # logger.debug(f'test1')
    # street = 'test2'
    # setup_logger(street, path.join(HERE, 'logs', f'{street}.log'))
    # logger.debug(f'test2')
    # sys.exit('g')
    # assert 1==4
    ####
    previous_street = None
    n_round = None

    game.set_bets()

    while True:
        if game.wait_for_bet_button(): # waiting for other players finishes placing their bets if necessary

            # read game data from screen
            game.set_community_cards()
            game.set_player_cards()
            game.set_current_street()
            game.set_button_position()
            game.set_bets()
            game.set_folded_players_all()
            game.set_full_pot()
            # print('!!! 1 game.full_pot = ',game.full_pot)

            game.clear_decisions()
            # game.set_previous_decisions()
            # game.set_current_decisions()

            street = game.get_current_street()
            # print('!!! 2 game.full_pot = ', game.full_pot)
            if street == 'PREFLOP' and previous_street != 'PREFLOP':
                print('GAME IS STARTED!')
                game.start()

            # set up logger
            if street != previous_street:
                setup_logger(street, path.join(HERE, 'logs', f'{street}.log'))
                n_round = 1
            else:
                n_round += 1

            screen = pyautogui.screenshot(path.join(HERE, 'logs', f'{street}_{n_round}.png'))

            logger.debug(f'current street {street}')
            logger.debug(f'previous street {previous_street}')
            logger.debug(f'round = {n_round}')
            print(street)
            print('round = ', n_round)
            # print('!!! 3 game.full_pot = ', game.full_pot)

            if street == 'PREFLOP' and previous_street != 'PREFLOP':
                game.set_decisions_first_round()
            else:
                if street != previous_street:
                    game.set_decisions_after_changing_street()
                else:
                    game.set_decisions_all_players()
            # print('!!! 4 game.full_pot = ', game.full_pot)
            # we gave data to model
            # model gave us back answer
            # temp answer is CALL
            game.set_decision(PLAYER, 'CALL')
            game.set_bet_by_decision()

            # save data of this round for using it in next round
            game.set_previous_decisions()
            game.set_previous_bets()
            # print('!!! 5 game.full_pot = ', game.full_pot)
            game.set_previous_full_pot()
            previous_street = street

            game.set_folded_players_all_before_current_round()
            # game.update_full_pot()
            if game.wait_for_player_bet():
                pass

            logger.debug(' ')


# clear attributres like decisions
