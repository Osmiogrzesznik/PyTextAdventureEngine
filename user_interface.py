class ConsoleUserInterface:
    def __init__(self):
        self.last_input = None
        self.userInputHandler = None

    def out(self, msg):
        print(msg)

    def input(self, msg):
        self.onUserInputRequested(msg)
        self.onUserInput(self.last_input)

    def onUserInputRequested(self, msg):
        self.out(msg)
        self.last_input = input()

    def addOnUserInputListener(self, userInputHandler):
        self.userInputHandler = userInputHandler

    def onUserInput(self, inputMsg):
        if self.userInputHandler is None:
            return
        self.userInputHandler.handleUserInput(inputMsg)


class TestUserInterface(ConsoleUserInterface):
    def __init__(self):
        self.last_input = None
        self.userInputHandler = None

    def out(self, msg):
        print(msg)

    def input(self, msg):
        self.onUserInputRequested(msg)

    def addOnUserInputListener(self, userInputHandler):
        self.userInputHandler = userInputHandler

    def onUserInputRequested(self, msg):
        self.out(msg)

    def onUserInput(self, inputMsg):
        if self.userInputHandler is None:
            return
        self.userInputHandler.handleUserInput(
            inputMsg)  # Game_object.handleUserInput()


class TestUserInterfaceBuffered(TestUserInterface):
    def __init__(self):
        self.last_input = None
        self.userInputHandler = None
        self.last_output = None

    def out(self, msg):
        self.last_output = msg

    def input(self, msg):
        self.onUserInputRequested(msg)

    def addOnUserInputListener(self, userInputHandler):
        self.userInputHandler = userInputHandler

    def onUserInputRequested(self, msg):
        self.out(msg)

    def onUserInput(self, inputMsg):
        if self.userInputHandler is None:
            return
        self.userInputHandler.handleUserInput(
            inputMsg)  # Game_object.handleUserInput()
