from datetime import datetime, timedelta
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

def parser(lang, date, start, country):

    # driver = webdriver.Chrome('./chromedriver_111')

    service = Service(executable_path='./chromedriver_111')
    driver = webdriver.Chrome(service=service)

    user_agent = UserAgent(verify_ssl=False,
                           fallback='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36').chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("user-agent=" + user_agent)

    driver.implicitly_wait(5)

    driver.get(f'https://www.google.com/search?q=covid&lr=lang_{lang}&cr=country{country}&hl={lang}&tbs=lr:lang_1{lang},ctr:country{country},cdr:1,cd_min:{date},cd_max:{date}&tbm=nws&start={start}&sa=N&biw=1440&bih=821&dpr=2')

    time.sleep(5 + random.uniform(1, 30))

    list = []

    for element in driver.find_elements(By.XPATH, '//*[@class="WlydOe"]'):
        # link = element.get_attribute('href')
        # portal = element.find_elements(By.XPATH, './/*[@class="CEMjEf NUnG9d"]/span')[0].text
        title = element.find_elements(By.XPATH, './/*[@class="mCBkyc ynAwRc MBeuO nDgy9d"]')[0].text
        details = element.find_elements(By.XPATH, './/*[@class="GI74Re nDgy9d"]')[0].text
        # list.append([date, link, portal, title, details])
        list.append([date, title, details])

    # return pd.DataFrame(list, columns=['date', 'link', 'portal', 'title', 'details'])

    return pd.DataFrame(list, columns=['date', 'title', 'details'])

def parser_interval(lang, date_start, date_end, country):

    start = datetime.strptime(date_start, '%m/%d/%Y')
    end = datetime.strptime(date_end, '%m/%d/%Y')
    dates = [(start + timedelta(days=x)).strftime('%m/%d/%Y') for x in range(0, (end-start).days)]
    dates = ['/'.join([j.replace('0', '') if j[0] == '0' else j for j in i.split('/')]) for i in dates]
    intervals = [(datetime.strptime(date_start, '%m/%d/%Y') + timedelta(days=10)).strftime('%m/%d/%Y'), (datetime.strptime(date_start, '%m/%d/%Y') + timedelta(days=20)).strftime('%m/%d/%Y')]
    intervals = ['/'.join([j.replace('0', '') if j[0] == '0' else j for j in i.split('/')]) for i in intervals]

    data = pd.DataFrame(columns=['date', 'title', 'details'])

    for date in dates:

        if date in intervals:
            time.sleep(60)

        start = 0
        data_temp = parser(lang, date, start, country)

        while not data_temp.empty:
            data = pd.concat([data, data_temp]).reset_index(drop=True)
            data_temp = parser(lang, date, start, country)
            # df.to_csv('covid.csv', index=False)
            # df = pd.read_csv('covid.csv')
            start += 10
        print(date)
    return data




try:
    df = pd.read_csv('covid.csv')
except:
    df = pd.DataFrame(columns=['date', 'title', 'details'])
    df.to_csv('covid.csv', index=False)

df.date.value_counts().sort_index()

date_start = '2/19/2023'
date_end = '3/21/2023'
lang = 'en'
country = 'US'

df_ad = parser_interval(lang, date_start, date_end, country)
df_ad.date.value_counts().sort_index()

df = pd.concat([df, df_ad]).reset_index(drop=True)
df = df.loc[~df[['title', 'details']].duplicated()]
df.to_csv('covid.csv', index=False)


df['date'] = pd.to_datetime(df.date)
df.to_csv('covid.csv', index=False)

