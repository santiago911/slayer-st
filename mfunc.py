import re
import time
import requests
import constants
import afunc
# Functions
# - Arbitrage
def ArbitSearch(platforms_selection = ("金宝博","沙巴"),
                time_limit = 48,
                primary_handicap_only = "否",
                rebate_rate_required = 194,
                stakes = 10000,
                language = 0):
    # request code
    url = 'http://zhishu.35.zqsos.com:896/xml/odds_n.aspx?companyID=,' + \
        constants.platforms_dict[platforms_selection[0]] + ',' + \
        constants.platforms_dict[platforms_selection[1]] + ','
    page_code = afunc.requestCode(url,None)
    
    # process data    
    timestamp_limit = int(round(time.time() * 1000)) + int(time_limit) * 3600000
    gamelist = []
    # re_game includes: [0]MatchID, [1]LeagueID, [2]MatchTimestamp, [3]HomeID, [4]HomeName [5]AwayID [6]AwayName
    if language == 0:
        gamelist = re.findall("(\d{7}),(%s),(\d{13}),.*?,(\d+),(.*?),.*?,.*?,.*?,(\d+),(.*?),.*?,.*?," % (constants.arbit_leagues_filter), page_code)
    elif language == 1:
        gamelist = re.findall("(\d{7}),(%s),(\d{13}),.*?,(\d+),.*?,.*?,(.*?),.*?,(\d+),.*?,.*?,(.*?)," % (constants.arbit_leagues_filter), page_code)
    re_gamelist = "|".join([i[0] for i in gamelist if int(i[2]) < timestamp_limit])
    
    # if only search primary handicaps.
    if primary_handicap_only == "是" or "Yes":
        re_handicap_1 = '(%s),(%s),(-*\d\.\d{2}),[01]\.\d{2},[01]\.\d{2},(-*\d\.\d{2}),([01]\.[0189]\d),([01]\.[0189]\d),' % (
            re_gamelist, constants.platforms_dict[platforms_selection[0]]) + '(False|True),(False|True),\d,\d'
        re_handicap_2 = '(%s),(%s),(-*\d\.\d{2}),[01]\.\d{2},[01]\.\d{2},(-*\d\.\d{2}),([01]\.[0189]\d),([01]\.[0189]\d),' % (
            re_gamelist, constants.platforms_dict[platforms_selection[1]]) + '(False|True),(False|True),\d,\d'
    elif primary_handicap_only == "否" or "No":
        re_handicap_1 = '(%s),(%s),(-*\d\.\d{2}),[01]\.\d{2},[01]\.\d{2},(-*\d\.\d{2}),([01]\.\d{2}),([01]\.\d{2}),' % (
            re_gamelist, constants.platforms_dict[platforms_selection[0]]) + '(False|True),(False|True),\d,\d'
        re_handicap_2 = '(%s),(%s),(-*\d\.\d{2}),[01]\.\d{2},[01]\.\d{2},(-*\d\.\d{2}),([01]\.\d{2}),([01]\.\d{2}),' % (
            re_gamelist, constants.platforms_dict[platforms_selection[1]]) + '(False|True),(False|True),\d,\d'
    
    # handicap list merging.
    handicap_list_1, handicap_list_2 = [], []
    handicap_list_1 = re.findall(re_handicap_1, page_code)
    handicap_list_2 = re.findall(re_handicap_2, page_code)

    handicap_list_merged = []
    for i in handicap_list_1:
        for j in handicap_list_2:
            if i[0] == j[0] and i[3] == j[3]:
                handicap_list_merged.append(i + j)
                break
    # merging again.
    match_list_merged = []
    for i in gamelist:
        for j in handicap_list_merged:
            if i[0] == j[0]:
                match_list_merged.append(i + j)
                break
    # Calculate it!
    # match_list_merged including:[list(tuples)]
    # [0]MatchID,[1]LeagueID,[2]MatchKickoffTimestamp,[3]HomeID,[4]HomeName,[5]AwayID,[6]AwayName,
    # [7]MatchID,[8]PlatformID,[9]EarlyHandicap,[10]LiveHandicap,[11]HomeOdd,[12]AwayOdd,[13][14]unknown'False/True',
    # [15]MatchID,[16]PlatformID,[17]EarlyHandicap,[18]LiveHandicap,[19]HomeOdd,[20]AwayOdd,[21][22]unknown'False/True'
    result_list = []
    for i in match_list_merged:
        league_name = constants.leagues_dict[i[1]][1] + constants.leagues_dict[i[1]][0] if i[1] in constants.leagues_dict else "（未知）"
        if afunc.calcRebateRate(float(i[11]), float(i[20])) >= (rebate_rate_required / 400 + 0.5):
            write_list = [str(round(afunc.calcRebateRate(float(i[11]), float(i[20])) * 100, 1))+"%",afunc.timestamp2Text(int(i[2])), 
                          league_name,i[4], i[6], i[10], i[11], i[20], round(afunc.calcRebateRate(float(i[11]), float(i[20])) * 100, 2),
                          str(stakes), afunc.calcStakes(int(stakes), i[11], i[20])]
            result_list.append(write_list)
        elif afunc.calcRebateRate(float(i[12]), float(i[19])) >= (rebate_rate_required / 400 + 0.5):
            write_list = [str(round(afunc.calcRebateRate(float(i[12]), float(i[19])) * 100, 1))+"%", afunc.timestamp2Text(int(i[2])),
                          league_name,i[4], i[6], i[10], i[12], i[19], round(afunc.calcRebateRate(float(i[12]), float(i[19])) * 100, 2),
                          str(stakes), afunc.calcStakes(int(stakes), i[12], i[19])]
            result_list.append(write_list)
    return result_list