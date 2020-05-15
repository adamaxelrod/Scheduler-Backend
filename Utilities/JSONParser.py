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
             
    def fetchFullCrewListAsJSON(self):
        fullSchedule = {}
        crewList = ["CORRENTE", "VINOVICH", "BOGER", "CHEFFERS", "BLAKEMAN", "WROLSTAD", "TORBERT", "ALLEN", "HUSSEY", "HOCHULI", "KEMP", "MARTIN", "SMITH", "HILL", "NOVAK", "ROGERS", "CLARK"]
        
        for crew in crewList:
            gameListByCrew = []
            for week in self.gameListByCrew[crew].getSchedule().items():
                game = week[1]
                if (game != Constants.NO_GAME_ASSIGNED and game.getAway() != Constants.WEEK_OFF):
                    gameJson = {"crew": game.getCrew(), "game": game.getAway() + " @ " + game.getHome(), "week": game.getWeek(), "tv": game.getTv(), "primetime": game.getPrimetime(), "notes": game.getNotes()}
                elif (game == Constants.NO_GAME_ASSIGNED):
                     gameJson = {"game": "UNASSIGNED", "week": week[0], "tv": "", "primetime": "", "notes": ""}                      
                else:
                    gameJson = {"game": "OFF", "week": week[0], "tv": "", "primetime": "", "notes": ""}   
                
                gameListByCrew.append(gameJson)
            crewSchedule = { crew : gameListByCrew }
            print(crewSchedule)
            fullSchedule.update(crewSchedule)
            
        return json.dumps(fullSchedule)
  