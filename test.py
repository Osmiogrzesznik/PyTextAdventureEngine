from copy import deepcopy
from maps.map1 import map
from user_interface import TestUserInterfaceBuffered
from game_init import *
import unittest

testUI = TestUserInterfaceBuffered()
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

spoon_item = {
    'name': 'spoon',
    'onUse': {
        # multiple use targets silver spoon can attack the werewolf or help with food or make noise when thrown
        'eventClass': 'room',
        'eventTyp': 'change',
        'amount_confirmation': 'there is no spoon no longer',
        # use wire on lock / allowed keywords
        'on': ['food', 'bowl'],
        'change': {
            # should onUse be optional array? not this but parent dict?

            'targetRoom': 'start',  # if no target room , can be used on door anywhere
                                    # lets say that by going under bed and saving wire we can open bonus room
                                    'prop': 'empty',
                                    'objName': 'food',  # should be only the name of property of object
                                    'val': True,
                                    'd': 'you ate the food, with the spoon itself',  # description of what exactly ?
                                    't': 'you ate the food, with the spoon itself'
        }
    },
    'onThrow': {
        'eventClass': 'room',
        'eventTyp': 'sound',
    },

    'amount_to_take': 1,
    'use_amount': 1,  # uses 1 is default
    'd': '''a silver spoon'''
}


class TestGameScenario(unittest.TestCase):
    def setUp(self):
        self.textUI = testUI
        pass
    # TODO do blank room templates
    # test:
    # moving
    # passage of time
    # timeevent - few types
    # take examine so on
    #  death

    def test_integration_take(self):
        self.mapp = {
            'rooms': {
                'start': {
                    'd': 'room',
                    'items': {
                        'spoon': spoon_item
                    }
                }
            }
        }
        game = Game(self.mapp, self.textUI, None, None)
        game.handleUserInput("take spoon")
        self.assertTrue(game.playerHas('spoon'))

    def test_integration_scenario(self):
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
        self.game = Game(self.mapp, self.textUI, None, None)
        for cm in self.scenario:
            self.game.handleUserInput(cm)
            if not self.scenario[cm]:
                continue

            self.assertTrue(scenario[cm](self.game))


if __name__ == "__main__":
    unittest.main()
