# from nba_api.stats.endpoints import leaguegamelog, commonplayerinfo, boxscoretraditionalv2
# import nba_api
import numpy as np
import pandas as pd
import requests
from os import mkdir
import json

years = []


# mkdir("./all_games_jsons")
# def makeJsonsForYears(years):
#     for year in years:
#         games_info = {}
#         try:
#             season = leaguegamelog.LeagueGameLog(season=f"20{year}-{year + 1}")
#             try:
#                 games = season.get_normalized_dict()['LeagueGameLog']
#                 game_ids = set([game['GAME_ID'] for game in games])
#                 for game_id in game_ids:
#                     games_info[game_id] = boxscoretraditionalv2.BoxScoreTraditionalV2(
#                         game_id=game_id).get_normalized_dict()
#                     print(game_id)
#             except requests.exceptions.Timeout:
#                 print("timeout inside second except")
#         except requests.exceptions.Timeout:
#             print("timeout insdie first excepty")
#         f = open(f"./all_games_jsons/all_games20{year}-{year + 1}.json", "w")
#         json.dump(games_info, f)
#         f.close()
def computeGameScore(PTS, FG, FGA, FTA, FT, OREB, DREB, STL, AST, BLK, PF, TO):
    try :
        return round (PTS + 0.4 * FG - 0.7 * FGA - 0.4 * (
                FTA - FT) + 0.7 * OREB + 0.3 * DREB + STL + 0.7 * AST + 0.7 * BLK - 0.4 * PF - TO, 3)
    except:
        return 0

def createGameScoreCSV(file):
    with open(file, 'r') as reader:
        try:
            mkdir('./all_games_csv')
        except:
            print("exceptional behavior, probably folder already exists")
        games = json.load(reader);
        for gameId in games.keys():
            game = games[gameId];
            playerStats = game["PlayerStats"];
            teamStats = game["TeamStats"]
            winner = teamStats[0]["TEAM_ABBREVIATION"] if teamStats[0]["PTS"] > teamStats[1]["PTS"] else teamStats[1]["TEAM_ABBREVIATION"]
            players_list = []
            for player in playerStats:
                name = player["PLAYER_NAME"]
                PTS = player["PTS"]
                FGA = player["FGA"]
                FG = player["FGM"]
                FTA = player["FTA"]
                FT = player["FTM"]
                OREB = player["OREB"]
                DREB = player["DREB"]
                STL = player["STL"]
                AST = player["AST"]
                BLK = player["BLK"]
                PF = player["PF"]
                TO = player["TO"]
                PLUS_MINUS = player["PLUS_MINUS"]
                MIN = player["MIN"]
                id = player["PLAYER_ID"]
                GameScore = computeGameScore(PTS, FG, FGA, FTA, FT, OREB, DREB, STL, AST, BLK, PF, TO)
                TEAM_ABBRV = player["TEAM_ABBREVIATION"]
                WIN = 1 if TEAM_ABBRV == winner else 0
                players_list.append([id, name, PTS, FG, FGA, FTA, FT, OREB, DREB, STL, AST, BLK, PF, TO, PLUS_MINUS, MIN, GameScore, WIN])
            np_arr = np.array(players_list)
            df = pd.DataFrame(players_list, columns=["id", "name", "PTS", "FG", "FGA", "FTA","FT","OREB", "DREB", "STL", "AST", "BLK", "PF", "TO", "PLUS_MINUS", "MIN", "GS", "WIN"])
            df.to_csv(path_or_buf=f'./all_games_csv/{gameId}')
#             team, name, won/lost, scores, player id

createGameScoreCSV("./all_games_jsons/all_games2013-14.json")







