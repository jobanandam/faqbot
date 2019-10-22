from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import sentencesimilarities.util.sentence_util as SentenceUtil
import sentencesimilarities.util.file_util as FileUtil

stem_obj = SnowballStemmer('english')
word_net_lemma = WordNetLemmatizer()


def get_best_suitable_question(user_question):
    best_score = 0.0
    best_sentence = ""
    for db_question in input_question_set:
        score = calculate_best_score(db_question, user_question)
        if score > best_score:
            best_score = score
            best_sentence = db_question
    return best_sentence, best_score


def calculate_best_score(db_question, user_question):
    symmetric_similarity_score = 0.0
    primary_sim = calculate_symmetric_score(db_question, user_question)
    secondary_sim = calculate_symmetric_score(user_question, db_question)

    if primary_sim is not None and secondary_sim is not None:
        symmetric_similarity_score = (primary_sim + secondary_sim) / 2
    elif primary_sim is not None and secondary_sim is None:
        symmetric_similarity_score = primary_sim
    elif primary_sim is None and secondary_sim is not None:
        symmetric_similarity_score = secondary_sim
    return symmetric_similarity_score


def calculate_symmetric_score(question1, question2):
    """ compute the sentence similarity using Wordnet """

    # Tokenize and tag
    sentence1 = SentenceUtil.pos_tagging(question1)
    sentence2 = SentenceUtil.pos_tagging(question2)

    # Get the synsets for the tagged words

    syn_sets_1 = [SentenceUtil.get_synsets_from_tags(*tagged_word) for tagged_word in sentence1]
    syn_sets_2 = [SentenceUtil.get_synsets_from_tags(*tagged_word) for tagged_word in sentence2]

    # Filter out the Nones
    syn_sets_1 = SentenceUtil.remove_empty_sets(syn_sets_1)
    syn_sets_2 = SentenceUtil.remove_empty_sets(syn_sets_2)

    sim_score, count = 0.0, 0
    # For each word in the first sentence
    for syn_set in syn_sets_1:
        # Get the similarity value of the most similar word in the other sentence
        best_score = [syn_set.path_similarity(ss) for ss in syn_sets_2]
        filtered_score = []

        for score_value in best_score:
            if score_value is not None:
                filtered_score.append(score_value)
                # Check that the similarity could have been computed
        new_score = 0.0
        if filtered_score:
            if filtered_score is not None:
                new_score = max(filtered_score)
        if new_score is not None:
            sim_score += new_score
            count += 1
    # Average the values
    if count > 0:
        sim_score /= count
    return sim_score


def bot_start_chat():
    print("Hi Welcome to FAQ BOT !!!!\n")

    while True:
        question = input("Please ask your Question? \n")
        if question.split(" ").__len__().__le__(1):
            print("Can you please give some more details, so that i can try to answer ?")
        else:
            best_sentence, best_score = get_best_suitable_question(question)
            answer = SentenceUtil.get_the_answer(best_sentence,'resources/FaqQuestionsAndAnswers.csv')
            if not answer:
                print("Please ask questions related to DevOps")
            else:
                print(answer)
    pass


if __name__ == '__main__':
    input_question_set = FileUtil.read_questions_from_input_file("resources/FaqQuestions.txt")
    bot_start_chat()
