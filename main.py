import json
from datetime import datetime, timezone
from pytz import timezone as tz
from bs4 import BeautifulSoup
import re
import requests


def wipetxt(content):
    wiped = BeautifulSoup(content, "html.parser").get_text()
    cleaned = re.sub(r"@[\w.-]+", "", wiped)
    return cleaned

def utc2teh(time):
    utc_time = datetime.fromisoformat(time)
    tehran = utc_time.astimezone(tz('Asia/Tehran'))
    print(f"{tehran}\n\n")

def name_catch(url):
    url_name = url.split("/")[-1].split(".")[0]
    return url_name
    
with open('urls.txt', 'r') as file:
    urls = file.read().splitlines()	

for url in urls:
    try:
        usr = input(f"{name_catch(url)} >> ")
        if usr == "n":
            continue
        response = requests.get(url)
        response.raise_for_status()  # بررسی خطا در دریافت
        data = json.loads(response.text)  # تبدیل محتوا به دیکشنری Python
        print("="*80)
        for post in data['posts'][::-1]:
            ussr = input("\n\n==================\n--- Press Enter ---\n==================\n >> ")
            if ussr == "n":
                break
            utc2teh(post['date'])
            print(wipetxt(post['message']))
            #break
     
    except requests.exceptions.RequestException as e:
        print(f"خطا در دریافت فایل: {e}")
        exit()

