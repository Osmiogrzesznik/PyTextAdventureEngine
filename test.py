from copy import deepcopy
from map1 import map
from user_interface import testUserInterface, UserInterface
from game_init import *
import unittest

testUI = testUserInterface()
# game should be called timeline? can be restarted with data of the past game

# game.start_loop('y')
scenario = {
    'wake up': 0,
    'look bed': 0,
    'look pillow': 0,
    'take pillow': lambda game: 'wire' in game.current.dct['items'],
    # displays cannot take pilow yet wire is present in items
    'take wire': lambda game: game.playerHas('wire'),
    # what is returned from game_init line 216 obinfo is an actual object ont an info,
    # check why it happens and make sure the object returned is always objectinfo
    'open door': 0,
    'pick the lock': lambda game: game.current.dct['exits']['door']['open'],
    'go door': lambda game: game.current.name != 'asylum cell'
}


class TestGameScenario(unittest.TestCase):
    def setUp(self):
        self.mapp = deepcopy(map)
        self.scenario = {
            'wake up': 0,
            'look bed': 0,
            'look pillow': 0,
            'take pillow': lambda game: 'wire' in game.current.dct['items'],
            # displays cannot take pilow yet wire is present in items
            'take wire': lambda game: game.playerHas('wire'),
            # what is returned from game_init line 216 obinfo is an actual object ont an info,
            # check why it happens and make sure the object returned is always objectinfo
            'open door': 0,
            'pick the lock': lambda game: game.current.dct['exits']['door']['open'],
            'go door': lambda game: game.current.name != 'asylum cell'
        }
        self.textUI = testUserInterface()
        self.game = Game(self.mapp, self.textUI, None, None)

    def test_scenario(self):
        for cm in self.scenario:
            self.game.handleUserInput(cm)
            if not self.scenario[cm]:
                continue

            self.assertTrue(scenario[cm](self.game))


if __name__ == "__main__":
    unittest.main()
