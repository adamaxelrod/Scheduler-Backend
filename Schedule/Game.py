import json
from json import JSONEncoder
from typing import Any, Dict, Optional

import Utilities.Constants as Constants

class Game(object):
    def __init__(self, week, away=None, home=None, tv=None, notes=None) -> None:
        self.week = week
        self.away = away
        self.home = home
        self.tv = tv
        self.notes = notes
        self.primetime = self.getPrimetime()
        self.crew = None

    def getAway(self):
        return self.away

    def getHome(self):
        return self.home

    def getWeek(self):
        return self.week

    def getTv(self):
        return self.tv

    def getPrimetime(self) -> Optional[str]:
        if (self.notes == Constants.SNF):
            return Constants.SNF
        elif (self.notes == Constants.MNF):
            return Constants.MNF
        elif (self.notes == Constants.THNF):
            return Constants.THNF           
        return None

    def getNotes(self) -> str:
        return " (" + self.notes + ")" if self.notes != 'N/A' else ''

    def setCrew(self, crew) -> None:
        self.crew = crew

    def getCrew(self):
        return self.crew

    def isEmpty(self) -> bool:
        return True if (self.home == Constants.WEEK_OFF or self.away == Constants.WEEK_OFF) else False

    def printGame(self) -> None:
        print("W{} - {} @ {}".format(self.getWeek(), self.getAway(), self.getHome()))

class GameEncoder(JSONEncoder):
        def default(self, o) -> Dict[str, Any]:
            return o.__dict__