from tweetfeels import TweetFeels
from threading import Thread
import time

access_token = "548017247-WGOckwwa33tD4a49G2Sf2ubExZM9qiF7awSePnic"
access_token_secret = "rwmOnGksWhKEVIRoKtXilcUEZmnB6SxQ8wFT7CoW2FeTo"
consumer_key = "2UQPiHEaCsx5L96KlTUVISweq"
consumer_secret = "pfOKhAgpRpxdxu2SoY9xybKvHxu5m2uIolpg10WfWbi3NBTQDm"

login = [consumer_key, consumer_secret, access_token, access_token_secret]

def print_feels(feels=None, seconds=10):
    time.sleep(seconds)
    print(f'[{time.ctime()}] Sentiment Score: {feels.sentiment.value}')
    return False

tesla_feels = TweetFeels(login, tracking=['tesla', 'tsla', 'gigafactory', 'elonmusk'], db='tesla.sqlite')
tesla_feels.start(seconds=120)

time.sleep(125)

import pandas as pd
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
data1 = {s.end: s.value for s in tesla_feels.sentiments(delta_time=timedelta(minutes=15), nans=True)}
data2 = {s.end: s.volume for s in tesla_feels.sentiments(delta_time=timedelta(minutes=15), nans=True)}
df1 = pd.DataFrame.from_dict(data1, orient='index')
df2 = pd.DataFrame.from_dict(data2, orient='index')
fig, axes = plt.subplots(nrows=2, ncols=1)
fig.set_size_inches(15, 5)
plt.subplot(211).axes.get_xaxis().set_visible(False)
df1[0].plot(kind='line', title='Tesla Sentiment')
plt.subplot(212)
df2[0].plot(kind='area', title='Volume')