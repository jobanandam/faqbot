# Scikit Learn
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Define the sentences
sentence1 = 'Hello, how are you ?'
sentence2 = 'Hey, how are you ?'

sentences = [sentence1, sentence2]

# Create the Document Term Matrix
count_vectorizer = CountVectorizer(stop_words='english')
count_vectorizer = CountVectorizer()
sparse_matrix = count_vectorizer.fit_transform(sentences)

# OPTIONAL: Convert Sparse Matrix to Pandas Dataframe if you want to see the word frequencies.
doc_term_matrix = sparse_matrix.todense()
df = pd.DataFrame(doc_term_matrix,
                  columns=count_vectorizer.get_feature_names(),
                  index=['sentence1', 'sentence2'])
print(df)
# Compute Cosine Similarity
cosine_similar_val = cosine_similarity(df, df)
print("cosine similarity of sentence 1 and sentence 2 is ", cosine_similar_val[0][1])

