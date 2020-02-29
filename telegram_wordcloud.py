from bs4 import BeautifulSoup as Soup
import re, urllib.request, nltk

url = 'http://google.com'
html = urllib.request.urlopen(url).read()  # make the request to the url
soup = Soup(html)  # using Soup on the responde read
for script in soup(["script", "style"]):  # You need to extract this <script> and <style> tags
    script.extract()  # strip them off
text = soup.getText()  # this is the method that I had like 40 min problems
text = text.encode('utf-8')  # make sure to encode your text to be compatible
# raw = nltk.clean_html(document)
print(text)