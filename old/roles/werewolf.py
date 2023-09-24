from roleInterface import Role

class Werewolf(Role):
    def __init__(self):
        self.killVote = None
        self.killTimestamp = None

    def alignment(self):
        return 'wolf'
    
    def updateDayAction(self, args):
        return None

    def updateNightAction(self, args):
        self.killVote = args[0]
        return

    def resetAction(self):
        self.killVote = None
        self.killTimestamp = None