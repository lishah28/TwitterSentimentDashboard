import pandas as pd
import numpy as np

from tweepy import API
from tweepy import OAuthHandler
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
    df['Location'] = np.array([tweet.user.location for tweet in tweets])

    return df


if __name__ == '__main__':
    auth = authenticate_app()
    api = API(auth)

    tweets = api.search(q = "pokemon card", lang = "en", result_type = 'recent', count = 10)

    df = create_dataframe(tweets)

    print(df)



