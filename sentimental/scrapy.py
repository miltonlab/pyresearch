# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""
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
# for after use with sentimental140
tweets['language'] = [t['language'] for t in data]
tweets['contry'] = [t['place']['country'] if t['place'] else None for t in data]
