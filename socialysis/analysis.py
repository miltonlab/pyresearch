# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""

#lectura de datos 

import json
dataset_path = "dataset-230415-11.56.txt"
data = []
f = open(dataset_path, "r")
input('hi')
for line in f:
	try:
		tweet = json.loads(line)
		data.append(tweet)
	except Exception as ex:
		print("Error :", ex)
		continue
print(len(data))
f.close()
import pandas as pd
tweets = pd.DataFrame()
tweets['text'] = [t['text'] for t in data]
tweets['lang'] = [t['lang'] for t in data]
tweets['country'] = [t['place']['country'] if t['place'] else None for t in data]

# function to search keyword programming languag in text
import re
def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word+" ", text)
    if match:
        return True
    return False
				
# En la columna text de nuestro DataFrame buscamos las ocurrencias de cada palabra a analizar 
# ... Incluir posible grafico
tweets['python'] = tweets['text'].apply(lambda tweet: word_in_text('python', tweet))
tweets['java'] = tweets['text'].apply(lambda tweet: word_in_text('java', tweet))
tweets['javascript'] = tweets['text'].apply(lambda tweet: word_in_text('javascript', tweet))

# Contabilizando 
print (tweets['python'].value_counts()[True])
print (tweets['java'].value_counts()[True])
print (tweets['javascript'].value_counts()[True])

tweets_by_prg_lang = (tweets['python'].value_counts()[True], tweets['java'].value_counts()[True], tweets['javascript'].value_counts()[True])
prg_langs = ('python', 'java', 'javascript')
x = list(range(len(prg_langs)))

# Plotting
import matplotlib.pyplot as plt
fig, axis =  plt.subplots()
plt.bar(x, tweets_by_prg_lang, 0.8, alpha=1, color='g')

axis.set_ylabel('Numero de tweets', fontsize=15)
axis.set_title('Ranking: python vs. java vs javascript (Raw data)')
axis.set_xticks([p + 0.4 * 0.8 for p in x])
axis.set_xticklabels(prg_langs)
plt.grid()