from player import Player

#TODO: Add talksto handling in gameWrapper class

VILLAGE = 'village'
WEREWOLF = 'werewolf'

class GameState:
    def __init__(self, players, roles):

        self._playerId2Class = {player.id: Player(player, role) for player, role in zip(players, roles)}

        self._players = list(self._playerId2Class.values())

        self.day = 0
        self.isDay = True

        self.ended    = False

        #Voter id: Voted id
        self.votes = {}

    def resolveDay(self):
        voteDict = self._getCount(self._votes)
        if voteDict:
            maxVotes = max(voteDict.values())
        else:
            maxVotes = 0

        lynchTargets = [target for target in voteDict.keys() if voteDict[target] == maxVotes]
        #Kill lynch target
        if len(lynchTargets) == 1 and maxVotes != 0:
            target = self._playerId2Class[lynchTargets[0]]
            target.alive = False
            return target.obj
        else:
            return None

    def resetVotes(self):
        self._votes = {}

    def resolveNight(self):
        visits = []

        lastWerewolfVote = None
        werewolfAttacks = []

        for playerClass in self._players:
            role = playerClass.role

            if role.alignment() == WEREWOLF:
                if lastWerewolfVote == None or lastWerewolfVote < role.killTimestamp:
                    lastWerewolfVote = role.killTimestamp

                    werewolfKiller  = playerClass
                    werewolfKill    = role.killVote

        #Visits
        if not lastWerewolfVote:
            visits.append((werewolfKiller, werewolfKill))
            werewolfAttacks.append(werewolfKill)

        kills = []; revives = []
        #Kills
        for victim in werewolfAttacks:
            victimPlayerClass = self._playerId2Class[victim.id]
            victimPlayerClass.alive = False
            kills.append(victimPlayerClass.obj)
        return kills, revives

    def parityCheck(self):
        ret = self.getParity()
        self.ended = ret
        return ret
    
    def resetActions(self):
        for playerClass in self._players:
            playerClass.resetAction()

    #Helper functions


    def getParity(self):
        parityDict = {}
        for playerClass in self._players:
            alignment = playerClass.role.alignment()
            parityDict[alignment] = parityDict.get(alignment, 0) + 1
        if len(parityDict.keys()) == 1:
            return True
        elif len(parityDict.keys()) == 2:
            if VILLAGE in parityDict.keys():
                evilFaction = [faction for faction in parityDict.keys if faction != VILLAGE][0]
                return parityDict[evilFaction] >= parityDict[VILLAGE]
            else:
                return False
        else:
            return False

    def endPhase(self):
        if self.isDay:
            self.isDay = False
        else:
            self.isDay = True
            self.day += 1

    def _getCount(self, votes):
        ret = {}
        for voted in votes.values():
            ret[voted.id] = ret.get(voted.id, 0) + 1
        return ret

    def _getWolves(self):
        return [playerClass for playerClass in self._players if playerClass.role.alignment == WEREWOLF]

    #Helper function for other classes usage

    def getTown(self):
        return [playerClass for playerClass in self._players if playerClass.alive]

    def getGraveyard(self):
        return self._players
            
    def getFactionPrefix(self, alignment):
        if alignment == 'village':
            return ([], '')
        elif alignment == 'wolf':
            return (self._getWolves(), '(To the werewolves) ')

    def getPlayerClass(self, queryPlayer):
        return self._playerId2Class[queryPlayer.id]

    def getRole(self, queryPlayer):
        return self.getPlayerClass(queryPlayer).role
    
    def getAlignment(self, queryPlayer):
        return self.getRole(queryPlayer).alignment()

    



    


