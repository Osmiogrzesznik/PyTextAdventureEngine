class Message:

    def __init__(self, d, startRoom):
        """ event-like potentially persistent effect spreading thorugh rooms
            spreading algorithm may help with hunter calculating his next target Room

        d - dictionary with init data:
            typ - sound, light, visual, signal, effect
            start - room
            life = startlife - how long has the effect
            leafnodesaffectedrooms = [startroom]
            !distance is actually affected by properties of the Room
            distance: sum of room distances to pass through
            speed if 0 instantaneous else how many seconds takes to spread
            !REDUNDANT TO typ -conductors: exit/room characteristics that allow to spread through rooms
        startRoom - instantiated Room object
        originator
            """

        self.typ = d['typ']  # - sound, visual, signal, effect
        self.start = startRoom
        self.life = d['startlife']
        self.leafnodesaffectedrooms = [startroom]
        # : sum of room distances to pass through
        self.distance = d['distance']

        # !REDUNDANT TO typ -conductors: exit/room characteristics that allow to spread through rooms
        self.conductors = d['conductors']
        self.speed = d['speed']  # speed if 0 instantaneous
        self.deleteme = False

    def update(self, rooms, map, player, hunters):
        if self.deleteme:
            return 'deleteme'
      """  rooms leading to start originator path


when next room calculated search which ext leads to it"""
        self.life -= 1
        distancemade += 1
        if self.life == 0:
            self.deleteme = True
        return 'deleteme'  # game still has to check all refs to obj in rooms before deleting
        newleafaffectedrooms = []  # new rooms on the boundary of the spreading pool
        for rm in self.leafnodeaffectedrooms:
            if not rm.conducts(typ):
                    continue
                exs = rm.exits
                for ex in exs:
                    if not ex.conducts(typ):
                        continue
                    else:
                        rn = ex.to() #room name
                        
                        get room? how?
                        room.beAffected(slf)
                        newleafaffectedrooms.append(room)
                leafnodesaffectedrooms = newleafaffectedrooms
                if speed > 0 and distancemade < distance:
                return 'i am still spreading in next round'
                elif speed == 0 and distancemade < distance
                return self.update()
