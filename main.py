# Importing all necessary libraries for project
import re
import pandas as pd
import numpy as np
from tweepy import API
from tweepy import OAuthHandler
import twitter_api_info
from textblob import TextBlob

#setting chart limits
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', None)

def authenticate_app():
    auth = OAuthHandler(twitter_api_info.C_KEY, twitter_api_info.C_SECRET)
    auth.set_access_token(twitter_api_info.A_KEY, twitter_api_info.A_SECRET)
    return auth

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def tweet_sentiment(tweet):
    return TextBlob(clean_tweet(tweet)).sentiment.polarity

def collect_tweets():
    all_tweets = []
    first_run = api.search(q = "donald trump", lang = "en", result_type = 'recent', count = 100)
    all_tweets += first_run
    last_tweet_date = first_run[len(first_run) - 1].created_at
    parsed_date = last_tweet_date.strftime("%Y-%m-%d")

    for x in range(9):
        all_tweets += api.search(q = "donald trump", lang = "en", result_type = 'recent', until = parsed_date, count = 100)

    return all_tweets

def create_dataframe(tweets):
    df = pd.DataFrame(data = [tweet.user.screen_name for tweet in tweets], columns = ['User'])
    df['Text'] = np.array([tweet.text for tweet in tweets])
    #df['Sentiment'] = np.array([tweet_sentiment(tweet) for tweet in tweets])
    df['Location'] = np.array([tweet.user.location for tweet in tweets])
    df['Date'] = np.array([tweet.created_at for tweet in tweets])
    df['Sentiment'] = np.array([tweet_sentiment(tweet.text) for tweet in tweets])

    return df

if __name__ == '__main__':
    auth = authenticate_app()
    api = API(auth)
    all_tweets = collect_tweets()

    df = create_dataframe(all_tweets)

    print(df)
