from roleInterface import Role

class Villager(Role):
    def alignment(self):
        return 'village'
    
    def updateDayAction(self, args):
        return None

    def updateNightAction(self, args):
        return None
    
    def resetAction(self):
        pass
