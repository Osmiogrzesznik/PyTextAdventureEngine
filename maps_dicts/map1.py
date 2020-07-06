map = {
    'rooms': {
        'start': {
            'cmds': {
                'open eyes': {
                    'alt': ['wake up', 'awake', 'get up'],
                    'do': 'go awake',
                },
            },
            'once': 'THE VOICE',
            'd': ''' Darkness, darkness everywhere, you feel like you just left some place.
        You were hunted, somebody , somewhere...
        .. You don't remember exactly. There was voices - telling you what to do. They told you what will happen.
         You didn't want to listen to them. But you did. There was people that did you harm.
        But it all is fading, becoming harder to grip on, with every second and slipping away into oblivion.
        all that remains is short breath and fast pulse of heavily pounding heart.
        You feel the hard mattress, moist, soaked with sticky sweat under your back
        You hear the voice really close to your ear:
        V: Wake up, it's me John.''',
            'onTime': {
                5: {
                    't': ''' V: Come on John, open your eyes. We have no time!''',
                },
                10: {
                    't': ''' V: Oh come on, just wake up. Quickly, they are coming to get you!''',
                },
                15: {
                    't': ''' V: If you will stay here, they will kill you. Trust me.''',
                },
                20: {
                    't': ''' V: They will come any second now. Fuck, are you deaf? Awake John, dont make me repeat myself again''',
                },
                25: {
                    't': ''' You hear multiple footsteps behind the door and muffled voices''',
                },
                30: {
                    't': ''' You hear sound of rattling keys and unlocking the door''',
                }
            },
            'exits': {
                'awake': {
                    'hidden': True,
                    'conducts': ['sound'],
                    'to': 'asylum cell',
                    'd': 'wooden door, not locked, light comes out through splits'
                }
            },
        },
        'asylum cell': {
            'ds': {
                'keyhole': {
                    'alt': ['lock'],
                    'd': 'you can see yellow wall in front of the door, '
                }
            },
            'items': {},  # nothing yet but there is a wire under pillow
            'once': '''You wake up. You dont see anybody. You are opening your eyes. You are in a dark room.
             You get up from bed and stare intesively into impenetrable, and seemingly empty darkness. But you swear the voice was really close to your ear''',
            'd': '''There is a bunk bed here.
There is strip of light pouring from under the door  with one door to the east''',
            'cmds': {
                'pick the lock': {
                    'alt': ['pick lock', 'open door with wire'],
                    'do': 'use wire on keyhole'  # if no wire
                },
                'lift pillow up': {  # this should be in the item_containers or openables
                    'alt': ['take pillow', 'check under pillow', 'look under pillow'],
                    't': 'you lifted the pillow, there is piece of wire under',
                    # add moves this item from here to items section of the room
                    'add': {  # give would be like add.inventory
                        # should i have some way to determine if event works on player or Room or just run it on both and see?
                        # 'eventClass': 'room',
                        'items': {
                            # what/where 'items' to collect in current room
                            'name': 'wire',
                                    'onUse': {
                                        # room or player or both lamp onuse is player giving him state checked in dark rooms
                                        'eventClass': "room",
                                        'eventTyp': 'change',
                                        'amount_confirmation': 'Unfortunately, wire is no longer usable.',
                                        # use wire on lock / allowed keywords
                                        'on': ['door', 'lock', 'keyhole'],
                                        'change': {
                                            # should onUse be optional array? not this but parent dict?

                                            # 'targetRoom': 'asylum cell', if no target room , can be used on door anywhere
                                            # lets say that by going under bed and saving wire we can open bonus room
                                            'prop': 'open',
                                            'objName': 'door',  # should be only the name of property of object
                                            'val': True,
                                            'd': 'Doors are now unlocked. Broken piece of wire stuck in the lock',
                                            't': 'You Managed to pick the lock with the wire. Doors are now unlocked. '
                                        }
                                    },
                            'amount_to_take': 1,
                            'use_amount': 1,  # uses 1 is default
                            'd': '''piece of stripped and straightened mains copper wire.
                         About 2mm thick. Stiff, and doesnt bend easily, sharpened and bend into a tiny hook on one end'''
                        }
                    },

                },
            },
            'exits': {
                'door': {
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
                    'to': 'hallway',
                    'd': 'wooden door, locked, light comes out from under. There is a keyhole.'
                },
                'bed': {
                    'to': 'under the bed',
                    'd': 'basic bunk, not much to say, it is high enough to fit under it. There is a pillow and a duvet.'
                }
            },
            'switches': {
                'switch': {
                    't': 'light has turned on.',
                    'd': 'just normal light switch',
                    'values': ['off', 'on'],
                    'currentValue': 0,
                    'change_room_desc': '''light is now on. You see bed next to you, 
                    wet with sweat stains .there is a door. Floor and walls are tiled.'''
                }
            },  # do not use item containers yet , just spec cmd
            'item_containers': {
                'pillow': {
                    'd': 'normal thin pillow , moist with sweat. There is something shining sticking from under it',
                    'take': 'under the pillow there is piece of thin wire'
                }
            }
        },
        'under the bed': {
            'once': 'You crawl under the bed, tiles are pressing cold to your chest through the wet pyjamas. you tremble from cold but you managed',
            'd': 'Springs of the bunk bed are just touching your head and shoulders, tiles are pressing cold to your chest',
            'exits': {
                'out': {
                    'to': 'asylum cell',
                    'd':  'you can see your cell floor.'
                }
            }
        },
        'hallway': {
            'once': 'For a while you seen wals pulsating, and swollen with blood',
            'd': 'hallway, corridor with doors, and main door down ',
            'exits': {
                'door': {
                    'to': 'asylum cell',
                    'd': 'wooden door, not locked'
                },
                'east': {
                    'to': 'clearing',
                    'd': 'you can see more light from the distance'
                }
            }
        },
        'staircase': {
            'once': 'You manage to open evacuation doors',
            'd': 'there are stairs here',
            'exits': {
                'door': {
                    'to': 'hallway',
                    'd': 'evacuation door, not locked'
                },
            }

        }
    },
    'hunters': {
        'h1': {
            'init': {
                'speed': 1,
                'noisy': 1,
                'alert': True,
                'hears': True,
                'sees': True,
                'curT': 'asylum cell',
                'sound': 'footsteps',
                'd': 'heavy boots, long cape or duster, male',
                'visual': 'heavy boots'}
        }
    }
}
