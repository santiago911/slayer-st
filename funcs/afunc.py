import time
import json

import requests

from funcs import constants

# read or write json file
def rJSON(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    
def wJSON(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

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

def calcRebateRate(odd1, odd2) -> float:
    # odd1,odd2:HongKong odds type required.
    return (odd1 + 1) * (odd2 + 1) / (odd1 + odd2 + 2)

def timestamp2text(timestamp:int,format_:str = "%m-%d %H:%M") -> str:
    # requirement: time
    # TODO timestamp must be 9 or 13 digits integer; 13 digits integer have to be 1000 times an integer. 
    t = timestamp if len(str(timestamp)) == 9 else timestamp / 1000    
    return time.strftime(format_, time.localtime(t))

def calcStakes(stake, odd1, odd2) -> str:
    # odd1,odd2:HK odds type required.
    return str(round(stake * (float(odd1) + 1) / (float(odd2) + 1)))

def handicapTransfer(handicap, odd1, odd2, alpha=0.30) -> float:
    # odd1,odd2:HK odds type required.
    # handicap: float type required.
    return float(handicap) - 0.125 * (float(odd1) - float(odd2)) / alpha

def time2stamp(time_str:str,format_:str = "%m-%d %H:%M") -> int: 
    # transfer time string to timestamp.
    return int(time.mktime(time.strptime(time_str,format_)))