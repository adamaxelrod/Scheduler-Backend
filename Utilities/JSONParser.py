import json
from Schedule.Game import GameEncoder
from Schedule.Crew import CrewEncoder

class JSONParser(object):
    def __init__(self, gameList, gameListByCrew):
        self.gameList = gameList
        self.gameListByCrew = gameListByCrew

    def fetchWeekAsJSON(self, week):
        return json.dumps(self.gameList[str(week)], cls=GameEncoder)
             
    def fetchCrewAsJSON(self, crewName):
        return json.dumps(self.gameListByCrew[crewName], cls=CrewEncoder)
  