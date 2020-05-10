import json
import csv
import boto3
import random
import Utilities.Constants as Constants
import Schedule.CrewInfo as CrewInfo
import Schedule.GameInfo as GameInfo
import Schedule.Game as Game
from boto3.dynamodb.conditions import Key, Attr


class Schedule(object):
    def __init__(self):
        self.crewStore = self.loadCrews()
        self.gameStore = self.loadGames()
        self.processSchedule()
        self.runTest()


    def runTest(self):
       # self.printGamesForCrew("HOCHULI")
       # self.printGamesForCrew("CORRENTE")
       # self.printGamesForWeek(1)
       # self.printGamesForWeek(8)
       # self.printGamesForWeek(17)
        self.printAllCrews()


    def printAllCrews(self):
        with open(Constants.SCHEDULE_OUTPUT, 'w') as f:
            for key in self.getCrews().keys():
                schedule = self.getCrews()[key].getSchedule()
                gameList = ""
                for i in range(1, 18):
                    game = schedule[str(i)]
                    if (game != None and game != Constants.NO_GAME_ASSIGNED):
                        if (game.getPrimetime() != None):                            
                            gameList = gameList + game.getAway() + " @ " + game.getHome() + " " + game.getPrimetime() + ","
                        else:
                            gameList = gameList + game.getAway() + " @ " + game.getHome() + ","
                    else:
                        gameList = gameList + "OFF,"
                f.write("%s,%s\n"%(key, gameList))
        

    def printGamesForWeek(self, week):
        weekGames = self.getGames()[str(week)]
        crewList = {}
        for game in weekGames:
            print("{} @ {} {} - {}".format(game.getAway(), game.getHome(), game.getNotes(), game.getCrew()))
            if (game.getCrew() not in crewList):
                crewList[game.getCrew()] = 1
            else:
                crewList[game.getCrew()] = crewList[game.getCrew()] + 1
        print ("Crew List: {}".format(crewList))


    def printGamesForCrew(self, crewName):
        crewSchedule = self.getCrews()[crewName].getSchedule()

        for i in range(1, 18):
            game = crewSchedule[str(i)]
            if (game != None and game != Constants.NO_GAME_ASSIGNED):
                print("W{} {} @ {} {}".format(game.getWeek(), game.getAway(), game.getHome(), game.getNotes()))
            else:
                print ("W{} OFF".format(i))

        print("Total Primetime: {}".format(self.getCrews()[crewName].getPrimetime()))
        print("Total Games by Team: {}".format(self.getCrews()[crewName].getHomeCount()))


    def loadCrews(self):
        return CrewInfo.CrewInfo()
        

    def loadGames(self):
        return GameInfo.GameInfo()


    def getGames(self):
        return self.gameStore.getGames()


    def getCrews(self):
        return self.crewStore.getCrews()


    def getRandomCrewList(self):
        crewList = list(self.getCrews())
        random.shuffle(crewList)
        return crewList


    def processSchedule(self):
        for i in range(1, 18):
            primetimeGames = self.gameStore.getPrimetimeGamesForWeek(i)
            nonPrimetimeGames = self.gameStore.getNonPrimetimeGamesForWeek(i)
            crewList = self.getRandomCrewList()
            unassignedGameList = []
            crewName = ""

            # Assign primetime games first
            for game in primetimeGames:
                crewName = self.findBestCrew(game.getWeek(), game.getAway(), game.getHome(), game.getPrimetime())
                if (crewName == Constants.NO_GAME_ASSIGNED):
                    unassignedGameList.append(game)
                else:
                    self.updateCrewSchedule(crewName, game) 
                    #crewList.pop(crewName)                   
 
            # Assign non-primetime games next
            for game in nonPrimetimeGames:
                crewName = self.findBestCrew(game.getWeek(), game.getAway(), game.getHome())
                if (crewName == Constants.NO_GAME_ASSIGNED):
                    unassignedGameList.append(game)
                else:
                    self.updateCrewSchedule(crewName, game) 
                    #crewList.pop(crewName)

            #TODO - find assignment for any unassigned games
            for game in unassignedGameList:
                print("CANT ASSIGN: W{} {} @ {} - {}".format(game.getWeek(), game.getAway(), game.getHome(), game.getPrimetime()))

          #  for crew in crewList:
          #      self.updateCrewSchedule(crewName, None)


    def updateCrewSchedule(self, crewName, game):
        if (crewName != None):
            self.crewStore.updateCrew(crewName, game)
            self.gameStore.updateGame(game.getWeek(), game, crewName)
       # else:
        #    self.crewStore.assignOff(crewName)

        
    def findBestCrew(self, week, away, home, primetime=None):
        crewList = self.getRandomCrewList()
        rankings = {Constants.MIN_RANKING: [], Constants.LOW_RANKING: [], Constants.MED_RANKING: [], Constants.HIGH_RANKING: [], Constants.MAX_RANKING: []}
 
        for crew in crewList:
            ranking = self.getCrews()[crew].getRanking(week, away, home, primetime)
            if (ranking != Constants.NOT_ALLOWED):
                rankings[ranking].append(crew)
        return self.parseRankings(rankings) 


    def parseRankings(self, rankings):
        if (rankings[Constants.MAX_RANKING] != []):
            return rankings[Constants.MAX_RANKING][0]
        elif(rankings[Constants.HIGH_RANKING] != []):
            return rankings[Constants.HIGH_RANKING][0]
        elif(rankings[Constants.MED_RANKING] != []):
            return rankings[Constants.HIGH_RANKING][0]
        elif(rankings[Constants.LOW_RANKING] != []):
            return rankings[Constants.LOW_RANKING][0]    
        elif(rankings[Constants.MIN_RANKING] != []):
            return rankings[Constants.MIN_RANKING][0]
        else:           
            return Constants.NO_GAME_ASSIGNED