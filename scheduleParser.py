import boto3
import csv
from boto3.dynamodb.conditions import Key, Attr

def getTVForTeam(away):
    foxGames = ['PHI', 'NYG', 'WAS', 'DAL', 'MIN', 'GB', 'DET', 'CHI', 'TB', 'ATL', 'CAR', 'NO', 'LAR', 'SF', 'ARZ', 'SEA']
    cbsGames = ['MIA', 'NYJ', 'NE', 'BUF', 'BAL', 'CIN', 'CLE', 'PIT', 'IND', 'HOU', 'TEN', 'JAX', 'LAS', 'KC', 'DEN', 'LAC']
    
    if (away in foxGames):
        return 'FOX'
    elif (away in cbsGames):
        return 'CBS'
    
    return None


def fetchTV(event, away):
    tv = getTVForTeam(away)

    if (event != None):
        if (event in 'SNF'):
            return 'NBC'
        elif (event in 'MNF'):
            return 'ESPN'
        elif (event in 'THNF'):
            return 'FOX'
        elif (event in 'THGV'):
            return tv
        elif (event in 'XMAS'):
            return 'FOX'
        elif (event in 'NAT'):
            return tv
    else:
        return tv


def store(week, away, home, event=None):
    try:
        if (week == '1'):
            print('Week: {} {} @ {} - {} ({})'.format(week, away, home, event, fetchTV(event, away)))
            dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
            table = dynamodb.Table('GameInfo_2020')
            table.put_item(Item = {
                                'gameId': ('{}_{}_{}').format(week, away, home),
                                'week': week,
                                'away': away,
                                'home': home,
                                'specialEventNotes': event,
                                'tv' : fetchTV(event, away)
                            })
    except KeyError:
        print("Exception storing data")
 
def parseAndStore():
    with open('NFL2020_csv.csv', mode='r') as csv_file:
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

                        if ('THNF' in eventNote):
                            event = 'THNF'
                        elif ('SNF' in eventNote):
                            event = 'SNF'
                        elif ('MNF' in eventNote):
                            event = 'MNF'
                        elif ('THGV' in eventNote):
                            event = 'THGV'
                        elif ('XMAS' in eventNote):
                            event = 'XMAS'
                        elif ('NAT' in eventNote):
                            event = 'NAT'
                        else:
                            event = 'None'
                        store (week.strip(), away.strip(), home.strip(), event.strip())
                    else:
                        game = row[col].split('@')
                        away = game[0]
                        home = game[1]
                        store(week.strip(), away.strip(), home.strip())

if __name__ == '__main__':
    parseAndStore()    