import boto3
import json
import Schedule.Game as Game
import Utilities.Constants as Constants
from boto3.dynamodb.conditions import Key, Attr

class GameInfo(object):
    def __init__(self) -> None:
        self.games = {}
        self.fetchGameInfo()


    def fetchGameInfo(self) -> None:
        dynamodb = boto3.resource('dynamodb', region_name=Constants.AWS_REGION)
        table = dynamodb.Table(Constants.TABLE_SCHEDULE_2020)
        response = table.scan()

        for gameItem in response['Items']:
            game = Game.Game(gameItem['week'], gameItem['away'], gameItem['home'], gameItem['tv'], gameItem['specialEventNotes'])
            if (gameItem['week'] not in self.games):
                self.games[gameItem['week']] = []
            self.games[gameItem['week']].append(game)


    def getGames(self):
        return self.games


    def getPrimetimeGamesForWeek(self, week):
        primetimeGames = []
        for game in self.getGames()[str(week)]:
            if (game.getPrimetime() != None):
                primetimeGames.append(game)
        return primetimeGames


    def getNonPrimetimeGamesForWeek(self, week):
        nonPrimetimeGames = []
        for game in self.getGames()[str(week)]:
            if (game.getPrimetime() == None):
                nonPrimetimeGames.append(game)
        return nonPrimetimeGames


    def updateGame(self, week, inputGame, crew) -> None:
        for game in self.getGames()[str(week)]:
            if (game.getHome() == inputGame.getHome() and  game.getAway() == inputGame.getAway()):
                game.setCrew(crew)