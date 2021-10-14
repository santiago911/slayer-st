# Title
script_name = ("流光杀手 v1.0","Slayer Streamlit Edition v1.0")
script_author = ("作者：流老湿。保留所有权利。仅限个人用途。",
                 "Viktor Liu's work. All rights reserved. Personal use only.")
buyme = ("打赏流老湿","Buy me a cup of coffee")
# Labels
text_arbit_0 = ("静态对冲套利","Arbitrage")
text_arbit_1_0 = ("请选择两个平台","Please Select TWO Platforms")
text_arbit_1_1 = (("皇冠", "金宝博", "沙巴", "BTI", "奥普斯", "日博", "易胜博"),
                  ("Crown", "188BET", "IBCBET", "BTI", "OPUS", "BET365", "EasyBets"))
text_arbit_1_2 = (("金宝博", "沙巴"),("188BET", "IBCBET"))
text_arbit_2_0 = ("要求最低返还率","Rebate Rate Required")
text_arbit_3_0 = ("投注配额","Stakes")
text_arbit_4_0 = ("时限(未来N小时内赛事)","Timelimit - hours in future")
text_arbit_5_0 = ("是否只搜索主让球盘","If Search Primary Handicap Only")
text_arbit_5_1 = (("是","否"),("Yes","No"))
text_arbit_6_0 = ("数据展示格式","Report Show Type")
# Help Texts
text_arbit_1_help = (
    """
    选择你所使用的两个平台。  
    考虑到大部分玩家的通常习惯，本程序被设计成只支持两个平台的数据计算。
    特别强调：我不是不会哦，我只是懒  
    """,
    """not completed yet""")
text_arbit_2_help = (
    """
    要求的最低返奖率。用我们通常所说的19x水表示。  
    返奖率低于这个值的结果将被过滤。默认值是196。  
    我建议你在周末调高此值（因为五大赛事较多），而在周中降低此值（如果必要）。 
    """,
    """not completed yet""")
text_arbit_3_help = (
    """
    填写一面的投注额（默认值是10000），可以计算出另一面的投注额。  
    这只是给懒人或者某位智障尤文球迷准备的，说实话，没卵用。  
    """,
    """not completed yet""")
text_arbit_4_help = (
    """
    时限的单位是小时，可以用来过滤掉未来N小时以外的赛事。  
    默认值是48，一般来说不需要修改。 
    """,
    """not completed yet""")
text_arbit_5_help = (
    """
    是否只搜索主要盘口。
    主要盘口是指两面赔率比较接近的（香港盘0.80-1.10）。  
    大部分平台会为比赛开出多盘口，并且有时副盘口的套利返奖率甚至要高于主盘口。  
    设置为是时会只计算主盘口，比较适合周末比赛多的情况。而设置为否比较适合比赛少的情况。两个选项的运算速度几乎没有差异。  
    从实战角度说，副盘口的投注额上限一般要比主盘口低很多；此外，周末比赛多的时候，同时搜索副盘口会出现很多让人眼花缭乱的数据。  
    所以，建议周末选择只搜索主盘口；其他赛事较少的比赛日可以选择同时搜索副盘口。
    """,
    """not completed yet""")
text_arbit_6_help = (
    """
    选择你所使用的两个平台。  
    考虑到大部分玩家的通常习惯，本程序被设计成只支持两个平台的数据计算。  
    """,
    """not completed yet""")
text_submit = ("薅他！","Search！")
text_arbit_df_columns = (['返还率', '比赛时间', '赛事', '主队', '客队', '让分', '主指数', '客指数', '返还', '主投注', '客投注'],
                         ['RbRate', 'KOffTime', 'League', 'Home', 'Away', 'Handi', 'HOdd', 'AOdd', 'RbRate', 'HStakes', 'AStakes'])
text_arbit_mdtable = ("|返还率|比赛时间|赛事|主队|客队|让分|主指数|客指数|返还率|主投注|客投注|",
                      "|RbRate|KOffTime|League|Home|Away|Handi|HOdd|AOdd|RbRate|HStakes|AStakes|")