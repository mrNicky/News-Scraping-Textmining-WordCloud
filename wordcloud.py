#--- Scraping
import requests
import re
from bs4 import BeautifulSoup

#--- Preprocessing and TextMining
import pandas as pd
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
stopwords = stopwords.words('french')

#--- DataViz
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud


#Requests and BeautifulSoup
r = requests.get("https://www.lemonde.fr/")
soup = BeautifulSoup(r.text, 'html.parser')
results = soup.find_all('span', attrs={'class':'article__title-label'})
titre = [results[i].text for i in range(len(results))]

#French STOP WORDS and Ponctuations
pat = r'\b(?:{})\b'.format('|'.join(stopwords))
p = r'[^\w\s]+'

#Create a DataFrame
df = pd.DataFrame(titre, columns=['titre'])
df['titre'] = df['titre'].str.lower()
df['titre'] = df['titre'].str.replace(pat, '')
df['titre'] = df['titre'].str.replace(p, '')

#Sentences to words and Preprocessing
word_count = pd.Series(' '.join(df.titre).split(), name="mots")
df = pd.DataFrame(word_count)
mask = (df['mots'].str.len() >= 3)
df = df.loc[mask]

#Show wordCloud top 500 words and save image file
top_mots = df.mots.value_counts().iloc[:500].index
w = WordCloud(width=1000, height=300, max_words=100, contour_width=3, contour_color='stwhiteeelblue').generate(' '.join(top_mots))
plt.figure( figsize=(15,7), facecolor='k')
plt.imshow(w)
plt.axis("off")
plt.savefig('wordcloud.png', facecolor='k', bbox_inches='tight')
plt.show()
