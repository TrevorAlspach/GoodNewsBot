import tweepy
import nltk.sentiment
from os import environ
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

followed_accounts = {"CNN_ID": "759251", "MSNBC_ID": "2836421", "ABC_ID": "28785486", "CBS_ID": "15012486",
                     "NBC_ID": "14173315", "TEDTalks_ID": "15492359", "NYTimes_ID": "807095", "BBC_ID": "742143",
                     "WSJ_ID": "3108351", "WashPost_ID": "2467791", "Guardian_ID": "87818409"}

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if from_creator(status):
            try:
                sia = nltk.sentiment.SentimentIntensityAnalyzer()
                print(sia.polarity_scores(status.text)["compound"])
                compound_score = sia.polarity_scores(status.text)["compound"]
                if compound_score > 0.0:
                    api.retweet(status.id)
                else:
                    print("Sentiment value less than 0.0, not tweeted")
            except BaseException as e:
                print("Error_On_Data %s" % str(e))

            print(status.text)
            return True
        return True

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

myStream.filter(follow=list(followed_accounts.values()))
