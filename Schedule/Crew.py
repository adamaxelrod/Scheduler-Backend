import json
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


    def initializeSchedule(self):
        schedule = {}
        for i in range(1, 18):
            schedule[str(i)] = Constants.NO_GAME_ASSIGNED
        return schedule


    def initializeTeamList(self):
        teamList = {}
        for team in Constants.ALL_TEAMS:
            teamList[team] = 0
        return teamList


    def getCrewName(self):
        return self.crewName


    def getRegion(self):
        return self.region


    def getSchedule(self):
        return self.schedule


    def getPrimetime(self):
        return self.primetime


    def isPrimetimeAllowed(self, primetime):
        primetimeStr = primetime.lower() + "Allowed"
        if (self.rules[primetimeStr] == "true"):
            return True
        else:
            return False


    def addGameToSchedule(self, game):
        self.schedule[game.getWeek()] = game
        self.homeCount[game.getHome()] = self.homeCount[game.getHome()] + 1
        self.awayCount[game.getAway()] = self.awayCount[game.getAway()] + 1

        if (game.getPrimetime() == Constants.SNF):
            self.primetime[Constants.SNF] += 1
        elif(game.getPrimetime() == Constants.MNF):
            self.primetime[Constants.MNF] +=1
        elif(game.getPrimetime() == Constants.THNF):
            self.primetime[Constants.THNF] +=1


    def addOffWeekToSchedule(self, week):
        self.schedule[week] = "OFF"
        self.totalOff +=1


    def isAssigned(self, week):
        return True if self.schedule[week] != "" else False 


    def hadTeamRecently(self, week, team):
        if (int(week) > 1):
            lowerBound = int(week) - 4 if (int(week) - 4 > 0) else 1
            upperBound = int(week) if (int(week) >= 0) else 1

            for prev in range(lowerBound, upperBound):
                if (str(prev) in self.schedule and self.schedule[str(prev)] != Constants.NO_GAME_ASSIGNED):
                    if (self.schedule[str(prev)].getAway() == team or self.schedule[str(prev)].getHome() == team):
                        return True
        return False


    def hadTeamsRecently(self, week, home, away):
        if (self.hadTeamRecently(week, home) or self.hadTeamRecently(week, away)):
            return True
        return False 


    def hadOneTeam(self, home, away):
        homeTeamCount = self.homeCount[home] + self.awayCount[home]
        awayTeamCount = self.awayCount[away] + self.awayCount[away]
        return True if homeTeamCount > 0 or awayTeamCount > 0 else False


    def maxedOutEitherTeam(self, home, away):
        homeTeamCount = self.homeCount[home] + self.awayCount[home]
        awayTeamCount = self.awayCount[away] + self.awayCount[away]
        return True if homeTeamCount >= Constants.MAX_TIMES_PER_TEAM or awayTeamCount >= Constants.MAX_TIMES_PER_TEAM else False


    def getPrimetimeRanking(self, primetime, week, home, away):
        if (self.isAssigned(week) != True):
            primetimeAllowed = self.isPrimetimeAllowed(primetime)
            primetimeCount = self.primetime[primetime]

            hadTeamsAtAll = self.hadOneTeam(home, away)
            hadTeamWithinFourWeeks = self.hadTeamsRecently(week, home, away)
            maxedOutEitherTeam = self.maxedOutEitherTeam(home, away)

            # Primetime allowed, Primetime not maxed, Hasn't had teams at all
            if (primetimeAllowed == True and 
                primetimeCount < Constants.MAX_PRIMETIME and
                hadTeamsAtAll == False):
                return Constants.MAX_RANKING
            # Primetime allowed, Primetime not maxed, Had teams but not recently (and not maxed)
            elif(primetimeAllowed == True and 
                primetimeCount < Constants.MAX_PRIMETIME and
                hadTeamsAtAll == True and
                maxedOutEitherTeam == False and
                hadTeamWithinFourWeeks == False):
                return Constants.MID_RANKING
            # Primetime allowed, Primetime not maxed, Had teams but recently (and not maxed)
            elif(primetimeAllowed == True and 
                primetimeCount < Constants.MAX_PRIMETIME and
                hadTeamsAtAll == True and
                maxedOutEitherTeam == False and
                hadTeamWithinFourWeeks == True):
                return Constants.MIN_RANKING
            else:
                return Constants.NOT_ALLOWED
        else:
            return Constants.NOT_ALLOWED


    def getNonPrimetimeRanking(self, week, home, away):
        if (self.isAssigned(week) != True):
            hadTeamsAtAll = self.hadOneTeam(home, away)
            hadTeamWithinFourWeeks = self.hadTeamsRecently(week, home, away)
            maxedOutEitherTeam = self.maxedOutEitherTeam(home, away)

            # Primetime allowed, Primetime not maxed, Hasn't had teams at all
            if (hadTeamsAtAll == False):
                return Constants.MAX_RANKING
            # Primetime allowed, Primetime not maxed, Had teams but not recently (and not maxed)
            elif(hadTeamsAtAll == True and
                maxedOutEitherTeam == False and
                hadTeamWithinFourWeeks == False):
                return Constants.MID_RANKING
            # Primetime allowed, Primetime not maxed, Had teams but recently (and not maxed)
            elif(hadTeamsAtAll == True and
                maxedOutEitherTeam == False and
                hadTeamWithinFourWeeks == True):
                return Constants.MIN_RANKING
            else:
                return Constants.NOT_ALLOWED
        else:
            return Constants.NOT_ALLOWED