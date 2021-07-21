import logging
from os import path
import rlcard
from rlcard.agents import NolimitholdemHumanAgent as HumanAgent
from rlcard.utils import print_card
import torch
from rlcard.agents.nfsp_agent_pytorch import NFSPAgent
from glob import glob
from os import path, remove

HERE = path.abspath(path.dirname(__file__))

# clear previous logs
filelist = [f for f in glob(path.join(HERE, 'logs', '*.*'))]
for f in filelist:
    remove(f)

logging.basicConfig(filename=path.join(HERE, 'logs', 'log.txt'),
                    format='%(asctime)s %(name)s %(funcName)s %(message)s',
                    datefmt='%m-%d %H:%M',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

if __name__ == '__main__':


    # Make environment
    # Set 'record_action' to True because we need it to print results
    env = rlcard.make('no-limit-holdem',
                      config={'record_action': True, 'game_player_num': 6, 'chips_for_each': [100] * 6}
                      )

    human_agent0 = HumanAgent(env.action_num)
    human_agent1 = HumanAgent(env.action_num)
    human_agent2 = HumanAgent(env.action_num)
    human_agent3 = HumanAgent(env.action_num)
    human_agent4 = HumanAgent(env.action_num)

    nfsp_agent = NFSPAgent(scope='nfsp' + str(2),
                           action_num=env.action_num,
                           state_shape=env.state_shape,
                           hidden_layers_sizes=[512, 1024, 2048, 1024, 512],
                           q_mlp_layers=[512, 1024, 2048, 1024, 512],
                           device=torch.device('cpu'))

    # checkpoint = torch.load(r'D:\Development\Jupiter\ rlcard\models\pretrained\nolimit_holdem_nfsp_pytorch\new\model.pth')
    checkpoint = torch.load(
        r'D:\Development\PyCharm\rlcard\rlcard\models\pretrained\leduc_holdem_nfsp_pytorch\20210501\model.pth')

    nfsp_agent.load(checkpoint)

    # random_agent = RandomAgent(action_num=env.action_num)

    env.set_agents([nfsp_agent, human_agent0, human_agent1, human_agent2, human_agent3, human_agent4])

    # env.game.dealer_id = 1

    while (True):
        print(">> Start a new game")
        print(type(env))
        trajectories, payoffs = env.run(is_training=False)
        # If the human does not take the final action, we need to
        # print other players action
        final_state = trajectories[0][-1][-2]
        action_record = final_state['action_record']
        state = final_state['raw_obs']
        _action_list = []
        for i in range(1, len(action_record) + 1):
            if action_record[-i][0] == state['current_player']:
                break
            _action_list.insert(0, action_record[-i])
        for pair in _action_list:
            print('>> Player', pair[0], 'chooses', pair[1])

        # Let's take a look at what the agent card is
        print('===============     Cards all Players    ===============')
        for hands in env.get_perfect_information()['hand_cards']:
            print_card(hands)

        print('===============     Result     ===============')
        if payoffs[0] > 0:
            print('You win {} chips!'.format(payoffs[0]))
        elif payoffs[0] == 0:
            print('It is a tie.')
        else:
            print('You lose {} chips!'.format(-payoffs[0]))
        print('')
        print('all payoffs = ', payoffs)
        input("Press any key to continue...")