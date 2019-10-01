import nltk
from nltk.book import *

n = len(text6)
print(sorted(set(text6)))
u = len(set(text6))
wc = n / u
print(wc)
contains_z = sorted(term for term in set(text6) if 'z' in term)
print(len(contains_z))
contains_pt = sorted(term for term in set(text6) if 'pt' in term)
print(len(contains_pt))
# task 5
# title_words = [word for word in set(text6) if word.istitle()]
title_words = sorted(t for t in set(text6) if t.istitle())
print(title_words)
print(len(title_words))
text6freq = nltk.FreqDist(text6)
print(text6freq['ARTHUR'])
print(text3.concordance("Adam"))
