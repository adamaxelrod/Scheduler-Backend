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
    def __init__(self) -> None:
        self.crewStore = self.loadCrews()
        self.gameStore = self.loadGames()
        self.processSchedule()
        #self.runTest()


    """ tester """ 
    def runTest(self) -> None:
        #self.printGamesForCrew("HOCHULI")
        #self.printGamesForCrew("CORRENTE")
        # self.printGamesForWeek(1)
        # self.printGamesForWeek(8)
        # self.printGamesForWeek(17)
        self.printAllCrews()


    """ Print all crews test function """ 
    def printAllCrews(self) -> None:
        with open(Constants.SCHEDULE_OUTPUT, 'w') as f:
            for key in self.getCrews().keys():
                schedule = self.getCrews()[key].getSchedule()
                gameList = ""
                for i in range(1, 18):
                    game = schedule[str(i)]
                    if (game != None and game != Constants.NO_GAME_ASSIGNED and game.getAway() != Constants.WEEK_OFF):
                        if (game.getPrimetime() != None):                            
                            gameList = gameList + game.getAway() + " @ " + game.getHome() + " " + game.getPrimetime() + ","
                        else:
                            gameList = gameList + game.getAway() + " @ " + game.getHome() + ","
                    elif (game == Constants.NO_GAME_ASSIGNED):
                        gameList = gameList + "UNASSIGNED,"
                    elif (game.getAway() == Constants.WEEK_OFF):
                        gameList = gameList + "OFF,"
                f.write("%s,%s\n"%(key, gameList))
        
        
    """ Print all games for week test function """ 
    def printGamesForWeek(self, week) -> None:
        weekGames = self.getGames()[str(week)]
        crewList = {}
        for game in weekGames:
            print("{} @ {} {} - {}".format(game.getAway(), game.getHome(), game.getNotes(), game.getCrew()))
            if (game.getCrew() not in crewList):
                crewList[game.getCrew()] = 1
            else:
                crewList[game.getCrew()] = crewList[game.getCrew()] + 1
        print ("Crew List: {}".format(crewList))


    """ Print all games for crew test function """
    def printGamesForCrew(self, crewName) -> None:
        crewSchedule = self.getCrews()[crewName].getSchedule()

        for i in range(1, 18):
            game = crewSchedule[str(i)]
            if (game != None and game != Constants.NO_GAME_ASSIGNED and game.getAway() != Constants.WEEK_OFF):
                print("W{} {} @ {} {}".format(game.getWeek(), game.getAway(), game.getHome(), game.getNotes()))
            elif (game != Constants.NO_GAME_ASSIGNED):
                print("W{} UNASSIGNED".format(i))
            else:
                print ("W{} OFF".format(i))

        print("Total Primetime: {}".format(self.getCrews()[crewName].getPrimetime()))
        print("Total Games by Team: {}".format(self.getCrews()[crewName].getHomeCount()))


    def loadCrews(self) -> CrewInfo.CrewInfo:
        return CrewInfo.CrewInfo()
        

    def loadGames(self) -> GameInfo.GameInfo:
        return GameInfo.GameInfo()


    def getGames(self):
        return self.gameStore.getGames()


    def getCrews(self):
        return self.crewStore.getCrews()


    def getRandomCrewList(self):
        crewList = list(self.getCrews())
        random.shuffle(crewList)
        return crewList


    """ Main scheduling algorithm """
    def processSchedule(self) -> None:
        # Iterate through all weeks of the season
        for i in range(1, Constants.FULL_SEASON+1):
            week = i
            primetimeGames = self.gameStore.getPrimetimeGamesForWeek(week)
            nonPrimetimeGames = self.gameStore.getNonPrimetimeGamesForWeek(week)
            totalGamesForWeek = len(primetimeGames) + len(nonPrimetimeGames)
            
            # Randomize the list of crews for each week to ensure random assignments
            crewList = self.getRandomCrewList()
            unassignedGameList = []
            offList = []
            crewName = ""

            # Assign off weeks first
            for j in range(0, Constants.MAX_GAMES_PER_WEEK - totalGamesForWeek + 1):
                crewName = self.findBestOffCrew(crewList, week)
                
                if (crewName != Constants.NO_GAME_ASSIGNED):                   
                    self.updateCrewSchedule(crewName, week, None)      
                    crewList.remove(crewName)
                    offList.append(crewName)
                    
            print("W{} OFF for {}". format(week, offList))
             
            # Assign primetime games
            for game in primetimeGames:
                crewName = self.findBestCrew(crewList, game.getWeek(), game.getAway(), game.getHome(), game.getPrimetime())
                
                if (crewName == Constants.NO_GAME_ASSIGNED):
                    unassignedGameList.append(game)
                else:
                    #print("W{} {} ASSIGNING {} @ {} -  {} - PRIME".format(week, game.getWeek(), game.getAway(), game.getHome(), crewName))
                    self.updateCrewSchedule(crewName, week, game)                   
                    crewList.remove(crewName)                   
 
            # Assign non-primetime games last
            for game in nonPrimetimeGames:
                crewName = self.findBestCrew(crewList, game.getWeek(), game.getAway(), game.getHome())
                
                if (crewName == Constants.NO_GAME_ASSIGNED):
                    unassignedGameList.append(game)
                else:
                    #print("W{} {} ASSIGNING {} @ {} -  {}".format(week, game.getWeek(), game.getAway(), game.getHome(), crewName))              
                    self.updateCrewSchedule(crewName, week, game) 
                    crewList.remove(crewName)

            # Find assignment for any unassigned games
            print("W{} UNASSIGNED CREWS: {}".format(week, crewList))
            for game in unassignedGameList:
                print("W{} LOOKING TO ASSIGN: {} @ {} - {}".format(game.getWeek(), game.getAway(), game.getHome(), game.getPrimetime()))

                for crew in crewList:
                    crewName = self.findBestCrewAndSwap(crew, game)
                    if (crewName == Constants.NO_GAME_ASSIGNED):
                        print("COULDNT SWAP WITH: {}".format(crew))                        
                    else:
                        crewList.remove(crew)
                        break

            for crew in crewList:
                print("======== W{} - NO ASSIGNMENT FOR: {} ({})".format(week, crew, self.getCrews()[crew].getTotalOff()))

 
    def findBestCrewAndSwap(self, inputCrew, game):
        crewList = self.getRandomCrewList()
        for crew in crewList:
            if (crew != inputCrew and self.getCrews()[crew].isCrewOff(game.getWeek()) == False):      
                #Temporarily remove from schedule to attempt swap
                removedGame = self.getCrews()[crew].removeGameFromSchedule(game.getWeek())                
                if (removedGame != None and removedGame != Constants.NO_GAME_ASSIGNED):
                    inputCrewRanking = self.getCrews()[inputCrew].getRanking(removedGame.getWeek(), removedGame.getAway(), removedGame.getHome(), removedGame.getPrimetime())                    

                    if (inputCrewRanking != Constants.NOT_ALLOWED):
                        iterCrewRanking = self.getCrews()[crew].getRanking(game.getWeek(), game.getAway(), game.getHome(), game.getPrimetime() if game.getPrimetime() != None else None) 
                        if (iterCrewRanking != Constants.NOT_ALLOWED):
                            self.updateCrewSchedule(crew, game.getWeek(), game)
                            self.updateCrewSchedule(inputCrew, removedGame.getWeek(), removedGame)
                            print(" *** SWAPPED: {} with {}".format(inputCrew, crew))
                            return crew

                    self.updateCrewSchedule(crew, removedGame.getWeek(), removedGame)
        return Constants.NO_GAME_ASSIGNED
    

    """ Determine the best off crew for the game """       
    def findBestOffCrew(self, crewList, week):
        # Iterate through each crew and determine their ranking for this game
        for crew in crewList:
            if (self.getCrews()[crew].isDueForOff(week) == True):
                return crew
        return Constants.NO_GAME_ASSIGNED        


    """ Determine the best crew for the game """       
    def findBestCrew(self, crewList, week, away, home, primetime=None):
        rankingCategories = {Constants.NOT_ALLOWED: [], Constants.MIN_RANKING: [], Constants.LOW_RANKING: [], Constants.MED_RANKING: [], Constants.HIGH_RANKING: [], Constants.MAX_RANKING: []}
        # Iterate through each crew and determine their ranking for this game
        for crew in crewList:
            ranking = self.getCrews()[crew].getRanking(week, away, home, primetime)
            rankingCategories[ranking].append(crew)
        return self.getBestRanking(rankingCategories) 


    """ Find highest ranked crew for this game """
    def getBestRanking(self, rankings):
        if (rankings[Constants.MAX_RANKING] != []):
            return rankings[Constants.MAX_RANKING][0]
        elif(rankings[Constants.HIGH_RANKING] != []):
            return rankings[Constants.HIGH_RANKING][0]
        elif(rankings[Constants.MED_RANKING] != []):
            return rankings[Constants.MED_RANKING][0]
        elif(rankings[Constants.LOW_RANKING] != []):
            return rankings[Constants.LOW_RANKING][0]    
        elif(rankings[Constants.MIN_RANKING] != []):
            return rankings[Constants.MIN_RANKING][0]
        else:
            return Constants.NO_GAME_ASSIGNED
        
        
    """ Assign game to crew and update data store """
    def updateCrewSchedule(self, crewName, week, game) -> None:
        if (crewName != None and game != None):
            self.crewStore.updateCrew(crewName, game)
            self.gameStore.updateGame(game.getWeek(), game, crewName)
        else:
            self.crewStore.assignOff(crewName, week)