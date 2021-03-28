from nba_api.stats.endpoints  import leaguegamelog, commonplayerinfo, boxscoretraditionalv2
import requests
from os import mkdir
import json
years = [16,17,18,19]

# mkdir("./all_games_jsons")
for year in years:
    games_info = {}
    try:
        season = leaguegamelog.LeagueGameLog(season=f"20{year}-{year+1}")
        try:
            games = season.get_normalized_dict()['LeagueGameLog']
            game_ids = set([game['GAME_ID'] for game in games])
            for game_id in game_ids:
                games_info[game_id] = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id).get_normalized_dict()
                print(game_id)
        except requests.exceptions.Timeout:
            print("timeout inside second except")
    except requests.exceptions.Timeout:
        print("timeout insdie first excepty")
    f = open(f"./all_games_jsons/all_games20{year}-{year+1}.json", "w")
    json.dump(games_info, f)
    f.close()

# f.write(season_19_20_games.get_normalized_json())
# f.close()
# print(season_19_20_games.get_json())


# player_info = commonplayerinfo.CommonPlayerInfo(player_id=2544)
# print(player_info.get_json())
# res = requests.request(url="https://google.com", method="GET");
# print(res)