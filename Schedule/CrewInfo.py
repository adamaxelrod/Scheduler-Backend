import boto3
import json
import Schedule.Crew as Crew
import Utilities.Constants as Constants
from boto3.dynamodb.conditions import Key, Attr

class CrewInfo(object):
    def __init__(self) -> None:
        self.crews = {}
        self.fetchCrewInfo()


    def fetchCrewInfo(self) -> None:
        dynamodb = boto3.resource('dynamodb', region_name=Constants.AWS_REGION)
        table = dynamodb.Table(Constants.TABLE_CREWINFO_2020)
        response = table.scan()

        for crewItem in response['Items']:
            crew = Crew.Crew(crewItem['crewName'], crewItem['region'], crewItem['rules'])
            self.crews[crewItem['crewName']] = crew


    def getCrews(self):
        return self.crews


    def updateCrew(self, crewName, game) -> None:
        self.crews[crewName].addGameToSchedule(game)
        
        
    def assignOff(self, crewName, week) -> None:
        self.crews[crewName].addOffWeekToSchedule(week)