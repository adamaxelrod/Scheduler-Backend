"""
Constants.py
"""

""" Team Information """
ALL_TEAMS = ['PHI', 'NYG', 'WAS', 'DAL', 'MIN', 'GB', 'DET', 'CHI', 'TB', 'ATL', 'CAR', 'NO', 'LAR', 'SF', 'ARZ', 'SEA', 'MIA', 'NYJ', 'NE', 'BUF', 'BAL', 'CIN', 'CLE', 'PIT', 'IND', 'HOU', 'TEN', 'JAX', 'LAS', 'KC', 'DEN', 'LAC']

FOX_TEAMS = ['PHI', 'NYG', 'WAS', 'DAL', 'MIN', 'GB', 'DET', 'CHI', 'TB', 'ATL', 'CAR', 'NO', 'LAR', 'SF', 'ARZ', 'SEA']
CBS_TEAMS = ['MIA', 'NYJ', 'NE', 'BUF', 'BAL', 'CIN', 'CLE', 'PIT', 'IND', 'HOU', 'TEN', 'JAX', 'LAS', 'KC', 'DEN', 'LAC']

EAST_TEAMS = ['PHI', 'NYG', 'WAS', 'TB', 'ATL', 'CAR', 'MIA', 'NYJ', 'NE', 'BUF', 'BAL', 'JAX']
CENTRAL_TEAMS = ['DAL', 'MIN', 'GB', 'DET', 'CHI', 'NO', 'CIN', 'CLE', 'PIT', 'IND', 'HOU', 'TEN', 'KC']
WEST_TEAMS = ['LAR', 'SF', 'ARZ', 'SEA', 'LAS', 'KC', 'LAC' ]

EAST_REGION = 'EAST'
CENTRAL_REGION = 'CENTRAL'
WEST_REGION = 'WEST'


""" TV Information """
CBS = "CBS"
FOX = "FOX"
NBC = "NBC"
ESPN = "ESPN"
NFLN = "NFLN"
THNF = "THNF"
SNF = "SNF"
MNF = "MNF"
SUN_NATIONAL = "NAT"

SNF_TV = "NBC"
MNF_TV = "ESPN"
THNF_TV = "FOX"
XMAS_TV = "Fox"

THGV = "THGV"
XMAS = "XMAS"


""" DYNAMO INFO """
AWS_REGION = "us-west-1"
TABLE_SCHEDULE_2020 = "GameInfo_2020"
TABLE_CREWINFO_2020 = "CrewInfo"


""" Schedule file info """
SCHEDULE_FILE = '../files/NFL2020_csv.csv'
SCHEDULE_OUTPUT = 'NFL2020_generated.csv'


""" Ranking and algorithm tuning params """
NOT_ALLOWED = 0
MIN_RANKING = 1
LOW_RANKING = 2
MED_RANKING = 3
HIGH_RANKING = 4
MAX_RANKING = 5

MAX_PRIMETIME = 2
MAX_EXTRA_PRIMETIME = 3

MAX_TIMES_PER_TEAM = 3

NO_GAME_ASSIGNED = ""

WEEK_OFF = "OFF"

HALF_SEASON = 9
FULL_SEASON = 17
MAX_GAMES_PER_WEEK = 16