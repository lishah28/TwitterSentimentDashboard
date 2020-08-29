import pandas as pd
import numpy as np

from tweepy import API
from tweepy import OAuthHandler
from datetime import datetime
from tweepy import Stream
from tweepy.streaming import StreamListener

import twitter_api_info

def authenticate_app():
    auth = OAuthHandler(twitter_api_info.C_KEY, twitter_api_info.C_SECRET)
    auth.set_access_token(twitter_api_info.A_KEY, twitter_api_info.A_SECRET)
    return auth

def create_dataframe(tweets):
    df = pd.DataFrame(data = [tweet.user.screen_name for tweet in tweets], columns = ['User'])
    df['Text'] = np.array([tweet.text for tweet in tweets])
    #df['Date'] = np.array([tweet.created_at for tweet in tweets])

    return df


if __name__ == '__main__':
    auth = authenticate_app()
    api = API(auth)
    all_tweets = []
    first_run = api.search(q = "donald trump", lang = "en", result_type = 'recent', count = 100)
    all_tweets += first_run
    last_tweet_date = first_run[len(first_run) - 1].created_at
    parsed_date = last_tweet_date.strftime("%Y-%m-%d")
    print(parsed_date)
    for x in range(9):
        all_tweets += api.search(q = "donald trump", lang = "en", result_type = 'recent', until = parsed_date, count = 100)
    df = create_dataframe(all_tweets)

    print(df)



