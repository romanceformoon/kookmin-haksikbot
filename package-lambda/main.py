import requests
import os
import datetime
import json

def lambda_handler(event, context):
    if event["content"]:
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d')
        today = now.strftime('%m월 %d일')
    
        params = {'sdate': nowDate, 'edate': nowDate, 'today': nowDate}
        res = requests.post('http://kmucoop.kookmin.ac.kr/menu/menujson.php', data=params)
        cafe = event["content"]
        
        try:
            menu = ""
            for keys, values in res.json()[cafe][nowDate].items():
                menu += keys.replace('<br>', '') + "\n" + res.json()[cafe][nowDate][keys]['메뉴'].replace('\r', '').strip() + " " + res.json()[cafe][nowDate][keys]['가격'] + "\n\n\n"
        except:
            menu = ""
            data = json.loads(res.text)
            for keys, values in data[cafe][nowDate].items():
                menu += keys.replace('<br>', '') + "\n" + data[cafe][nowDate][keys]['메뉴'].replace('\r', '').strip() + " " + data[cafe][nowDate][keys]['가격'] + "\n\n\n"
                

        final = {
                "message":{
                    "text": today + '의 ' + event["content"] + ' 메뉴입니다.\n\n' + menu
                },
                "keyboard":{
                    "type": "buttons",
                    "buttons": ['학생식당', '교직원식당', '한울식당', '청향', '생활관식당(일반식)', '생활관식당(정기식)']
                }
            }

    return final

