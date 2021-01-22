from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


import twitter_credentials
import numpy as np
import pandas as pd



# # # # TWITTER CLIENT-SIDE # # # #
class TwitterClient():
    def __init__(self, twitter_user = None ):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user


    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweet(self, num_tweet):
        tweet =[]
        for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user).items(num_tweets):
            tweet.append(tweet)
        return tweet
    def get_friend_list(self, num_friends):
        friend_list=[]
        for friend in Cursor(self.twitter_client.friends, id = self.twitter_user).items(num_tweets):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweet(self, num_tweets):
        home_timeline_tweet = []
        for tweet in Cursor(self.twitter_client.home_timeline, id = self.twitter_user).items(num_tweets):
            home_timeline_tweet.append(tweet)
            return home_timeline_tweet


# # # # TWITTER KEYS # # # #

class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.cons_tok, twitter_credentials.cons_sec)
        auth.set_access_token(twitter_credentials.app_tok, twitter_credentials.app_sec)
        return auth


class TwitterStreamer():
    """"
    A class that streams live tweet

    """
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles the Twitter Authentication and the connection to the Twitter streaming API
        listener = TwitterListener(fetched_tweets_filename, hash_tag_list)
        auth = OAuthHandler(twitter_credentials.cons_tok, twitter_credentials.cons_sec)
        auth.set_access_token(twitter_credentials.app_tok, twitter_credentials.app_sec)

        stream = Stream(auth, listener)
# This line filter tweet streams to capture by keyword
        stream.filter(track=hash_tag_list)
#this filter line is overwritten in line "133"




class TwitterListener(StreamListener):
    """"
    A basic listener class that fetches the data from the API

    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename


    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print( "error on_data %s" % str(e))
            return True

    def on_error(self, status_code):
        if status_code == 420:
            # returning false on data method in case rate limit occur : "really important"
           return False
        print(status_code)


filename = "test"
f = open(filename, "w")

headers = "id, len, date, source, likes, retweets, in_reply_to_screen_name, in_to_status_id, in_reply_to_user_id \n"

f.write(headers)

class TweetAnalyzer():
    """"
    Class for tweet analysis
    """
    def tweet_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets ], columns=['tweets'])

        df['id']= np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['in_reply_to_screen_name'] = np.array([tweet.in_reply_to_screen_name for tweet in tweets])
        df['in_reply_to_status_id'] = np.array([tweet.in_reply_to_status_id for tweet in tweets])
        df['in_reply_to_user_id'] = np.array([tweet.in_reply_to_user_id for tweet in tweets])

        #the loops are essential in the data presentation ('for tweet in tweets')

        return df




if __name__ == "__main__":

#main function of the program == The switch
    twitter_client = TwitterClient()
    api =twitter_client.get_twitter_client_api()
    tweet_analyzer = TweetAnalyzer()

    tweets =api.user_timeline(screen_name ='marykaycanada', count = 1000 )

    print(dir(tweets[0])) # 'dir' function makes you see all the availabe call keywords
   #  print(tweets[2].retweet_count) # method to count all retweets by a particular user
    df = tweet_analyzer.tweet_to_data_frame(tweets)
    np.savetxt(r'elsa_project.csv', df.values, fmt='%s', newline='n', header='id,len, date, source, likes, retweets, in_reply_to_screen_name,in_reply_to_status_id,in_reply_to_user_id', delimiter='\t', comments="")
    #df.to_csv(r'c:\data\pandas.txt', header=None, index=None, sep='\t', mode='a')

    print(df.head(1000))

    # Authenticate using config.py and connect to Twitter Streaming API
    hash_tag_list = ['make up', 'foundation', 'powder', 'concealer', 'eye brush', 'lip stick']
    fetched_tweets_filename ='tweets.txt'

    #twitter_client = TwitterClient('marykaycanada')


f.close()