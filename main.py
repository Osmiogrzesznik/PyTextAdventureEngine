# qpy:3
# qpy:console
from copy import deepcopy
from map1 import map
from user_interface import testUserInterface, UserInterface
from game_init import *


textUI = testUserInterface()
# game should be called timeline? can be restarted with data of the past game
game = Game(deepcopy(map), textUI, None, None)
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

}

# test
for cm in scenario:

    print('TEST SCRIPT ENTERED COMMAND:' + cm)
    game.handleUserInput(cm)
    if scenario[cm]:
        if scenario[cm](game):
            working = 'working'
        else:
            working = 'not working'
        print('TEST:\'' + cm + '\' command is ' + working)


print('TEST HAS ENDED')
