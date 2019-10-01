import nltk

nltk.download('book')
from nltk.corpus import gutenberg


for fileid in gutenberg.fileids():
    # fdist2 = nltk.FreqDist(gutenberg.words(fileid))
    n_chars = len(gutenberg.raw(fileid))
    n_words = len(gutenberg.words(fileid))
    n_sent = len(gutenberg.sents(fileid))
    print(int(n_chars / n_words), fileid)
    # print(int(n_chars / n_words), int(n_words / n_sent), fileid)




"""
nltk.download('book')
from nltk.corpus import PlaintextCorpusReader

corpus_root = 'D:/works/faqbot/db'
wl = PlaintextCorpusReader(corpus_root, '.*')
print(wl.fileids())"""

'''
from nltk.book import genesis

print(genesis.fileids())


for fileid in genesis.fileids():
   if fileid == "english-kjv.txt":
           frq_words=genesis.words('english-kjv.txt')
           contains_jah = sorted(term for term in set(genesis) if 'Jehovah' in term)
           print(contains_jah)

    n_chars = len(genesis.raw(fileid))
    # print(genesis.raw(fileid))
    print(n_chars)
    n_words = len(genesis.words(fileid))
    print(n_words)
    # print(genesis.words(fileid))
    n_sent = len(genesis.sents(fileid))
    # print(n_sent)
    print(genesis.sents(fileid))
    print(int(n_chars / n_words), int(n_words / n_sent), fileid)
'''
