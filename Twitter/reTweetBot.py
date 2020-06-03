import tweepy
from time import sleep
from random import randint

#Authenticate to Twitter
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Where q='#example', change #example to whatever hashtag or keyword you want to search.
# Where items(5), change 5 to the amount of retweets you want to tweet.
# Make sure you read Twitter's rules on automation - don't spam!
for tweet in tweepy.Cursor(api.search, q='#COVID19').items(500):
    try:
        print('\nRetweet Bot found tweet by @' + tweet.user.screen_name + '. ' + 'Attempting to retweet.')
        tweet.retweet()
        print('Retweet published successfully.')

        # Where sleep(10), sleep is measured in seconds.
        # Read Twitter's rules on automation. Don't spam!
        sleep(randint(50,100))

    # Some basic error handling. Will print out why retweet failed, into your terminal.
    except tweepy.TweepError as error:
        print('\nError. Retweet not successful. Reason: ')
        print(error.reason)

    except StopIteration:
        break