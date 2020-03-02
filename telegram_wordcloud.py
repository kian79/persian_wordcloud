from bs4 import BeautifulSoup as Soup
import re, urllib.request, nltk
from pathlib import Path
import requests
import wordcloud_fa

def get_html_files(path:str):
    htmls_path = Path(path).glob('*.html')
    htmls = []

    for p in htmls_path:
        htmls.append(open(p, 'r').read())
    return htmls


dir_path = input("Please enter the absolute path of the directory in which your html files are saved.")
my_html = '\n'.join(get_html_files(dir_path))
my_soup = Soup(my_html,'html.parser')
my_soup = my_soup.find_all('div')
text = ""
for t in my_soup:
    if "text" in t.attrs['class']:
        text +=t.get_text()+" "
my_wc = wordcloud_fa.WordCloudFa(width=1200,height=1200,background_color="white",persian_normalize=True)
my_wc.generate(text)
image = my_wc.to_image()
image.show()
image.save("pashmam.png")