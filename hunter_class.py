from utils import byKey, byKeyOrSubAlt


class Hunter:
    def __init__(self, dict):
        init = dict['init']
        self.curTargetRoom = byKey(init, 'curT', None)
        self.prevTargetRoom = None
        self.alert = False
        # some silent hunters could be made to make noise by leaving puddle of water on their path etc
        self.noisy = byKey(init, 'noisy', False)
        self.cur = init['room']
        self.speed = byKey(init, 'speed', 1)  # not sure
