class Player:
    def __init__(self, obj, role):
        self.obj = obj
        self.role = role
        self.alive = True
        self.vote = None

    #Voting
    def getVote(self):
        return self.vote
    
    def updateVote(self, player):
        self.vote = player

    def resetVote(self):
        self.vote = None

    #Action
    def updateAction(self, args):
        return self.role.updateAction()

    def resetAction(self):
        self.role.resetAction()

