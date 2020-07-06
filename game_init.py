from room_class import *

from utils import *


def removePrepositions(cmdsStr):
    for wrd in [' at ', 'with ', ' using ', ' in ', ' under ', ' on ', ' off ', ' the ', ' a ', ' an ', ' to ', ' along ', ' inside ']:
        cmdsStr = cmdsStr.replace(wrd, ' ')
    return cmdsStr


def isCheckInventory(tks):
    w = ['inventory', 'items', 'pockets', 'backpack']
    return anyWords(w, tks)


def isUseThisOnThat(tks):
    c = tks[0]
    r = isOpen(c) or isUse(c)
    r = r and len(tks) > 2  # only use key door or open door key cases
    return r


def isExamine(cm):
    return cm in ['see', 'examine', 'look', 'check', 'describe', 'investigate', 'search']


def isTake(cm):
    return cm in ['take', 'pick', 'grab']


def isGo(cm):
    return cm in ['go', 'walk', 'climb', ]


def isOpen(cm):
    # move rather here for secret passages
    return cm in ['open', 'unlock', 'pry', 'cut']


def isUse(cm):
    # use and other words may be different in the context of thing they refer to
    # there is a need for checking it and putting it in data dict
    # you need to get all usables/openables in the room and search if there is one of their alts/names in it
    return cm in ['use', 'try', 'turn', 'hit', 'attack',
                  'switch', 'activate', 'pull', 'push', 'move']


def isSpeak(cm):
    return cm in ['speak', 'talk', 'ask', 'questio']


def go_number(strg):
    n = int(strg)
    return n
    return False


def con_I(r0, r1):
    r0.addExit(r1)
    r1.addExit(r0)
    return r0


def con_Y(r0, r1, r2):
    r0.addExit(r1)
    r0.addExit(r2)
    r1.addExit(r0)
    r2.addExit(r0)
    return r0


class Game:

    # how to transform class using input to be async ready to be observing input?
    # end methods on UI.input()
    # start handling on HandleUserInput(msg) being called
    # do not use loop just increase internal index every call of HandleuserInput

    def __init__(self, map, user_interface, prevActions, Entities):
        # TODO separate Player class based on
        # TODO Agent baseclass, able to perform actions as if player would do (pick up items, open doors etc)
        # TODO Agent is steered by input or own ogic gets the world state and performs actions

        # TODO map loading from JSON or different formats
        self.nameOflastObjectConsidered = None
        self.lastCmdsStr = ''
        # for contextual use
        # if user writes just "use wire" after looking at door or keyhole this name is conisdered as object to be acted upon
        # BOOKMARK
        # finish use method,

        self.previousGameplayCommands = []
        # TODO after dying game restarts and the previous commands are added to the voice talking to you

        self.count_time = 0
        self.count_moves = 0
        self.count_enteredCommands = 0

        self.ui = user_interface
        self.rooms = {}
        self.loaded_room = None
        self.map = map
        self.player = {'inventory': {}, 'playerStates': {}, 'worldStates': {}}
        self.hunters = {}
        for i, (name, dict) in enumerate(map['rooms'].items()):
            self.ui.out(name)
            # instead of self.ui this could be a channel for relaying info from Rooms  instead returning
            loaded_room = Room(name, dict, self.ui)
            self.rooms[name] = loaded_room

        start = self.rooms['start']
        start.enterFrom(start)
        previous = start
        self.current = start

    def updateEntities(self):
        pass

    def runTimeEvents(self):
        pass

    def run_OnTurn_Item_Friend_Events(self):
        pass

    def handlePlayerEvents(self, ev):
        # give should have alternative where it works as giveAndRemoveFromRoom
        if 'give' in ev:
            allgiven = ev['give']
            # {'inventory': {}, 'playerStates': {}, 'worldStates': {}}
            for typ in allgiven:
                given = allgiven[typ]
                self.player[typ][given['name']] = given
                if 'rmvSelf' in given:
                    # TODO removeFromPlayer 'take' (for example cured from disease)
                    pass
                self.ui.out('DEBUG:you have now {} in {}'.format(
                    given['name'], typ))

        if 'giveRmv' in ev:
            allgiven = ev['giveRmv']
            # {'inventory': {}, 'playerStates': {}, 'worldStates': {}}
            for typ in allgiven:
                given = allgiven[typ]
            self.player[typ][given['name']] = given
            self.ui.out('DEBUG:you have now {} in {}'.format(
                given['name'], typ))

        if 't' in ev:
            # like when it did something maybe but we need some text result at least, return because there is no need for intepreting
            self.ui.out(ev['t'])

    def handleAllActionEvents(self, ev):
        if 'req' in ev:
            requirement = ev['req']
            playerProp = requirement['playerProp']
            objName = requirement['objName']

            if objName in self.player[playerProp]:
                self.ui.out(ev['reqOK'])
                # TODO run event if there is one

                # TODO aaand what? nothing happens apart from text hint?
                # TODO shouldn't open be part of use?
                # TODO these instead of
                CODE = self.current.runEventOnRoom(ev)
                self.ui.out(
                    'DEBUG:CODE ret from runEventOnRoom in doOpen:' + str(CODE))
                CODE2 = self.handlePlayerEvents(ev)
                self.ui.out(
                    'DEBUG:CODE2 ret from handlePlayerEvents in doOpen:'+str(CODE))
                return
            else:
                self.ui.out(onopen['reqFail'])
                self.ui.out('DEBUG: handleAllActionEvents no event run')
        else:
            # TODO these instead of
            CODE = self.current.runEventOnRoom(ev)
            self.ui.out('DEBUG:CODE ret from runEventOnRoom in doOpen:'+CODE)
            CODE2 = self.handlePlayerEvents(ev)
            self.ui.out(
                'DEBUG:CODE2 ret from handlePlayerEvents in doOpen:'+CODE)

    def doGo(self, tks):
        # TODO take stairs up
        # TODO go stairs up
        # TODO go up (because is removed as preposition)
        # if onexit event
        cmd = tks[0]
        cur = self.current
        exitName = tks[-1]
        ex = cur.getExit(exitName)
        if ex:
            if 'open' in ex:
                if ex['open']:
                    destinationName = ex['to']
                    self.go_room(destinationName, ex)

                elif 'fail' in ex:
                    self.ui.out(ex['fail'])
                    if 'onfail' in ex:
                        # similarly for any open - able objects(is underpillow an opened item container?)
                        # this may need invoke some predefined event handlers f.ex produceSound or similar Trapwires accepting player map
                        evt = ex['onfail']
                        self.player['playerState'][evt['name']] = evt
                    self.ui.out('you couldnt get through')
                    return
            elif 'to' in ex:
                destinationName = ex['to']
                self.go_room(destinationName, ex)
            else:
                raise Exception(
                    'Exit without destination in room:' + cur.name)

        else:
            self.ui.out('there is no {} to {}'.format(tks[-1], tks[0]))
            # getDestinationName should be executed in context of room if i wamt to execute function onExit - like closed or	something

    def doExamine(self, tks):
        cur = self.current
        objName = tks[-1]
        # this shouldnt be here , make method that counts this as referer to room
        desc = cur.getDescription(objName)
        if not desc:
            if objName in ['around', 'room']:
                desc = cur.description
                # TODO replace all self.ui.outs with UI.out(msg)
                self.ui.out(desc)
        else:
            self.ui.out(desc)
        return

    def doTake(self, tks):
        cur = self.current
        objName = tks[-1]
        # this shouldnt be here , make method that counts this as referer to room
        # BOOKMARK there is takeObject method in room class it by default runs events on room

        obinfo = cur.getObjectForCatg('items', objName, True)
        if not obinfo:
            # TODO replace all self.ui.outs with UI.out(msg)
            self.ui.out('cannot take ' + objName)
        else:
            ob = obinfo['ob']
            name = obinfo['key']
            if 'onTake' in ob:
                # if take verb is 'buy' , onTake shoud remove coins from player wallet for example
                self.handleAllActionEvents('onTake')
                # TODO !!!! onTake shouldnt give the same item !!!!
                # this type of events can save some additional info for scoring the game
                # info : did player taken the rose and so on ,and should be default, not explicitly set in map dict
                # TODO BOOKMARK remove object from room items and put into payer inventory
            takenitem = cur.takeObject(name)
            self.player['inventory'][name] = takenitem
            # Bookmark I think i finished doTake TEST IT NOW
        return

    def doOpen(self, tks):
        if isUseThisOnThat(tks):
            self.doUseThisOnThat(tks)
        # 2 ways to open use
        # thing openrd by 'key''
        # key opens doors
        cur = self.current
        objName = tks[-1]
        obj = cur.getObject(objName)
        # hell of a things here wrong
        if obj and 'onopen' in obj:
            # TODO every onSomething ev should be renamed to 'evs'
            onopen = obj['onopen']
            self.handleAllActionEvents(onopen)

        # TODO this logic should be in above runevents

        else:
            self.ui.out('doOpen does not understand:'+str(tks))

    def doUseThisOnThat(self, tks):
        c = tks[0]
        if isOpen(c):
            addresse = 1
            item = 2
        elif isUse(c):
            addresse = 2
            item = 1
        else:
            raise Exception(
                'functidoUseThisOnThaton called on not accurate string wtf? ')
        self.ui.out("tokens:"+str(tks))
        # open doors with key
        # OR
        # use key to open doors
        # OR
        # use key on Doors
        #
        keylikeName = tks[item]
        doorlikeName = tks[addresse]
        self.useInventoryItem(keylikeName, doorlikeName)
        self.ui.out('use:{} on:{}'.format(keylikeName, doorlikeName))

    def playerHas(self, objName):
        obinfo = byKeyOrSubAlt(self.player['inventory'], objName, False)
        return obinfo

    def playerIs(self, statName):

        return byKeyOrSubAlt(self.player['playerStates'], statName, False)

    def useInventoryItem(self, itemName, doorlikeName):

        if not self.playerHas(itemName):
            self.ui.out('I do not have ' + itemName)
            return False
        ii = byKeyOrSubAlt(self.player['inventory'], itemName, False, True)
        i = ii['ob']
        name = ii['key']
        if 'onUse' in i:
            if 'on' in i['onUse']:  # if item use is restricted to certain objects
                on = i['onUse']['on']  # object that we allow to use item on
                if (isinstance(on, list) and doorlikeName in on) or doorlikeName == on:
                    # works like alt in cases of objects
                    # TODO REPLACE all onSomething with 'ev'
                    self.runItemUseEventsAndDecreaseAmount(i, name)
                else:
                    self.ui.out("you cannot use {} on {}".format(
                        name, doorlikeName))
            else:
                # if item use is not restricted
                self.runItemUseEventsAndDecreaseAmount(i, name)
        else:
            self.ui.out("item {} cannot be used this way".format(
                        name, doorlikeName))
            # what does it mean to have item that has no use? :
            # - it still may be required by exits and other things (glasses, coat and so on)

    def runItemUseEventsAndDecreaseAmount(self, i, name):
        # TODO here find out what class of event should be runn ROOM or PLayer if no class try both
        successRoom = self.current.runEventOnRoom(i['onUse'])
        self.handlePlayerEvents(i['onUse'])
        if 'use_amount' in i:
            # there is a difference betweem the amount of item laying in the room
            # and the amount of item in your pocket, if item is reusable,
            # for example there is many mushrooms in forest but you can use it only once
            # there is only one knife found but you can use it many times
            # there is one water bottle but you can use it 3 times
            i['use_amount'] -= 1
            if i['use_amount'] < 1:
                self.ui.out("you no longer have {}".format(name))
                del self.player['inventory'][name]
                # BOOKMARK trying to finish onUse event

    def doUse(self, tks):

        # what about multiword items?
        if len(tks) > 2:
            if isUseThisOnThat(tks):

                # use knife on bread, use key to open door, open door with key
                self.doUseThisOnThat(tks)
    # BOOKMARK trying to figure out what is adresse of item use ,on what
        elif len(tks) == 2:  # two word : use wire
            cur = self.current
            # use lamp light lamp push button use lever
            cmd = tks[0]  # use cmd is already figured out
            objName = tks[-1]
            usedObjInfo = byKeyOrSubAlt(
                self.player['inventory'], objName, False, True)  # this is different
            if usedObjInfo:
                usedObjInfo['typ'] = 'inventory item'
                useInventoryItem(usedObjInfo)
            if not usedObjInfo:
                # than that
                # if no in inventory check for room levers pushes etc.
                usedObjInfo = cur.getObject(objName, False, True)
            # byKeyorSubalt returns {key,ob} and getObject() returns {typ,key,ob}

    def go_room(self, destinationName, ex):

        if not destinationName in self.rooms:
            self.ui.out(
                'seems location that exit leads to doesnt exist in map')
            raise Exception(
                'map location key Error, either no location or worng name: ' + destinationName)
        if 'onExit' in ex:
            effect = self.current.runEventOnRoom(ex['onExit'])

        previous = self.current
        self.current = self.rooms[destinationName]
        self.current.enterFrom(previous)

    def loop_step(self, origcmdsStr):
        cur = self.current

        # try speccmd should remove item from room/container
        cmdsStr = (origcmdsStr + '.')[:-1]  # create copy to manipulate on
        specCmd = self.current.trySpecCmd(
            cmdsStr)  # shd  rename to be trySpecCmd

        if specCmd:
            self.ui.out(
                'DEBUG:specCmd is executed:{}'.format(specCmd))
            if isinstance(specCmd, str):
                cmdsStr = specCmd
            else:
                self.handlePlayerEvents(specCmd)
                return

        if len(cmdsStr.split()) > 2:  # use wire on keyhole
            cmdsStr = removePrepositions(cmdsStr)

        tks = cmdsStr.split()
        cmd = tks[0]  # so go under the bed counts as go bed take the verb 'go'
        # there will be need for separate modular things here
        # dont cram evthing here
        # create comdexecutor or something ?
        # use polymorphism on Room, CmdExector(Room).execCMD(), CMDEXEC(Othertypeofroom).execCMD
        # instead of ifs use methods

        if cmd.isdigit():
            self.ui.out('no more digits')

        if isGo(cmd):
            self.doGo(tks)
        elif isExamine(cmd):
            self.doExamine(tks)
        elif isOpen(cmd):
            if len(tks) > 2 and isUseThisOnThat(tks):  # but first is open
                self.doUseThisOnThat(tks)
            else:
                self.doOpen(tks)
        elif isUse(cmd):
            self.doUse(tks)
        elif isTake(cmd):
            self.doTake(tks)
        else:
            self.ui.out('i do not understand origcmdsStr:{} cmdsStr:{} tks:{}'.format(
                origcmdsStr, cmdsStr, str(tks)))
        self.updateEntities()
        self.runTimeEvents()

    def handleUserInput(self, cmdsStr):
        self.loop_step(cmdsStr)
        self.lastCmdsStr = cmdsStr
        self.count_enteredCommands += 1

    # this could be optional in TestUserInterface module for testing
    def start_console_loop_mode(self, cmdsStr):
        while not self.lastCmdsStr == 'quit':
            origcmdsStr = input('What should i do?').lower()
            self.loop_step(origcmdsStr)
            self.lastCmdsStr = origcmdsStr
