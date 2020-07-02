class UserInterface:
    def __init__(self):
        self.last_input = None
        self.userInputHandler = None

    def out(self, msg):
        print(msg)

    def input(self, msg):
        self.last_input = input(msg)
        self.onUserInput(self.last_input)

    def addOnUserInputListener(self, userInputHandler):
        self.userInputHandler = userInputHandler

    def onUserInput(self, inputMsg):
        if self.userInputHandler is None:
            return
        self.userInputHandler.handleUserInput(inputMsg)


class testUserInterface(UserInterface):
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
        print(msg)

    def onUserInput(self, inputMsg):
        if self.userInputHandler is None:
            return
        self.userInputHandler.handleUserInput(
            inputMsg)  # Game_object.handleUserInput()
