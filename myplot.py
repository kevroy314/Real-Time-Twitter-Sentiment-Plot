# myplot.py
from bokeh.plotting import figure, curdoc
from bokeh.driving import linear
from bokeh.models import Span
from bokeh.palettes import Dark2_5 as palette
from bokeh.models import BoxAnnotation

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from tweetfeels import TweetFeels

import pandas as pd

from datetime import timedelta, datetime
from threading import Thread

import random
import time
import itertools
import sys

from fragmenter import generate_string_fragments, slugify

#Variables that contains the user credentials to access Twitter API 
access_token = "548017247-WGOckwwa33tD4a49G2Sf2ubExZM9qiF7awSePnic"
access_token_secret = "rwmOnGksWhKEVIRoKtXilcUEZmnB6SxQ8wFT7CoW2FeTo"
consumer_key = "2UQPiHEaCsx5L96KlTUVISweq"
consumer_secret = "pfOKhAgpRpxdxu2SoY9xybKvHxu5m2uIolpg10WfWbi3NBTQDm"

login = [consumer_key, consumer_secret, access_token, access_token_secret]

tracking_keys = [
    generate_string_fragments('beto o\'rourke') + ['@BetoORourke'], 
    list(set(generate_string_fragments('ted cruz')) - set(['ted', 'Ted'])) + ['@tedcruz']
    ]

for idx in range(0, len(tracking_keys)):
    print(f'Searching for {tracking_keys[idx]} in stream {idx}')
tracking_names = ['Beto O\'Rourke', 'Ted Cruz']

db_names = ['{0}.sqlite'.format(slugify(name)) for name in tracking_names]

feels = [TweetFeels(login, tracking=tracking, db=dbname) for tracking, dbname in zip(tracking_keys, db_names)]

p = figure(sizing_mode='stretch_both')
p.legend.location = "top_left"
colors = itertools.cycle(palette) 

rs = [p.line([], [], color=color, line_width=2, legend=name) for name, color in zip(tracking_names, colors)]

# Horizontal line
hline = Span(location=0, dimension='width', line_color='black', line_width=3)
pos_box = BoxAnnotation(left=-sys.maxsize, right=sys.maxsize, top=1, bottom=0, fill_color='green', fill_alpha=0.1)
neg_box = BoxAnnotation(left=-sys.maxsize, right=sys.maxsize, top=0, bottom=-1, fill_color='red', fill_alpha=0.1)

p.renderers.extend([hline, pos_box, neg_box])

dss = [r.data_source for r in rs]

most_recent_sentiment = [0 for _ in rs]

def print_feels(seconds=10):
    global most_recent_sentiment, feels
    while go_on:
        time.sleep(seconds)
        for idx, feel in enumerate(feels):
            try:
                data = {s.end: s.volume for s in feels[idx].sentiments(nans=True)}
                df = pd.DataFrame.from_dict(data, orient='index')
                df[0].plot(kind='area', title='Volume')
                most_recent_sentiment[idx] = feel.sentiment.value
                print(f'[{time.ctime()}] [{tracking_names[idx]}] Sentiment Score: {most_recent_sentiment[idx]}')
            except UnboundLocalError as e:
                pass
        plt.gcf().set_size_inches(18.5, 10.5)
        plt.savefig('testplot.png', dpi=100)

go_on = True
t = Thread(target=print_feels)
for feel in feels:
    feel.start(selfupdate=5)
t.start()

@linear()
def update(step):
    global most_recent_sentiment
    for ds, sent in zip(dss, most_recent_sentiment):
        ds.data['x'].append(step)
        ds.data['y'].append(sent)
        ds.trigger('data', ds.data, ds.data)

curdoc().add_root(p)

# Add a periodic callback to be run every 500 milliseconds
curdoc().add_periodic_callback(update, 500)