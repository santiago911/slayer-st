import re
import time
import requests
from funcs import constants
from funcs import afunc
from lxml import etree
import pandas as pd
from pyquery import PyQuery as pq

# fetch win007-multiodds-page-data and process.
def fetch_multiodds(platforms = ("金宝博","沙巴"), 
                    data_review = None):
    # data_review: None for current day, or YYYY-MM-DD str for history review.  
    if data_review == None: 
        url = 'http://zhishu.35.zqsos.com:892/xml/odds_n.aspx?companyID=,' + \
            constants.platforms_dict[platforms[0]] + ',' + \
            constants.platforms_dict[platforms[1]] + ','
        page_code = afunc.requestCode(url,None)
    else:
        url = 'http://vip.titan007.com/history/multiOddsData.aspx?date=' + data_review
        page_code = afunc.requestCode(url,"GBK")
    
    splitDomain = "$"
    splitRecord = ";"
    splitColumn = ","
    
    domains = page_code.split(splitDomain)
    leagueDomain = domains[0]
    matchDomain = domains[1]
    hanDomain = domains[2]
    hdaDomain = domains[3]
    ouDomain = domains[4]
    
    # 0 leagueid, 1 leaguetype(1 for liga and 2 for cup), 2 leaguecolor, 
    # 3 leaguecnname, 4 leaguetrname, 5 leagueenname, 6 url, 7 isimportant(1 for important league, 0 for not)
    leagueDetail = leagueDomain.split(splitRecord)
    leagueList = []
    for league in leagueDetail:
        l = league.split(splitColumn)
        leagueList.append(l)

    #mid,lid,time1,time2,t1id,
    #t1cn,t1tr,t1en,t1rank,t2id,
    #t2cn,t2tr,t2en,t2rank,state,
    #homescore,awayscore,tv,iszhongli,level
    matchDetail = matchDomain.split(splitRecord)
    matchList = []
    for match in matchDetail:
        m = match.split(splitColumn)
        matchList.append(m)

    # mid,cid,handicap,home,away,handicap,home,away,isclose,islive,num,maxnum,
    hanDetail = hanDomain.split(splitRecord)
    hanList = []
    for handicap in hanDetail:
        o = handicap.split(splitColumn)
        hanList.append(o)
        
    #mid,cid,home,draw,away,home,draw,away,num
    hdaRecord = hdaDomain.split(splitRecord)
    hdaList = []
    for hda in hdaRecord:
        o = hda.split(splitColumn)
        hdaList.append(o)
    
    # mid,cid,ou,over,under,ou,over,under,num
    ouRecord = ouDomain.split(splitRecord)
    ouList = []
    for ou in ouRecord:
        o = ou.split(splitColumn)
        ouList.append(o)

    return leagueList, matchList, hanList, hdaList, ouList

def get_team_info(teamID):
    code = afunc.requestCode(f"http://zq.titan007.com/jsData/teamInfo/teamDetail/tdl{teamID}.js","utf8")
    lineup = re.findall("var lineupDetail=(.*?);",code)
    line = eval(lineup[0]) if lineup else []
    coach = [line[0][i] for i in (0,2,5,9)] if line[0][8] == "主教练" else []
    team = [[line[i][j] for j in (0,1,2,5,8,9,11,13,14,15,16)] for i in range(1, len(line))]
    return coach, team

def get_lineup(matchID):
    detail_code = afunc.requestCode(f"http://live.titan007.com/detail/{matchID}sb.htm","utf8")
    docu = pq(detail_code)
    home_number_list = re.findall('(\d+)',docu('.home .name').text())
    away_number_list = re.findall('(\d+)',docu('.guest .name').text())
    return home_number_list, away_number_list


# Functions
# - Arbitrage

def HandicapChangeMost(date = None,
                       platform_selection = "沙巴",
                       time_limit = 480,
                       handicap_transfer_alpha = 0.30
                       ):
    # request code
    if date == None:
        url = 'http://zhishu.35.zqsos.com:896/xml/odds_n.aspx?companyID=,8,12,14,23,24,'
    else:
        url = 'http://vip.win007.com/history/multiOddsData.aspx?date=' + str(date)
    page_code = afunc.requestCode(url,None)

    # process data
    timestamp_limit = int(round(time.time() * 1000)) + int(time_limit) * 3600000
    # gamelist includes: [0]MatchID, [1]LeagueID, [2]MatchKickoffTimestamp, [3]HomeID, [4]HomeName [5]AwayID [6]AwayName
    gamelist = re.findall("(\d+),(\d+),(\d{13}),.*?,(\d+),(.*?),.*?,.*?,.*?,(\d+),(.*?),", page_code)
    
    if date == None:
        re_gamelist = "|".join([i[0] for i in gamelist if int(i[2]) < timestamp_limit and int(i[2]) > time.time() * 1000])
    else:
        re_gamelist = "|".join([i[0] for i in gamelist])
    
    re_handicap = '(%s),(%s),(-*\d\.\d{2}),(\d\.\d{2,3}),(\d\.\d{2,3}),(-*\d\.\d{2}),(\d\.\d{2,3}),(\d\.\d{2,3}),' % (
        re_gamelist, constants.platforms_dict[platform_selection]) + '(False|True),(False|True),1,\d'
    # handicap list merging.
    handicap_list = re.findall(re_handicap, page_code)
    handicap_list_merged = []
    for i in gamelist:
        for j in handicap_list:
            if i[0] == j[0]:
                handicap_list_merged.append(i + j)
                break
    handicap_transfer_list = []
    for i in handicap_list_merged:
        hte = afunc.handicapTransfer(i[9],i[10],i[11],handicap_transfer_alpha)
        htc = afunc.handicapTransfer(i[12],i[13],i[14],handicap_transfer_alpha)
        handicap_transfer_list.append(list(i) + [round(hte,2),round(htc,2),round(htc - hte,2)])
    handicap_transfer_dataset = []
    for i in handicap_transfer_list:
        label = ((constants.leagues_dict[i[1]][1]+ constants.leagues_dict[i[1]][0]) if i[1] in constants.leagues_dict else "（未知）") + " " + i[4] + " VS " + i[6]
        handicap_transfer_dataset.append([label,i[0],i[1],i[3],i[5],afunc.timestamp2Text(int(i[2])),i[10],i[9],i[11],i[13],i[12],i[14],i[17],i[18],i[19]])
    
    return handicap_transfer_dataset

def SingleGameHandicapChange(matchid, companyid = 24):
    url = f"http://vip.titan007.com/changeDetail/handicap.aspx?id={matchid}&companyID={companyid}"
    tree = etree.HTML(afunc.requestCode(url, decode='GBK'))

    odd_home = tree.xpath('//*[@id="odds2"]/table/tr[./td/text()="早" or ./td/text()="即"]/td[3]//text()')
    handicap = tree.xpath('//*[@id="odds2"]/table/tr[./td/text()="早" or ./td/text()="即"]/td[4]//text()')
    odd_away = tree.xpath('//*[@id="odds2"]/table/tr[./td/text()="早" or ./td/text()="即"]/td[5]//text()')
    chg_time = tree.xpath('//*[@id="odds2"]/table/tr[./td/text()="早" or ./td/text()="即"]/td[6]//text()')

    odd_list = []
    for i in range(len(chg_time)):
        odd_list.append([float(odd_home[i]), 
                         float(constants.handicap_dict[handicap[i]]), 
                         float(odd_away[i]), 
                         chg_time[i],
                         afunc.time2stamp("2022-" + chg_time[i],"%Y-%m-%d %H:%M"), 
                         round(afunc.handicapTransfer(float(constants.handicap_dict[handicap[i]]),float(odd_home[i]),float(odd_away[i])),4)
                         ])
    return odd_list

def LineChartData(odd_list, start_hour = None, period = 3600):

    odd_list_new = []
    if start_hour == None:
        timeline = int((odd_list[0][4] - odd_list[-1][4]) / period) + 1
        odd_list_new.append(odd_list[0])
    else:
        timeline = int(start_hour * 3600 / period) + 1
    
    for i in range(timeline):
        for j in range(len(odd_list)):
            if odd_list[j][4] < odd_list[0][4] - period * (i + 1):
                odd_list_new.append(odd_list[j])
                break
    
    if start_hour == None:
        odd_list_new.append(odd_list[-1])
    
    odd_list_new = odd_list_new[::-1]
    data = pd.DataFrame(odd_list_new,columns=["Home","Handicap","Away","Time","Timestamp","HandiTrans"])
    return data

