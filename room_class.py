from utils import byKey, byKeyOrSubAlt
from exit_class import Exit

NO_OBJECT_IN_ROOM = 404


class Room:

    def __init__(self, name, dct, ui):  # ui shouldnt be here, separation of concerns
        self.name = name
        self.ui = ui
        self.exits = []
        self.dct = dct
        self.description = dct['d']
        self.once = byKey(dct, 'once', False)
        self.was_entered = False
        self.typ = byKey(dct, 'typ', 'real')
        self.conducts = byKey(dct, 'conducts', ['light,sound'])

        if 'exits' in dct:
            for exno, (exname, exdict) in enumerate(dct['exits'].items()):
                self.ui.out("adding exit :" + exname)
                exdict['name'] = exname
                self.addExit(exname, exdict)
        self.entrance = None

    def conducts(self, typ):
        return typ in self.conducts

    def beAffected(self, effectmsgob):

        self.subscribers.notify(self, effectmsgob)
        ''' who is in the room
        could adjoining rooms be subscribers to neighbours'''

    def runEventOnRoom(self, ev):
        if 'targetRoom' in 'ev' and self.name != ev['targetRoom']:
            self.ui.out(
                'RoomEvent: this cannot happen in here cannot use it in here. use it in '+ev['targetRoom'])
        if 'add' in ev:
            add = ev['add']
            for typ in add:
                # have effect on accessible room data
                # ['exits', 'item_containers','items', 'objects', 'switches', 'ds', 'links']
                obToAddToTyp = add[typ]
                self.dct[typ][obToAddToTyp['name']] = obToAddToTyp
                # for example add item to items
                # problem with exits - they are objects and stored in the array
            # return {'t': ev['t']}  # return text feedback on what happened
        if 'addToDesc' in ev:
            self.dct['d'] += '\n' + ev['addToDesc']
        if 'changeDesc' in ev:
            self.dct['d'] = 'Previously:' + \
                self.dct + 'now:' + ev['changeDesc']
        if 'change' in ev:
            # TODO think about generalising this logic,
            # if ev['evtypname'} is instance of list loop through it with the function as teh paramater
            #  else execute function on ev['evtypname'] itself
            changes = ev['change']
            if not isinstance(changes, list):
                results = self.runChangeEvent(changes)
            else:
                results = []
                for change in changes:
                    result = self.runChangeEvent(change)
                    results.append(result)
        # BOOKMARK trying to finish use functionality

        # should return false or success  and text reason why or text
        # feedback on success
        return ev  # let game logic to handle player given items, statuses

    def runChangeEvent(self, change):
        objName = change['objName']
        propName = change['prop']
        newValue = change['val']
        obinfo = self.getObject(objName, True)

        if not obinfo:
            self.ui.out('cannot find {} object in {} room'.format(
                objName, self.name))
            return NO_OBJECT_IN_ROOM
        ob = obinfo['ob']
        obName = obinfo['key']
        obTyp = obinfo['typ']

        if not propName in ob:
            m = 'cannot find {} prop in {} object'.format(
                propName, objName)
            self.ui.out(m)
            raise Exception(m)
        # check on source data just in case of not mutable stuff
        elif self.dct[obTyp][obName][propName] == change['val']:
            self.ui.out('{} property in {} object is already equal to {}'.format(
                propName, objName, change['val']))
        else:
            # change

            property_to_change = ob[propName]
            # it doesnt work  with returned objects ? because there is no pointers in ppython
            # Solution: change source data just in case of not mutable stuff
            self.dct[obTyp][obName][propName] = newValue

            # TODO THIS DOESNT WORK ?!!!
            self.ui.out("runChangeEvent RESULT: " + change['t'])
            return change['t']

    def trySpecCmd(self, cm):
        if 'cmds' in self.dct:
            cmd = byKeyOrSubAlt(self.dct['cmds'], cm, False)
            if not cmd:
                return False
            else:
                if 'do' in cmd:  # do serves as handy synonym for other commands
                    # do is for weird cases only 'do' commands should lead to effects themselves
                    return cmd['do']
                # ! TODO all below (add, addtoDesc )
                # should be factored out to Effect and executed always when any action results in effect on room
                # add and addToDesc may happen always and independently of outcome
                if 'add' in cmd:  # this should be onExec or onSpecCmd RoomEvent
                    add = cmd['add']
                    for typ in add:
                        # should i have some way to determine if event works on player or Room or just run it on both and see?
                        # if typ == 'eventClass':
                        #     eventClass = add[typ]
                        #     if eventClass == 'room':

                        # have effect on accessible room data
                        # ['exits', 'item_containers','items', 'objects', 'switches', 'ds', 'links']
                        obToAddToTyp = add[typ]
                        self.dct[typ][obToAddToTyp['name']] = obToAddToTyp
                        # for example add item to items
                        # problem with exits - they are objects and stored in the array
                        # return text feedback on what happened
                        return {'t': cmd['t']}
                if 'addToDesc' in cmd:
                    self.dct['d'] += '\n' + cmd['addToDesc']
                if 'give' in cmd:
                    return cmd  # let game logic to handle player given items, statuses
        return False

    def takeObject(self, objName):
        obinfo = self.getObject(objName, True)
        if not obinfo:
            self.ui.out('there is no {} here'.format(objName))
            return False
        ob = obinfo['ob']
        if 'amount' in ob and ob['amount'] > 1:
            ob['amount'] -= 1
        else:
            self.ui.out('no more {} left'.format(obinfo['key']))
            objects_dct_ofTyp = self.dct[obinfo['typ']]
            taken_object = objects_dct_ofTyp.pop(obinfo['key'])
            return taken_object

    def getObject(self, objName, rettypandkey=False):
        typs = ['exits', 'item_containers',
                'items', 'objects', 'switches', 'ds', 'links']
        if len(objName.split()) > 1:
            self.ui.out('multiword!!! TODO')
            # TODO when searching
        for typ in typs:
            if typ in self.dct:
                d = self.getObjectForCatg(typ, objName, rettypandkey)
                if not d:
                    continue
                else:
                    if rettypandkey:
                        d['typ'] = typ
                    return d
            else:  # if no above specified typ in current
                continue
        # if loop finished not finding object
        return False
        # TODO no object in data, game-init or this function should check if the word is mentioned in room description or other descriptions and say that it is "not interesting"

    def getDescription(self, objName):
        obj = self.getObject(objName)
        if obj:
            # there should be check canDescribe
            if 'd' in obj:
                return obj['d']
            elif 'noDesc' in self.dct:
                return self.dct['noDesc']
            else:
                # each room should had its own default none response
                # if no description of object but it exists
                return "just normal " + objName
        else:
            # WAS: return 'nothing interesting about that or it doesnt exist here'
            # LEAD TO BUG : couldn't determine in game logic if 'around' exists and default to Room desc
            return False  # let game logic handle that

    def getObjectForCatg(self, cat, objName, retkey=False):
        if not cat in self.dct:
            return False
        ret = byKeyOrSubAlt(self.dct[cat], objName, False, retkey)
        # ret may have ob prop but here doesnt matter
        if ret:

            return ret
            # each room should had its own default none response
        elif 'noObj' in self.dct:
            ret = self.dct['noObj']  # should be string only
        else:
            ret = False
            # what about alts?

    def enterFrom(self, entrance=False):
        if not self.was_entered:
            self.ui.out(self.once)
            self.was_entered = True
            # TODO onEnter event resetting ghost in ActionCastle duncgeons
        self.ui.out(self.description)
        self.ui.out('EXITS:')
        if 'exits' in self.dct:
            for exkey in self.dct['exits']:
                ex = self.dct['exits'][exkey]
                if not 'hidden' in ex:
                    self.ui.out(exkey)

        if entrance:
            self.entrance = entrance
            # self.ui.out(self.name)

            # self.ui.out("      0: back to location " + entrance.name)
        # for exno, ex in enumerate(self.exits):
            # self.ui.out("       "+str(exno+1) + ":" +
            #       ex.name + " DEBUG: " + str(ex.dict))
        return self

    def addExit(self, exitname, exitdict):
        exit = Exit(exitname, exitdict)
        self.exits.append(exit)

    def getExit(self, exitname):
        ex = self.getObjectForCatg('exits', exitname)
        return ex
