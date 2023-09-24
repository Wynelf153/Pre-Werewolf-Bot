class GameState:
    def __init__(self):
        pass

    def useVote(self, player):
        pass

    def useSkill(self, u, v):
        pass

    def solveVotes(self):
        # Counts village votes, werewolf votes, recruit votes...
        pass

    def solveVisits(self):
        #Resolve visits, change the game state then return deaths, revives and visits
        deaths = None; visits = None
        return deaths, visits