import tweepy as tw
import os
import pandas as pd
import random

consumer_key= ''
consumer_secret= ''
access_token= ''
access_token_secret= ''
bearer = ''
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

df = pd.DataFrame(columns=["date","text"])
#filters = "covid OR vaccination OR pfizer OR johnson OR moderna OR astrazenica OR covid-19 OR covid19 OR corona OR coronavirus OR vaccine OR #SARSCoV2 OR #COVID OR #Vaccinated OR #COVID19 OR Quarantine -filter:retweets"
filters = "#SARSCoV2 OR #COVID OR #Vaccinated OR #COVID19 OR #vaccine OR #moderna OR #pfizer OR #Astrazenica OR #antibodies OR #antibody -filter:retweets"
all_dates = ["2021-11-25","2021-11-26","2021-11-27"]
for date in all_dates:
    print(date)
    if (date == all_dates[2]):
        tweets = tw.Cursor(api.search_tweets,q = filters,lang="en",until=date,tweet_mode="extended").items(334)
    else:
        tweets = tw.Cursor(api.search_tweets,q = filters,lang="en",until=date,tweet_mode="extended").items(333)
    for z, tweet in enumerate(tweets):
        df = df.append({"date":tweet.created_at,"text":tweet.full_text}, ignore_index=True)

df.to_csv("tweets.csv")


