from rlcard.utils.utils import print_card

from gamereader import reader
import logging
logger = logging.getLogger(__name__)

class HumanAgent(object):
    ''' A human agent for No Limit Holdem. It can be used to play against trained models
    '''

    def __init__(self, action_num):
        ''' Initilize the human agent

        Args:
            action_num (int): the size of the ouput action space
        '''
        self.use_raw = True
        self.action_num = action_num



    @staticmethod
    def step(state, reader_game):
        ''' Human agent will display the state and make decisions through interfaces

        Args:
            state (dict): A dictionary that represents the current state

        Returns:
            action (int): The action decided by human
        '''

        def get_action_from_reader(reader_game, player_id):
            reader_action = reader_game.get_action_for_AI(player_id)
            logger.debug(f'reader_action = {reader_action}')

        print('#### step state = ', state)
        print('#### step reader_game.get_actions_current_street() = ', reader_game.get_actions_current_street())
        _print_state(state['raw_obs'], state['action_record'])
        player_id = state['raw_obs']['current_player']
        print('#### step player_id = ', player_id)
        get_action_from_reader(reader_game, player_id)
        action = int(input('>> You choose action (integer): '))
        while action < 0 or action >= len(state['legal_actions']):
            print('Action illegel...')
            action = int(input('>> Re-choose action (integer): '))
        return state['raw_legal_actions'][action]

    def eval_step(self, state, reader_game):
        ''' Predict the action given the curent state for evaluation. The same to step here.

        Args:
            state (numpy.array): an numpy array that represents the current state

        Returns:
            action (int): the action predicted (randomly chosen) by the random agent
            probs (list): The list of action probabilities
        '''
        return self.step(state, reader_game), []

def _print_state(state, action_record):
    ''' Print out the state

    Args:
        state (dict): A dictionary of the raw state
        action_record (list): A list of the historical actions
    '''
    _action_list = []
    for i in range(1, len(action_record)+1):
        if action_record[-i][0] == state['current_player']:
            break
        _action_list.insert(0, action_record[-i])
    for pair in _action_list:
        print('>> Player', pair[0], 'chooses', pair[1])

    # print('\n=============== Community Card ===============')
    # print_card(state['public_cards'])
    #
    # print('=============  Player',state["current_player"],'- Hand   =============')
    # print_card(state['hand'])

    print('===============     Chips      ===============')
    print('In Pot:',state["pot"])
    print('Remaining:',state["stakes"])

    print('\n=========== Actions Player',state["current_player"],'Can Choose ===========')
    print(', '.join([str(index) + ': ' + str(action) for index, action in enumerate(state['legal_actions'])]))
    print('')
    # print(state)
