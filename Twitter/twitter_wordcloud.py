import re
import tweepy as tweepy
from wordcloud_fa import WordCloudFa
import numpy as np
from PIL import Image
from datetime import datetime
import os

mask_path = "twitter_mask.png"
background_color = "white"
# for bellow keys you should have twitter developer account you can have by simply asking twitter in
# https://developer.twitter.com/
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret= ""
def initial_api():
    api_file = open("/home/kiankr/Desktop/twitter_api.txt", 'r') # I copied my apis in this file and use them from here
    # because i didn't want anyone to see them:)
    my_apis = api_file.read().split('\n')
    print(my_apis)
    consumer_key = my_apis[0][my_apis[0].index('=') + 1:].strip()  # Your consumer key
    consumer_secret = my_apis[1][my_apis[1].index('=') + 1:].strip()  # your consumer secret key
    access_key = my_apis[2][my_apis[2].index('=') + 1:].strip()  # your access_key
    access_secret = my_apis[3][my_apis[3].index('=') + 1:].strip()  # your access secret
    print(consumer_key)


def get_text_from_file(path):
    with open(path, 'r') as file:
        text = file.read()
        return text


def get_tweets_from_user(screen_name: str):  # You can use this for getting tweets from twitter using twitter developer
    # account apis.
    initial_api()
    print("Starting to get tweets.")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    print("api initialized.")
    all_tweets = []
    new_tweets = api.user_timeline(screen_name=screen_name, count=180)

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


def removeWeirdChars(text0):
    weridPatterns = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u'\U00010000-\U0010ffff'
                               u"\u200d"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\u3030"
                               u"\ufe0f"
                               u"\u2069"
                               u"\u2066"
                               u"\u200c"
                               u"\u2068"
                               u"\u2067"
                               "]+", flags=re.UNICODE)
    return weridPatterns.sub(r'', text0)


def get_words(c_tweet):  # get all of the words in a tweet and return the list of words
    word_list = c_tweet.split()
    return word_list


def get_tweets(b_text):  # get text and return all of the tweets as a list
    tweet_list = b_text.split("\n")
    return tweet_list


def remove_bad_tweets(tweet_list):  # this method removes bad tweets that we dont need like retweets, etc
    for a_tweet in tweet_list:
        if "RT" in tweet_list:
            print("retweets : ", a_tweet)
            a_tweet = ""
    return tweet_list


def remove_bad_words(a_text: str):
    for i in range(len(a_text)):
        if a_text[i].startswith("@"):
            a_text[i] = ""
        elif ord(a_text[i][0]) < 328:
            a_text[i] = ""
        elif "." in a_text[i]:
            a_text[i] = ""
        elif "می" in a_text[i]:
            a_text[i] = ""
        elif len(a_text[i]) < 3:
            a_text[i] = ""
        elif '!' in a_text[i]:
            a_text[i] = ""
        elif 'اومد' in a_text[i]:
            a_text[i] = ""
        elif 'داشت' in a_text[i]:
            a_text[i] = ""
        elif 'دار' in a_text[i]:
            a_text[i] = ""
        elif 'کن' in a_text[i]:
            a_text[i] = ""
        elif 'شد' in a_text[i]:
            a_text[i] = ""
        elif 'من' in a_text[i]:
            a_text[i] = ""
        elif 'زد' in a_text[i]:
            a_text[i] = ""
        elif 'این' in a_text[i]:
            a_text[i] = ""
        elif 'بش' in a_text[i]:
            a_text[i] = ""
        elif 'باش' in a_text[i]:
            a_text[i] = ""
        elif 'رسید' in a_text[i]:
            a_text[i] = ""
        elif '(' in a_text[i]:
            a_text[i] = ""
        elif ')' in a_text[i]:
            a_text[i] = ""
    return a_text


text = ""
anw = input("How do you want to get tweets?from file or username?<f for file and u for username>")
while True:
    if anw == 'f':
        path = input("Enter absolute path of your txt file:")
        text = get_text_from_file(path)  # To get tweets from a file (if you dont have twitter api you can use this.
        break
    elif anw == 'u':
        username = input("Enter id:")
        text = get_tweets_from_user(username)  # to get tweets of a specific user by its username
        break
    else:
        print("you should enter f or u!")

text = get_tweets(text)
text = remove_bad_tweets(text)
text = "\n".join(text)
text = get_words(text)
print(len(text))
text = remove_bad_words(text)
print(len(text))
text1 = "\n".join(text)
text1 = removeWeirdChars(text1)
mask_array = np.array(Image.open(mask_path))
my_wc = WordCloudFa(width=1200, height=1200, background_color=background_color, mask=mask_array, persian_normalize=True,
                    repeat=False, collocations=True, no_reshape=False)
photo_path = input("where do you want to save the photo?enter absolute path.")
open("edited_tweets.txt", "w").write(text1)
my_wc.add_stop_words_from_file("stop_words_kian.txt")
my_wc.generate(text1)
image = my_wc.to_image()
image.show()
filename = datetime.now().strftime("%Y-%m-%d-%H")
image.save(photo_path+'/{time}_photo.png'.format(time=filename))
