"""
Constants.py
"""
ALL_TEAMS = ['PHI', 'NYG', 'WAS', 'DAL', 'MIN', 'GB', 'DET', 'CHI', 'TB', 'ATL', 'CAR', 'NO', 'LAR', 'SF', 'ARZ', 'SEA', 'MIA', 'NYJ', 'NE', 'BUF', 'BAL', 'CIN', 'CLE', 'PIT', 'IND', 'HOU', 'TEN', 'JAX', 'LAS', 'KC', 'DEN', 'LAC']

FOX_TEAMS = ['PHI', 'NYG', 'WAS', 'DAL', 'MIN', 'GB', 'DET', 'CHI', 'TB', 'ATL', 'CAR', 'NO', 'LAR', 'SF', 'ARZ', 'SEA']
CBS_TEAMS = ['MIA', 'NYJ', 'NE', 'BUF', 'BAL', 'CIN', 'CLE', 'PIT', 'IND', 'HOU', 'TEN', 'JAX', 'LAS', 'KC', 'DEN', 'LAC']

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

SCHEDULE_FILE = '../files/NFL2020_csv.csv'
SCHEDULE_OUTPUT = 'NFL2020_generated.csv'

NOT_ALLOWED = 10
MIN_RANKING = 1
LOW_RANKING = 2
MID_RANKING = 3
MAX_RANKING = 4

MAX_PRIMETIME = 1
MAX_EXTRA_PRIMETIME = 3

MAX_TIMES_PER_TEAM = 3

NO_GAME_ASSIGNED = ""