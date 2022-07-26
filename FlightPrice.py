# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 17:42:08 2022

@author: xlf
"""
def get90CalendarPrices(From,To):
    import requests
    import pandas as pd
    import time
    import os

    url = "https://flights.ctrip.com/international/search/api/lowprice/calendar/getOwCalendarPrices?departCityCode={From}&arrivalCityCode={To}&cabin=Y_S_C_F"
    
    payload={}
    headers = {
      'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
      'sec-ch-ua-mobile': '?0',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
      'scope': 'd',
      'Accept': 'application/json',
      'Cache-Control': 'no-cache',
      'transactionID': '089d1a327a684ee89519a96679ab7ba9',
      'sec-ch-ua-platform': '"Windows"',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Dest': 'empty'
    }
    
    
    
    while(1):
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            low_price_calenlar = response.json()["data"]
            break
        except:
            pass
           
    label_time = time.strftime("%Y-%m-%d|%H:%M", time.localtime()) 
    file_time = time.strftime("%Y-%m-%dT%H", time.localtime()) 
    low_price_calenlar_df = pd.DataFrame(low_price_calenlar,index=[label_time]).T.sort_index()
    try:
        low_price_calenlar_df.to_pickle(f"{From}-{To}/{file_time}.df")            
    except OSError:
        os.mkdir(f"{From}-{To}")
        low_price_calenlar_df.to_pickle(f"{From}-{To}/{file_time}.df")


def readFlightList(file):

    import json
    with open(file) as f:
        t = json.load(f)    
    return [(x,y) for x in t for y in t if x!=y]
          
if __name__ == "main":
    flightList = readFlightList("flight.json")
    for item in flightList:
        get90CalendarPrices(item[0],item[1])
    