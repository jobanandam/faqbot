def get_jaccard_sim(str1, str2):
    a = set(str1.split())
    print(a)
    b = set(str2.split())
    print(b)
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


sentence1 = 'Hello, how are you ?'
sentence2 = 'Hey, how are you ?'
print("jacob sentence similarity", get_jaccard_sim(sentence1, sentence2))
