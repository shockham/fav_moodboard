import os
import tweepy
import requests
from configparser import ConfigParser

config = ConfigParser()
config.read('gen.ini')

consumer_key = config['twitter']['consumer_key']
consumer_secret = config['twitter']['consumer_secret']
access_token_key = config['twitter']['access_token_key']
access_token_secret = config['twitter']['access_token_secret']


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth)

img_dir = "./img"

if not os.path.isdir(img_dir):
    os.mkdir(img_dir)

def process_tweet(tweet):
    if 'media' in tweet.entities:
        media_url = tweet.entities['media'][0]['media_url']
        file_name = "%s/%s" % (img_dir, media_url.split('/')[-1])

        r = requests.get(media_url)

        if not os.path.exists(file_name):
            print('saving: %s' % file_name)
            with open(file_name, 'wb') as f:
                f.write(r.content)
        else:
            print('skipping: %s' % file_name)

page=0
while True:
    favourites = api.favorites(page=page)
    if not favourites:
        break

    for tweet in favourites:
        process_tweet(tweet)

    page += 1
