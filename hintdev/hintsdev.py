import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords')
nltk.download('punkt')


def readtextfromfile(file_path):
    file = open(file_path, 'r')
    return file.read()


def create_frequency_table(text_string) -> dict:
    stopWords = set(stopwords.words("english"))
    words = nltk.word_tokenize(text_string)
    ps = PorterStemmer()
    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    return freqTable


def score_sentences(sentences, freqTable) -> dict:
    sentencevalue = dict()
    for sentence in sentences:
        word_count_in_sentence = (len(nltk.word_tokenize(sentence)))
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                if sentence[:100] in sentencevalue:
                    sentencevalue[sentence[:100]] += freqTable[wordValue]
                else:
                    sentencevalue[sentence[:100]] = freqTable[wordValue]
    sentencevalue[sentence[:100]] = sentencevalue[sentence[:100]] // word_count_in_sentence
    return sentencevalue


def find_average_score(sentencevalue) -> int:
    sumValues = 0
    for entry in sentencevalue:
        sumValues += sentencevalue[entry]
    average = int(sumValues / len(sentencevalue))
    return average


def generate_summary(sentences, sentencevalue, threshold):
    sentence_count = 0
    summary = ''
    for sentence in sentences:
        if sentence[:100] in sentencevalue and sentencevalue[sentence[:100]] > threshold:
            summary += " " + sentence
            sentence_count += 1
    return summary


paragraph = readtextfromfile('input.txt')
print("###############RAW TEXT##################\n", paragraph, "\n################################")

word_freq_table = create_frequency_table(paragraph)
print("###############Word frequency##################\n", word_freq_table)

print("###############Tokenization##################\n")
sentences = nltk.sent_tokenize(paragraph)
for sentence in sentences:
    print(sentence)

print("###############Scoring Sentences##################\n")
scoresentences = score_sentences(sentences, word_freq_table)
print(scoresentences)

print("###############Finding Thershold##################\n")
scorethershold = find_average_score(scoresentences)
print(scorethershold)

print("###############Showing summary - Hints##################\n")
summary = generate_summary(sentences, scoresentences, 1.5*scorethershold)
print(summary)
