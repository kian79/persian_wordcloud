# from Twitter.twitter_wordclou import remove_bad_words,removeWeirdChars
import datetime

import numpy as np
from PIL import Image
from bs4 import BeautifulSoup as Soup
import re, urllib.request, nltk
from pathlib import Path
import requests
import wordcloud_fa


def remove_bad_words(a_text: str):
    for i in range(len(a_text)):
        if '@' in a_text[i]:
            a_text[i] = ""
        elif 'RT' in a_text[i]:
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
        elif "ببین" in a_text[i]:
            a_text[i] = ""
        elif "دید" in a_text[i]:
            a_text[i] = ""
        elif "بود" in a_text[i]:
            a_text[i] = ""
    return a_text


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


def get_html_files(path: str):
    htmls_path = Path(path).glob('*.html')
    htmls = []
    print("reading html files.")
    for p in htmls_path:
        htmls.append(open(p, 'r').read())
    print("HTML files read.")
    return htmls


file_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
dir_path = input("Please enter the absolute path of the directory in which your html files are saved.")
my_html = '\n'.join(get_html_files(dir_path))
my_html = removeWeirdChars(my_html)
my_soup = Soup(my_html, 'html.parser')
print("finding all divs.")
my_soup = my_soup.find_all('div')
print("All divs found")
text = ""
print("Getting text class from divs.")
for t in my_soup:
    if "text" in t.attrs['class']:
        text += t.get_text() + " "
print("Text is now ready!writing on a file.")
open(f"msg_tele_{file_time}.txt", 'w').write(text)
print("writed on a file. generating wordcloud...")
mask_array = np.array(Image.open('tele_mas1.jpg'))
my_wc = wordcloud_fa.WordCloudFa(width=1400, height=1400, background_color="white", persian_normalize=True,
                                 mask=mask_array)
my_wc.add_stop_words_from_file("stop_words_kian.txt")
text = text.split()
text = remove_bad_words(text)
text = '\n'.join(text)
my_wc.generate(text)
image = my_wc.to_image()
image.show()
image.save(f"Images/{file_time}.png")
