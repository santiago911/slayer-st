import streamlit as st
import pandas as pd
import time

from funcs import mfunc, afunc, constants

# Page Configuration
st.set_page_config(page_title="SLAYER Streamlit Edition", layout="wide")


def calcArbit(data_list,refund_rate,stakes):
    result_list = []
    for i in data_list:
        RR1 = afunc.calcRebateRate(float(i[8]), float(i[14]))
        RR2 = afunc.calcRebateRate(float(i[9]), float(i[13]))
        if RR1 >= (refund_rate / 400 + 0.5):
            league_name = constants.leagues_dict[i[1]][1] + constants.leagues_dict[i[1]][0] if i[1] in constants.leagues_dict else "（未知）"
            write_list = [str(round(RR1 * 100, 1))+"%",afunc.timestamp2text(int(i[2])), 
                          league_name,i[3], i[4], i[7], i[8], i[14], str(round(RR1 * 100, 2)),
                          str(stakes), afunc.calcStakes(int(stakes), i[8], i[14])]
            result_list.append(write_list)
        elif RR2 >= (refund_rate / 400 + 0.5):
            league_name = constants.leagues_dict[i[1]][1] + constants.leagues_dict[i[1]][0] if i[1] in constants.leagues_dict else "（未知）"
            write_list = [str(round(RR2 * 100, 1))+"%", afunc.timestamp2text(int(i[2])),
                          league_name,i[3], i[4], i[7], i[9], i[13], str(round(RR2 * 100, 2)),
                          str(stakes), afunc.calcStakes(int(stakes), i[9], i[13])]
            result_list.append(write_list)
    return result_list

# Functions - Arbitrage
def ArbitSearch(platforms = ("金宝博","沙巴"),
                time_limit = 24,
                refund_rate_required = 194,
                stakes = 1000):
    
    ## match filter
    ## data[1]: 
    ## 0 mid,1 lid,2 kotime,3 lvtime,4 homeid,5 homecn,6 hometr,7 homeen,8 homerank,
    ## 9 awayid,10 awaycn,11 awaytr,12 awayen,13 awayrank,14 status,15 homescore,16 awayscore,17 unknown null,
    ## 18-25 unknown.
    data = mfunc.fetch_multiodds(platforms=platforms,data_review=None)
    timestamp_limit = int(round(time.time() * 1000)) + int(time_limit) * 3600000
    ## match_list: list of str
    match_list = [i[0] for i in data[1] if int(i[2]) < timestamp_limit and i[14] in ("0","2")]
    ## handicap: 0 matchid,1 companyid,2 han1,3 home1,4 away1,5 han2,6 home2,7 away2,8,9,10 num,11 maxnum
    ## ou:0 matchid,1 companyid,2 han1,3 home1,4 away1,5 han2,6 home2,7 away2,8,9,10 num,11 maxnum
    platforms_1 = constants.platforms_dict[platforms[0]]
    platforms_2 = constants.platforms_dict[platforms[1]]
    
    han1, han2, ou1, ou2 = [],[],[],[]
    for i in data[2]:
        if i[1] == platforms_1 and i[0] in match_list:
            han1.append([i[j] for j in (0,1,5,6,7)])
        elif i[1] == platforms_2 and i[0] in match_list:
            han2.append([i[j] for j in (0,1,5,6,7)])
    for i in data[4]:
        if i[1] == platforms_1 and i[0] in match_list:
            ou1.append([i[j] for j in (0,1,5,6,7)])
        elif i[1] == platforms_2 and i[0] in match_list:
            ou2.append([i[j] for j in (0,1,5,6,7)])
    
    handicap_list_merged = []
    for i in han1:
        for j in han2:
            if i[0] == j[0] and i[2] == j[2]:
                handicap_list_merged.append(i + j)
    overunder_list_merged = []
    for i in ou1:
        for j in ou2:
            if i[0] == j[0] and i[2] == j[2]:
                overunder_list_merged.append(i + j)                
    
    han_match_list_merged = []
    for i in match_list:
        for j in handicap_list_merged:
            if i == j[0]:
                for k in data[1]:
                    if k[0] == i:
                        han_match_list_merged.append([k[n] for n in (0,1,2,5,10)] + j)
                        break
    ou_match_list_merged = []
    for i in match_list:
        for j in overunder_list_merged:
            if i == j[0]:
                for k in data[1]:
                    if k[0] == i:
                        ou_match_list_merged.append([k[n] for n in (0,1,2,5,10)] + j)
                        break    
    
    # Calculate it!
    # match_list_merged including:[list-2d]
    # [0]MatchID,[1]LeagueID,[2]MatchKickoffTimestamp,[3]HomeName,[4]AwayName,
    # [5]MatchID,[6]Platform1,[7]Handicap,[8]HomeOdd,[9]AwayOdd,
    # [10]MatchID,[11]Platform2,[12]Handicap,[13]HomeOdd,[14]AwayOdd
    han_result = calcArbit(han_match_list_merged,refund_rate_required,stakes)
    ou_result = calcArbit(ou_match_list_merged, refund_rate_required,stakes)
    return han_result, ou_result

# Columns
r1c1, r1c2 = st.columns([8, 6])
r2c1, r2c2, r2c3, r2c4, r2c5= st.columns([6, 6, 6, 6, 6])
r3c1, r3c2, r3c3 = st.columns([1, 6, 1])
r4c1, r4c2, r4c3 = st.columns([1, 6, 1])

# Title
with r1c1:
    "# Slayer Streamlit Edition"
with r1c2:
    ""
    ""
    "#### 作者：流老湿。保留所有权利。仅限个人用途。"

# Arbitrage Detection

with r2c1:
    # arbitrage - platforms selection(only for 2-way arbitrage)
    arbit_platforms = st.multiselect(
        "请选择两个平台",
        ("皇冠", "金宝博", "沙巴", "BTI", "奥普斯", "日博", "易胜博"),
        ("金宝博", "沙巴"))
with r2c2:
        # arbitrage - least rebate rate required
    arbit_refund_rate_required = st.slider(
            "要求最低返还率", 
            190,  # min
            200,  # max
            195  # default
            )
with r2c3:
        # arbitrage - stakes
    arbit_stakes = st.text_input(
            "投注配额", 
            "1000")
with r2c4:
    arbit_time_limit = st.text_input(
            "时限(未来N小时内赛事)", 
            "24")


with r2c5:
        ""
        ""
        if st.button("薅他！"):
            arbit_result_list = ArbitSearch(
                platforms = arbit_platforms,
                time_limit = arbit_time_limit,
                refund_rate_required = arbit_refund_rate_required,
                stakes = arbit_stakes)

            handicap_chance = pd.DataFrame(arbit_result_list[0],
                                            columns=['返还率', '比赛时间', '赛事', '主队', '客队', '让分', 
                                                     arbit_platforms[0], arbit_platforms[1], '返还', '主投注', '客投注'])
            overunder_chance = pd.DataFrame(arbit_result_list[1],
                                            columns=['返还率', '比赛时间', '赛事', '主队', '客队', '大小', 
                                                     arbit_platforms[0], arbit_platforms[1], '返还', '主投注', '客投注'])            
            
            r3c2.write("### 让球盘机会")
            r3c2.write(handicap_chance)
            r4c2.write("### 大小盘机会")
            r4c2.write(overunder_chance)
            