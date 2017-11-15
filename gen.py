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

image_html = ""

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

        return "<img src=\"%s\"/>\n" % file_name
    else:
        return ""

def create_page(image_html):
    html = """
    <!DOCTYPE html>
    <html>
        <head></head>
        <body>
            %s
        </body>
    </html>
    """ % image_html

    with open('index.html', 'wb') as f:
        f.write(bytes(html, 'utf-8'))

for tweet in tweepy.Cursor(api.favorites).items():
    image_html += process_tweet(tweet)

create_page(image_html)
