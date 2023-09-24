from datetime import datetime

class GameClock:
    def __init__(self):
        self._start = datetime.timestamp(datetime.now())
