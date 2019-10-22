from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import csv

word_net_lemma = WordNetLemmatizer()


def pos_tagging(sentence):
    return pos_tag(word_tokenize(sentence))


def get_synsets(pos_tag_array):
    return [filter_on_tag(*tagged_word) for tagged_word in pos_tag_array]


def remove_empty_sets(syn_sets):
    return [ss for ss in syn_sets if ss]


def filter_on_tag(tag):
    if tag.startswith('N'):
        return 'n'
    if tag.startswith('V'):
        return 'v'
    if tag.startswith('J'):
        return 'a'
    if tag.startswith('R'):
        return 'r'
    return None


def get_the_answer(best_sentence, csvPath):
    answers = ""
    with open(csvPath, encoding='UTF-8') as csvfile:
        csv_content = csv.reader(csvfile, delimiter=',')
        for row in csv_content:
            if row[0].strip() == best_sentence.strip():
                answers = row[1]
    return answers


def get_synsets_from_tags(word, tag):
    wn_tag = filter_on_tag(tag)
    if wn_tag is None:
        return None
    try:
        return wn.synsets(word_net_lemma.lemmatize(word), wn_tag)[0]
    except:
        return None
