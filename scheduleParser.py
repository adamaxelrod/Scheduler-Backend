import boto3
import csv
import Utilities.JSONParser as JSONParser
import Utilities.Constants as Constants
import Schedule.Schedule as Schedule
from boto3.dynamodb.conditions import Key, Attr

import Schedule.CrewInfo as CrewInfo

""" Return TV host for corresponding away team """
def getTVForTeam(away):
    if (away in Constants.FOX_TEAMS):
        return Constants.FOX
    elif (away in Constants.CBS_TEAMS):
        return Constants.CBS
    else:
        return 'None'


""" Lookup TV host for the corresponding game """
def fetchTV(event, away):
    tv = getTVForTeam(away)
    if (event != None):
        if (event in Constants.SNF):
            return Constants.SNF_TV
        elif (event in Constants.MNF):
            return Constants.MNF_TV
        elif (event in Constants.THNF):
            return Constants.THNF_TV
        elif (event in Constants.THGV):
            return tv
        elif (event in Constants.XMAS):
            return Constants.XMAS_TV
        elif (event in Constants.SUN_NATIONAL):
            return tv
    return tv


""" Persist the game information in the database """
def store(week, away, home, event="N/A"):
    try:
        print('Week: {} {} @ {} - {} ({})'.format(week, away, home, event, fetchTV(event, away)))
        dynamodb = boto3.resource('dynamodb', region_name=Constants.AWS_REGION)
        table = dynamodb.Table(Constants.TABLE_SCHEDULE_2020)
        table.put_item(Item = {
                            'gameId': ('W{}_{}_{}').format(week, away, home),
                            'week': week,
                            'away': away,
                            'home': home,
                            'specialEventNotes': event,
                            'tv' : fetchTV(event, away)
                        })
    except KeyError:
        print("Exception storing data")
 

""" Parse the schedule CSV and store it """
def parseAndStore():
    with open(Constants.SCHEDULE_FILE, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            for col in row:
                week = str(row['Week'])
                if (row[col] != 'OFF' and col != 'Week'):
                    if ('(' in row[col] and ')' in row[col]):
                        game = row[col].split('(')
                        game_sub = game[0].split('@')
                        away = game_sub[0]
                        home = game_sub[1]
                        eventNote = game[1].split(')')
                        eventNote = eventNote[0]

                        if (Constants.THNF in eventNote):
                            event = Constants.THNF
                        elif (Constants.SNF in eventNote):
                            event = Constants.SNF
                        elif (Constants.MNF in eventNote):
                            event = Constants.MNF
                        elif (Constants.THGV in eventNote):
                            event = Constants.THGV
                        elif (Constants.XMAS in eventNote):
                            event = Constants.XMAS
                        elif (Constants.SUN_NATIONAL in eventNote):
                            event = Constants.SUN_NATIONAL
                        else:
                            event = 'None'
                        store (week.strip(), away.strip(), home.strip(), event.strip())
                    else:
                        game = row[col].split('@')
                        away = game[0]
                        home = game[1]
                        store(week.strip(), away.strip(), home.strip())


""" Query for games """ 
def fetchGames(week):
    dynamodb = boto3.resource('dynamodb', region_name=Constants.AWS_REGION)
    table = dynamodb.Table(Constants.TABLE_SCHEDULE_2020)
    response = table.scan(FilterExpression=Key('week').eq(week))

    for game in response['Items']:
        print("{} @ {} - {} {}".format(game['away'], game['home'], game['tv'], game['specialEventNotes'] if (game['specialEventNotes'] != 'N/A') else ""))


def processSchedule():
    return Schedule.Schedule()


def fetchCrews():
    crewInfo = CrewInfo.CrewInfo()
    

def handler(event, context): 
    schedule = processSchedule()
    parser = JSONParser.JSONParser(schedule.getGames(), schedule.getCrews())


if __name__ == '__main__':
    #parseAndStore()    
    schedule = processSchedule()
    parser = JSONParser.JSONParser(schedule.getGames(), schedule.getCrews())
   # print(parser.fetchWeekAsJSON(1))
    print(parser.fetchCrewAsJSON("MARTIN"))
    