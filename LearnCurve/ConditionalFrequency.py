from typing import re

import nltk

nltk.download('book')
from nltk.corpus import brown
from nltk.corpus import reuters

items = ['apple', 'kiwi', 'cabbage', 'cabbage', 'apple', 'potato']
print(nltk.FreqDist(items))
c_items = [('F', 'apple'), ('F', 'apple'), ('F', 'kiwi'), ('V', 'cabbage'), ('V', 'cabbage'), ('V', 'potato')]
cfd = nltk.ConditionalFreqDist(c_items)
print(cfd)
cfd.conditions()
print(cfd['F'])

cfd = nltk.ConditionalFreqDist(
    [(genre, word) for genre in brown.categories() for word in brown.words(categories=genre)])
print("what is in cfr", cfd.items())
print(cfd.conditions())
cfd.tabulate(conditions=['government'], samples=['leadership'])
news_fd = cfd['news']
print(news_fd)
print(news_fd.most_common(3))

news_text = brown.words(categories='news')

fde = nltk.FreqDist(w.lower() for w in news_text)
print("fde value", fde.values())
print("fde has", fde.tabulate())
modals = ['can', 'could', 'may', 'might', 'must', 'will']
for m in modals:
    print(m + ':', fde[m], end=' ')

# How many times zinc in genre zinc

print(reuters.fileids('zinc'))
print (nltk.FreqDist(reuters.words(categories='zinc')))
