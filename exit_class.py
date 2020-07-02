class Exit():
    def __init__(self, name, dct):
        self.dct = dct
        self.name = name
        self.description = dct['d']

        self.footprintable = True
        self.hearThrough = True
        self.seeThrough = True
        self.timeCost = 5

        self.to = dct['to']
        if 'alt' in dct:
            self.alt = dct['alt']
        else:
            self.alt = [name]

    def examine(self, player):
        return self.description

    def isalt(self, name):
        """this is not needed since getObjforCatg includes this logic"""
        if name in self.alt:
            return True

    def canGo(self, player):
        print('canGo not implemented yet returns True')
        return True

    def go(self, player, room):
        print('go not implemented yet returns True')
        # this is where dct should contain name of the function or
        # function to fire when player goes
        return self.to
