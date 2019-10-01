from _ast import Dict

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# example_sent = "This is a sample sentence, showing off the stop words filtration."
example_sent = "A U.S. Treasury official said there are no current plans to stop Chinese companies from listing on " \
               "U.S. " \
               "exchanges, a day after a report that the Trump administration is discussing ways to limit U.S. " \
               "investors’ portfolio flows into China.“The administration is not contemplating blocking Chinese " \
               "companies from listing shares on U.S. stock exchanges at this time,” Treasury spokeswoman Monica " \
               "Crowley said in an emailed statement on Saturday.Crowley was responding to Friday’s Bloomberg News " \
               "report on various measures under consideration by the U.S., including delisting Chinese companies from " \
               "U.S. exchanges. The report unnerved markets, with the S&P 500 Index closing about 0.5% lower. " \
               "U.S.-listed shares of China-based companies, such as Alibaba Group Holding and Baidu Inc., tumbled. "
stop_words = set(stopwords.words('english'))

word_tokens = word_tokenize(example_sent)

filtered_sentence = [w for w in word_tokens if not w in stop_words]

# for w in word_tokens:
#   if w not in stop_words:
#      filtered_sentence.append(w)

print(word_tokens)
print(filtered_sentence)

freqTable = dict()
print("freqTable Initialized", freqTable)
for word in word_tokens:
    word = word.lower()
    if word in stop_words:
        continue
    if word in freqTable:
        freqTable[word] += 1
    #    print("freqTable appended > +1", freqTable)
    else:
        freqTable[word] = 1
    #   print("freqTable appended just 1", freqTable)
print(freqTable)

sentences = sent_tokenize(example_sent)
print(sentences)
sentValue = dict()
print("sentValue", sentValue)
for sentence in sentences:
    for wordValue in freqTable:
        #   print(wordValue[0])
        if wordValue[0] in sentence.lower():
            #    print("sentence[:12]", sentence[:12])
            if sentence in sentValue:
                sentValue[sentence] += wordValue[1]
            else:
                sentValue[sentence] = wordValue[1]
                print("sentValue", sentValue)
sumValues = 0
for s in sentValue:
    sumValues += sentValue[s]

# Average value of a sentence from original text
average = int(sumValues / len(sentValue))
summary = ''
for sentence in sentences:
    if sentence in sentValue and sentValue[sentence] > (1.5 * average):
        summary += " " + sentence
        print("summary", summary)
