import json
import Utilities.Constants as Constants
from Schedule.Game import GameEncoder
from Schedule.Crew import CrewEncoder

class JSONParser(object):
    def __init__(self, gameList, gameListByCrew):
        self.gameList = gameList
        self.gameListByCrew = gameListByCrew

    def fetchWeekAsJSON(self, week):
        return json.dumps(self.gameList[str(week)], cls=GameEncoder, indent=4)
             
    def fetchCrewAsJSON(self, crewName):
        gameList = []
        for week in self.gameListByCrew[crewName].getSchedule().items():
            game = week[1]
            if (game != Constants.NO_GAME_ASSIGNED):
                gameJson = {"game": game.getAway() + " @ " + game.getHome(), "week": game.getWeek(), "tv": game.getTv(), "primetime": game.getPrimetime()}
            else:
                gameJson = {"game": "OFF", "week": week[0], "tv": "", "primetime": ""}   
            
            gameList.append(gameJson)

        return json.dumps(gameList)
  