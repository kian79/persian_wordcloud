import tweepy as tweepy
from wordcloud_fa import WordCloudFa
import numpy as np
from PIL import Image

path = "/home/kiankr/my_tweets.txt"
mask_path = "/home/kiankr/Desktop/twitter_mask.png"
background_color = "white"

# for bellow keys you should have twiiter developer account you can have by simply asking twitter in
# https://developer.twitter.com/
consumer_key = ""  # Your consumer key
consumer_secret =""
access_key = ""
access_secret = ""


def get_text_from_file(path):
    with open(path, 'r') as file:
        text = file.read()
        return text


def get_tweets_from_user(username):
    print("Starting to get tweets.")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    print("api initialized.")
    all_tweets = []
    new_tweets = api.user_timeline(screen_name=username, count=180)

    all_tweets.extend(new_tweets)
    oldest_tweet_id = all_tweets[-1].id - 1

    while len(new_tweets):
        print("getting tweets before ", oldest_tweet_id)
        new_tweets = api.user_timeline(screen_name=username, count=180, max_id=oldest_tweet_id)
        all_tweets.extend(new_tweets)
        oldest_tweet_id = all_tweets[-1].id - 1
        print("{} tweets downloaded!".format(len(all_tweets)))
    text = "\n".join(list(map(lambda x: x.text, all_tweets)))
    my_file = open("/home/kiankr/Desktop/{}_tweets1.txt".format(username), 'w')
    my_file.write(text)
    return text


username = "kian_kr"
tweets = get_tweets_from_user(username)

mask_array = np.array(Image.open(mask_path))

my_wc = WordCloudFa(width=1200, height=1200, background_color=background_color, mask=mask_array)
my_wc.generate(tweets)
image = my_wc.to_image()
image.show()
image.save('/home/kiankr/Documents/images/{}_photo.png'.format(username))
