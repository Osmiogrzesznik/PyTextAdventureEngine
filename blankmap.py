

example_event = {
    # onuse
    # room or player or both lamp onuse is player giving him state checked in dark rooms
    'eventClass': "room",
    'eventTyp': 'change',
    'amount_confirmation': 'Unfortunately, wire is no longer usable.',
    # use wire on lock / allowed keywords
    'on': ['door', 'lock', 'keyhole'],
    'change': [{
        # should onUse be optional array? not this but parent dict?

        # 'targetRoom': 'asylum cell', if no target room , can be used on door anywhere
        # lets say that by going under bed and saving wire we can open bonus room
        'prop': 'open',
        'objName': 'door',  # should be only the name of property of object
        'val': True,
        'd': 'Doors are now unlocked. Broken piece of wire stuck in the lock',
        't': 'You Managed to pick the lock with the wire. Doors are now unlocked. '

    }

    ]
}


example_exit = {  # obj name is the dict key in parent
    'hidden': True,
    'conducts': ['sound'],
    'to': 'asylum cell',
    'd': 'wooden door, not locked, light comes out through splits'
    'onopen': {
        # if playerhasitem'lamp' and item isActive
        # if playerHasState litLamp
        # if player has item wire here is not good

        'req': {
            'objName': 'wire',
            'playerProp': 'inventory'
        },
        'reqOK': 'it seems that i could use wire to pick the lock',
        'reqFail': 'maybe i could use something to pick the lock'
    },
    'fail': 'doors are closed, it seems that i could use something to pick the lock',
    'open': False,
    'opened by': 'wire',
    'alt': ['east', 'door'],
}


example_room = {

}

example_map = {
    'hunters': {

    },
    'rooms': {
        'start': {

        }
    }
}
