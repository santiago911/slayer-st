import time
import requests
import constants

def requestCode(url, decode:str = None) -> str:
    # requirement: requests
    # GET code from source URL.
    # :decode:  None for raw text, or str of decode type for page code decoded to any charset.
    response = requests.get(url, headers = constants.requests_headers)
    if decode == None:
        page_code = response.text
    else:
        page_code = response.content.decode(decode)
    return page_code

def calcRebateRate(x, y) -> float:
    # x,y:HK odds type required.
    return (x + 1) * (y + 1) / (x + y + 2)

def timestamp2Text(timestamp) -> str:
    # requirement: time
    # to convert 13 digits timestamp to formatted text for reading.
    return time.strftime("%m-%d %H:%M", time.localtime(timestamp / 1000))

def calcStakes(stake, odd1, odd2) -> str:
    # odd1,odd2:HK odds type required.
    return str(round(stake * (float(odd1) + 1) / (float(odd2) + 1)))

def handicapTransfer(handicap, odd1, odd2, alpha=0.30) -> float:
    # odd1,odd2:HK odds type required.
    # handicap: float type required.
    return float(handicap) - 0.125 * (float(odd1) - float(odd2)) / alpha

def time2stamp(t, _year_int4 = 2021) -> int: 
    # transfer time string to timestamp.
    # TODO default year is 2021. Games past years have not been optimized and can not be transferred correctly so far.
    return int(time.mktime(time.strptime(str(_year_int4) + '-' + t,'%Y-%m-%d %H:%M')))
