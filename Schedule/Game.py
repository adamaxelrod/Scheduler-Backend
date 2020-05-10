import json
from json import JSONEncoder
import Utilities.Constants as Constants

class Game(object):
    def __init__(self, week, away, home, tv, notes):
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

    def getPrimetime(self):
        if (self.notes == Constants.SNF):
            return Constants.SNF
        elif (self.notes == Constants.MNF):
            return Constants.MNF
        elif (self.notes == Constants.THNF):
            return Constants.THNF           
        return None

    def getNotes(self):
        return " (" + self.notes + ")" if self.notes != 'N/A' else ''

    def setCrew(self, crew):
        self.crew = crew

    def getCrew(self):
        return self.crew

    def printGame(self):
        print("W{} - {} @ {}".format(self.getWeek(), self.getAway(), self.getHome()))

class GameEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__