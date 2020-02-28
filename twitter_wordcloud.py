import tweepy as tweepy
from wordcloud_fa import WordCloudFa
import numpy as np
from PIL import Image

path = "/home/kiankr/my_tweets.txt"
mask_path = "/home/kiankr/Desktop/twitter_mask.png"
background_color = "white"
mask_array = np.array(Image.open(mask_path))

consumer_key = "qJBw4NnM1yaAhuD6tWndoVurP"
consumer_secret = "Riw9EE79E4LpUTipVEkAlhBrx2DdE8p75ZnUnv7QgMpa1ZMQ4g"
access_key = "741947563855745024-84QUfeCOOuXnRrs9y3pqkTM0wppQdQc"
access_secret = "gmXKfAV785JssW5jwyZ9Am4ODHMa3q8AopOBsvDMlP3Zu"


def get_text_from_file(path):
    with open(path, 'r') as file:
        text = file.read()
        return text

def get_tweets_from_user(username):
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)


my_wc = WordCloudFa(width=1200, height=1200, background_color=background_color, mask=mask_array)
my_wc.generate(get_text_from_file(path))
image = my_wc.to_image()
