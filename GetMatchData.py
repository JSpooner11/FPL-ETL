import pandas as pd
import requests
import json
import datetime
import boto3

# sqs = boto3.client('sqs')
# queue_url = 'SQS_QUEUE_URL'

url = 'https://fantasy.premierleague.com/api/fixtures/'

r = requests.get(url).json()

today_date = datetime.datetime(2022, 1, 15).strftime('%Y-%m-%d')
# today_date = datetime.datetime.now().strftime('%Y-%m-%d')

# print(r)
df = pd.json_normalize(r)

df = df[['kickoff_time']]

# convert kickoff_time to ignore the time
# 1. get the date info
# 2. convert it into a date data type
df['kickoff_date'] = df['kickoff_time'].str[:10]
# df['kickoff_date'] =  pd.to_datetime(df['kickoff_date'])
df['kickoff_date'] = pd.to_datetime(df['kickoff_date']
                                    , format='%Y-%m-%d')

# Get time
df['kickoff_datetime'] = df['kickoff_time'].str[11:19]
df['kickoff_datetime'] = pd.to_datetime(df['kickoff_datetime']
                                        , format='%H:%M:%S')

filt = df.kickoff_date == today_date

# Get max time to send notification to SQS 2 hrs after last game
dftime = df['kickoff_datetime'][filt].max()
dftime = dftime.time()

print(today_date)
print(df[filt])
print(dftime)
# print(df.head)
