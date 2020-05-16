import json
from json import JSONEncoder
import Schedule.Game as Game
import Utilities.Constants as Constants

class Crew(object):
    def __init__(self, name, region, rules):
        self.crewName = name
        self.region = region
        self.rules = json.loads(rules)
        self.primetime = {"SNF": 0, "MNF": 0, "THNF": 0}
        self.totalOff = 0
        self.schedule = self.initializeSchedule()
        self.homeCount = self.initializeTeamList()
        self.awayCount = self.initializeTeamList()


    """ intialize schedule information """
    def initializeSchedule(self):
        schedule = {}
        for i in range(1, 18):
            schedule[str(i)] = Constants.NO_GAME_ASSIGNED
        return schedule


    """ intialize team list """
    def initializeTeamList(self):
        teamList = {}
        for team in Constants.ALL_TEAMS:
            teamList[team] = 0
        return teamList


    """ get home count """
    def getHomeCount(self):
        return self.homeCount


    """ get away count """
    def getAwayCount(self):
        return self.awayCount


    """ get crew name """
    def getCrewName(self):
        return self.crewName


    """ get region """
    def getRegion(self):
        return self.region


    """ get schedule """
    def getSchedule(self):
        return self.schedule


    """ get primetime status """
    def getPrimetime(self):
        return self.primetime
    
    
    """ get total off weeks assigned """
    def getTotalOff(self):
        return self.totalOff


    """ check if primetime games are allowed for this crew """
    def isPrimetimeAllowed(self, primetime):
        primetimeStr = primetime.lower() + "Allowed"
        if (self.rules[primetimeStr] == "true"):
            return True
        else:
            return False

    """ check if extra primetime games are allowed for this crew """
    def isExtraPrimetimeAllowed(self):
        extraPrimetimeStr = "multipleAllowed"
        if (extraPrimetimeStr in self.rules and self.rules[extraPrimetimeStr] == "true"):
            return True
        else:
            return False


    def hadRecentPrimetime(self, week, threshold):
        if (int(week) > 1):
            lowerBound = int(week) - threshold if (int(week) - threshold > 0) else 1
            upperBound = int(week)
            for prev in range(lowerBound, upperBound):
                if (str(prev) in self.schedule and self.schedule[str(prev)] != Constants.NO_GAME_ASSIGNED):
                    if (self.schedule[str(prev)].getPrimetime() != None):
                        return True
        return False
                        
        
    def addGameToSchedule(self, game):
        self.schedule[str(game.getWeek())] = game
        self.homeCount[game.getHome()] = self.homeCount[game.getHome()] + 1
        self.awayCount[game.getAway()] = self.awayCount[game.getAway()] + 1
        if (game.getPrimetime() == Constants.SNF):
            self.primetime[Constants.SNF] +=1
        elif(game.getPrimetime() == Constants.MNF):
            self.primetime[Constants.MNF] +=1
        elif(game.getPrimetime() == Constants.THNF):
            self.primetime[Constants.THNF] +=1
            

    def removeGameFromSchedule(self, week):
        game = self.schedule[str(week)]
        self.schedule[str(week)] = Constants.NO_GAME_ASSIGNED
        
        if (game != None and game != Constants.NO_GAME_ASSIGNED and game.isEmpty() != True):
            self.schedule[str(week)] = Constants.NO_GAME_ASSIGNED
            self.homeCount[game.getHome()] = self.homeCount[game.getHome()] - 1
            self.awayCount[game.getAway()] = self.awayCount[game.getAway()] - 1
            if (game.getPrimetime() == Constants.SNF):
                self.primetime[Constants.SNF] -=1
            elif(game.getPrimetime() == Constants.MNF):
                self.primetime[Constants.MNF] -=1
            elif(game.getPrimetime() == Constants.THNF):
                self.primetime[Constants.THNF] -=1
            return game
        return None


    def addOffWeekToSchedule(self, week):
        self.getSchedule()[str(week)] = Game.Game(week, Constants.WEEK_OFF, Constants.WEEK_OFF)
        self.totalOff +=1
        

    def isAssigned(self, week):
        if (int(week) > 0):
            return True if self.schedule[week] != Constants.NO_GAME_ASSIGNED else False 
        return False
    
    
    def isCrewOff(self, week):
        if (int(week) > 0):
            return True if self.schedule[week] != Constants.NO_GAME_ASSIGNED and self.schedule[week].getAway() == Constants.WEEK_OFF else False
        
        
    def isDueForOff(self, week):
        intWeek = int(week)       
        if (intWeek == 1):
            return True        
        if (self.getTotalOff() >= Constants.MAX_OFF_WEEKS): 
            return False            
        if (self.isAssigned(str(intWeek-1)) == True):
            if (intWeek <= 8):
                return True if self.getTotalOff() == 0 else False
            elif (intWeek <= 17):
                return True if self.getTotalOff() < 2 else False
            else:
                return False
        else:
            return False


    def hadTeamRecently(self, week, team, threshold):
        if (int(week) > 1):
            lowerBound = int(week) - threshold if (int(week) - threshold > 0) else 1
            upperBound = int(week)
            for prev in range(lowerBound, upperBound):
                if (str(prev) in self.schedule and self.schedule[str(prev)] != Constants.NO_GAME_ASSIGNED):
                    if (self.schedule[str(prev)].getAway() == team or self.schedule[str(prev)].getHome() == team):
                        return True
        return False


    def hadTeamsRecently(self, week, home, away, threshold):
        if (self.hadTeamRecently(week, home, threshold) or self.hadTeamRecently(week, away, threshold)):
            return True
        return False 


    def hadAtLeastOneTeam(self, home, away):
        homeTeamCount = self.homeCount[home] + self.awayCount[home]
        awayTeamCount = self.homeCount[away] + self.awayCount[away]
        return True if homeTeamCount > 0 or awayTeamCount > 0 else False


    def hadOnlyOneTeam(self, home, away):
        homeTeamCount = self.homeCount[home] + self.awayCount[home]
        awayTeamCount = self.homeCount[away] + self.awayCount[away]
        if (homeTeamCount > 0 and awayTeamCount == 0):
            return True
        elif (homeTeamCount == 0 and awayTeamCount > 0):
            return True
        return False
    
    
    def hadOffWeekRecently(self, week):
        if (int(week) > 1):
            lowerBound = int(week) - 2 if (int(week) - 2 > 0) else 1
            upperBound = int(week)
            for prev in range(lowerBound, upperBound):
                if (str(prev) in self.schedule and self.schedule[str(prev)] == Constants.NO_GAME_ASSIGNED):
                        return True
        return False


    def isPreferedRegion(self, team):
        if (self.region == Constants.EAST_REGION and team in Constants.EAST_TEAMS):
            return True
        elif (self.region == Constants.CENTRAL_REGION and team in Constants.CENTRAL_TEAMS):
            return True
        elif (self.region == Constants.WEST_REGION and team in Constants.WEST_TEAMS):
            return True
        return False 
    
    
    def maxedOutEitherTeam(self, home, away):
        homeTeamCount = self.homeCount[home] + self.awayCount[home]
        awayTeamCount = self.homeCount[away] + self.awayCount[away]
        totalCountForTeam = homeTeamCount + awayTeamCount
        return True if totalCountForTeam >= Constants.MAX_TIMES_PER_TEAM else False
        

    def getRanking(self, week, home, away, primetime=None):
        ranking = ""
        if (primetime != None):
            ranking = self.getPrimetimeRanking(primetime, week, home, away)
        else:
            ranking = self.getNonPrimetimeRanking(week, home, away)

        if (int(week) <= Constants.HALF_SEASON and self.totalOff == 0):
            if (ranking <= Constants.MED_RANKING and ranking > Constants.NOT_ALLOWED):
                return Constants.MIN_RANKING
        elif (int(week) >= Constants.HALF_SEASON and self.totalOff < 2):
            if (ranking <= Constants.MED_RANKING and ranking > Constants.NOT_ALLOWED):
                return Constants.MIN_RANKING
        return ranking


    def getPrimetimeRanking(self, primetime, week, home, away):
        ranking = Constants.NOT_ALLOWED
        needsOff = self.isDueForOff(week)
        
        if (self.isAssigned(week) != True):
            primetimeAllowed = self.isPrimetimeAllowed(primetime)
            primetimeCount = self.primetime[primetime]
            extraPrimetimeAllowed = self.isExtraPrimetimeAllowed()
            hadRecentPrimetime = self.hadRecentPrimetime(week, 2)

            hadTeamsAtAll = self.hadAtLeastOneTeam(home, away)
            hadOnlyOneTeam = self.hadOnlyOneTeam(home, away)
            hadTeamsLastTwoWeeks = self.hadTeamsRecently(week, home, away, 2)
            hadTeamWithinFourWeeks = self.hadTeamsRecently(week, home, away, 4)            
            maxedOutEitherTeam = self.maxedOutEitherTeam(home, away)
            inPreferedRegion = self.isPreferedRegion(home)
            
            if (hadRecentPrimetime == False):
                # Primetime allowed, Primetime not maxed, Hasn't had teams at all
                if ((primetimeAllowed == True and primetimeCount < Constants.MAX_PRIMETIME) and
                    hadTeamsAtAll == False and
                    inPreferedRegion == True):
                    ranking = Constants.MAX_RANKING
                elif ((primetimeAllowed == True and primetimeCount < Constants.MAX_PRIMETIME) and
                    hadTeamsAtAll == False and
                    inPreferedRegion == False):
                    ranking = Constants.HIGH_RANKING
                # Primetime allowed, Primetime not maxed, Had teams but not recently (and not maxed) but only one team
                elif((primetimeAllowed == True and primetimeCount < Constants.MAX_PRIMETIME) and
                    hadTeamsAtAll == True and
                    hadOnlyOneTeam == True and 
                    maxedOutEitherTeam == False and
                    hadTeamWithinFourWeeks == False):
                    ranking = Constants.HIGH_RANKING
                # Primetime allowed, Primetime not maxed, Had teams but not recently (and not maxed) and had both teams
                elif((primetimeAllowed == True and primetimeCount < Constants.MAX_PRIMETIME) and
                    hadTeamsAtAll == True and
                    hadOnlyOneTeam == False and
                    maxedOutEitherTeam == False and
                    hadTeamWithinFourWeeks == False):
                    ranking = Constants.MED_RANKING            
                # Primetime allowed, Primetime maxed but allow extra, Had teams but recently (and not maxed)
                elif((primetimeAllowed == True and (primetimeCount < Constants.MAX_EXTRA_PRIMETIME and extraPrimetimeAllowed == True)) and
                    hadTeamsAtAll == True and
                    maxedOutEitherTeam == False and
                    (hadTeamWithinFourWeeks == True and hadTeamsLastTwoWeeks == False)):
                    ranking = Constants.LOW_RANKING
                # Primetime allowed, Primetime not maxed, Had teams but recently (and not maxed)
                elif((primetimeAllowed == True and primetimeCount < Constants.MAX_PRIMETIME) and
                    hadTeamsAtAll == True and
                    maxedOutEitherTeam == False and
                    (hadTeamWithinFourWeeks == True and hadTeamsLastTwoWeeks == False)):
                    ranking = Constants.NOT_ALLOWED

        if (ranking >= Constants.MIN_RANKING and needsOff == True):
            ranking -= 1;
            
        return ranking


    def getNonPrimetimeRanking(self, week, home, away):
        ranking = Constants.NOT_ALLOWED
        needsOff = self.isDueForOff(week)
        
        if (self.isAssigned(week) != True):
            hadTeamsAtAll = self.hadAtLeastOneTeam(home, away)
            hadOnlyOneTeam = self.hadOnlyOneTeam(home, away)
            hadTeamsLastTwoWeeks = self.hadTeamsRecently(week, home, away, 2)
            hadTeamWithinFourWeeks = self.hadTeamsRecently(week, home, away, 4)
            maxedOutEitherTeam = self.maxedOutEitherTeam(home, away)
            inPreferedRegion = self.isPreferedRegion(home)
            
            # Primetime allowed, Primetime not maxed, Hasn't had teams at all
            if (hadTeamsAtAll == False and
                inPreferedRegion == True):
                ranking = Constants.MAX_RANKING
            elif (hadTeamsAtAll == False and
                inPreferedRegion == False):
                ranking = Constants.HIGH_RANKING
            # Primetime allowed, Primetime not maxed, Had teams but not recently (and not maxed) but only one team
            elif(hadTeamsAtAll == True and
                hadOnlyOneTeam == True and 
                maxedOutEitherTeam == False and
                hadTeamWithinFourWeeks == False):
                ranking = Constants.HIGH_RANKING
            # Primetime allowed, Primetime not maxed, Had teams but not recently (and not maxed) and had both teams
            elif(hadTeamsAtAll == True and
                hadOnlyOneTeam == False and 
                maxedOutEitherTeam == False and
                hadTeamWithinFourWeeks == False):
                ranking = Constants.MED_RANKING
            # Primetime allowed, Primetime not maxed, Had teams but recently (and not maxed)
            elif(hadTeamsAtAll == True and
                maxedOutEitherTeam == False and
                (hadTeamWithinFourWeeks == True and hadTeamsLastTwoWeeks == False)):
                ranking = Constants.MIN_RANKING
         
        if (ranking >= Constants.MIN_RANKING and needsOff == True):
            ranking -= 1;
            
        return ranking

class CrewEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__