from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer

from classifier import DevopsClassifier

stem_obj = SnowballStemmer('english')
word_net_lemma = WordNetLemmatizer()


class myClass():
    def __init__(self, sentence_score, value):
        self.score = sentence_score
        self.value = value

    def __eq__(self, other):
        return self.score == other.score and self.value == other.value

    def __lt__(self, other):
        return self.score < other.score


class SentenceSimilarities:
    dc = DevopsClassifier('resources/Single_FaQ.csv')
    @staticmethod
    def penn_to_wn(tag):
        """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
        if tag.startswith('N'):
            return 'n'
        if tag.startswith('V'):
            return 'v'
        if tag.startswith('J'):
            return 'a'
        if tag.startswith('R'):
            return 'r'
        return None

    @staticmethod
    def tagged_to_syn_set(word, tag):
        wn_tag = SentenceSimilarities.penn_to_wn(tag)
        if wn_tag is None:
            return None
        try:
            return wn.synsets(word_net_lemma.lemmatize(word), wn_tag)[0]
        except:
            # print(word,wn_tag)
            return word, wn_tag

    @staticmethod
    def symmetric_sentence_similarity(sentence1, sentence2):
        # """ compute the symmetric sentence similarity using Wordnet """
        sentence_similar_score = 0.0
        primary_sim = SentenceSimilarities.sentence_similarity(sentence1, sentence2)
        secondary_sim = SentenceSimilarities.sentence_similarity(sentence2, sentence1)

        if primary_sim is not None and secondary_sim is not None:
            sentence_similar_score = (primary_sim + secondary_sim) / 2
        elif primary_sim is not None and secondary_sim is None:
            sentence_similar_score = primary_sim
        elif primary_sim is None and secondary_sim is not None:
            sentence_similar_score = secondary_sim
        return sentence_similar_score


    @staticmethod
    def sentence_similarity(sentence1, sentence2):
        """ compute the sentence similarity using Wordnet """
        # Tokenize and tag
        sentence1 = pos_tag(word_tokenize(sentence1))
        sentence2 = pos_tag(word_tokenize(sentence2))

        syn_sets_1 = []
        syn_sets_2 = []
        non_dict_set_sets_1 = []
        non_dict_set_sets_2 = []

        for tagged_word in sentence1:
            result_returned = SentenceSimilarities.tagged_to_syn_set(*tagged_word)
            if result_returned is not None:
                if type(result_returned) is tuple:
                    non_dict_set_sets_1.append(result_returned)
                else:
                    syn_sets_1.append(result_returned)

        for tagged_word in sentence2:
            result_returned = SentenceSimilarities.tagged_to_syn_set(*tagged_word)
            if result_returned is not None:
                if type(result_returned) is tuple:
                    non_dict_set_sets_2.append(result_returned)
                else:
                    syn_sets_2.append(result_returned)

        # Filter out the Nones
        syn_sets_1 = [ss for ss in syn_sets_1 if ss]
        syn_sets_2 = [ss for ss in syn_sets_2 if ss]
        synset_score, count = 0.0, 0
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
                synset_score += new_score
                count += 1

        non_dict_score, sum_non_dict_score = 0.0, 0.0
        for non_dict_word_sent1, non_dict_word_pos_sent1 in non_dict_set_sets_1:
            non_dict_score_array = []
            for non_dict_word_sent2, non_dict_word_pos_sent2 in non_dict_set_sets_2:
                if str(non_dict_word_sent1).lower().__eq__(str(non_dict_word_sent2).lower()):
                    if non_dict_word_pos_sent1 == non_dict_word_pos_sent2:
                        non_dict_score_array.append(1.0)
                    else:
                        non_dict_score_array.append(0.5)
            sum_non_dict_score = sum(non_dict_score_array)
            if sum_non_dict_score is not None:
                non_dict_score += sum_non_dict_score
                count += 1
        final_score = synset_score + non_dict_score

        # Average the values
        if count > 0:
            final_score /= count
        return final_score

    @staticmethod
    def read_content_from_file(file_name):
        import csv
        faq_sentences = []
        with open(file_name) as file:
            csv_reader = csv.reader(file, delimiter='\t')
            for each_line in csv_reader:
                faq_sentences.append(each_line[1])
        return faq_sentences

    @staticmethod
    def filter_matched_sentences(cumulative_average_score, matched_sentences, print_possible_matches, max_score_array):
        filtered_matched_sentences = []
        if print_possible_matches:
            print("************************************************")
            print("Best match before Filter")
            print("Asked Question, Matched Sentence , Matched Score")
        for sentence_matched, question, score in matched_sentences:
            if print_possible_matches:
                print("%s, %s, %s  " % (question, sentence_matched, score))
            if max_score_array.__eq__(1.0):
                if score == 1.0:
                    filter_matched_sentence_tuple = (sentence_matched, question, score)
                    filtered_matched_sentences.append(filter_matched_sentence_tuple)
            elif cumulative_average_score <= score <= 1.0:
                filter_matched_sentence_tuple = (sentence_matched, question, score)
                filtered_matched_sentences.append(filter_matched_sentence_tuple)
        return filtered_matched_sentences

    @staticmethod
    def test_classifier(save_result=False, accuracy=False):
        SentenceSimilarities.dc.initialize_models()
        tot = len(SentenceSimilarities.dc.raw_category_question)
        cur = 0
        for cat, question in SentenceSimilarities.dc.raw_category_question:
            result = SentenceSimilarities.dc.get_devops_category(question)
            if(result != cat):
                cur = cur + 1
                print('[Test] Question: {}'.format(question))
                print('[Test] True: {} <====> Predicted: {}'.format(cat, result))
                print()
        print('[Test]: Accuracy: {:.2f}%'.format(((tot - cur)/tot)*100))
        print('[Test]: Completed ! ! !')

    @staticmethod
    def calculate_similarity(print_possible_matches, question, perform_classification):
        score_array = []
        if perform_classification:
            cat = SentenceSimilarities.dc.get_devops_category(question)
            sentences = SentenceSimilarities.dc.get_questions(category=cat)
        else:
            sentences = SentenceSimilarities.read_content_from_file("resources/Single_FaQ.csv")
        if print_possible_matches:
            print("----Possible Matches ---")
            print("Matched Sentence , Matched Score")
        matched_sentences, matched_score_array = [], []
        overall_score, training_data_count = 0.0, 0
        for sentence in sentences:
            if sentence:
                score = SentenceSimilarities.symmetric_sentence_similarity(sentence, question)
                score_class = myClass(score, sentence)
                score_array.append(score_class)
                if print_possible_matches:
                    print("%s , %s  " % (sentence, score))
                if score > 0.56:
                    # print(sentence, question, score)
                    matched_sent_tuple = (sentence, question, score)
                    matched_score_array.append(score)
                    overall_score += score
                    training_data_count += 1
                    matched_sentences.append(matched_sent_tuple)

        if training_data_count != 0:
            cumulative_average_score = overall_score / training_data_count
            if print_possible_matches:
                print("Cumulative Average score", cumulative_average_score)
                print("Max Score", max(matched_score_array))

            filtered_matched_sentences = SentenceSimilarities.filter_matched_sentences(cumulative_average_score, matched_sentences,
                                                                  print_possible_matches, max(matched_score_array))
        else:
            filtered_matched_sentences = matched_sentences

        if print_possible_matches:
            SentenceSimilarities.print_match_results(filtered_matched_sentences)
        return filtered_matched_sentences

    @staticmethod
    def print_match_results(matched_sentences):
        print("************************************************")
        print("Best match")
        print("Asked Question, Matched Sentence , Matched Score")
        for best_sentence, question, best_score in matched_sentences:
            print("%s, %s, %s  " % (question, best_sentence, best_score))
        print("************************************************")

    @staticmethod
    def print_question_answer(question, answers, best_score):
        print("************************************************")
        print("Answer for your Question")
        print("Question, Answer , Matched Score")
        print("%s, %s , %s  " % (question, answers, best_score))
        print("************************************************")

    @staticmethod
    def get_questions_from_user(detailed_logging, perform_classification):
        print("Hi Welcome to FAQ BOT !!!!  Ctrl+C to Exit from FAQ BOT \n")
        while True:
            question = input("Please ask your Questions? \n")
            if question.split(" ").__len__().__le__(1):
                print("Can you please give some more details, so that i can try to answer")
            else:
                possible_sentences = SentenceSimilarities.calculate_similarity(detailed_logging, question, perform_classification)
                for best_sentence, question, best_score in possible_sentences:
                    answer = SentenceSimilarities.get_the_answer_unclassified(detailed_logging, best_sentence, best_score, question)
                    if not answer:
                        print("Please ask questions related to DevOps")
                    else:
                        print(answer, best_score)
                if not possible_sentences:
                    print("Please ask questions related to DevOps")
        return answer

    @staticmethod
    def get_questions_from_user_interface(question, detailed_logging):
        if question.split(" ").__len__().__le__(1):
            return "Can you please give some more details, so that i can try to answer"
        else:
            possible_sentences = SentenceSimilarities.calculate_similarity(detailed_logging, question, False)
            for best_sentence, question, best_score in possible_sentences:
                answer = SentenceSimilarities.get_the_answer_unclassified(detailed_logging, best_sentence,
                                                                          best_score, question)
                if not answer:
                    return "Please ask questions related to DevOps"
                else:
                    return answer
            if not possible_sentences:
                return "Please ask questions related to DevOps"

    @staticmethod
    def get_the_answer_unclassified(print_answers, best_sentence, best_score, question):
        import csv
        answers = ""
        with open('resources/Single_FaQ.csv') as csvfile:
            csv_content = csv.reader(csvfile, delimiter='\t')
            for row in csv_content:
                if row[1] == best_sentence:
                    answers = row[2]
        if print_answers:
            SentenceSimilarities.print_question_answer(question, answers, best_score)
        return answers

    @staticmethod
    def read_questions_from_file(file_name):
        file = open(file_name, "r")
        questions_from_file = file.read().split("\n")
        return questions_from_file

    @staticmethod
    def write_the_results(results):
        import csv
        with open('test/FAQResults.csv', 'w', newline='') as out:
            csv_out = csv.writer(out)
            csv_out.writerow(("Quesion asked", "Question Matched", "Answers", "Score"))
            for row in results:
                csv_out.writerow(row)

    @staticmethod
    def get_questions_from_file(detailed_logging, perform_classification):
        print("Hi Welcome to FAQ BOT !!!!")
        questions = SentenceSimilarities.read_questions_from_file("test/questions.txt")
        results = []
        for question in questions:
            if question.split(" ").__len__().__le__(1):
                print("Can you please give some more details, so that i can try to answer")
                results.append((question, "No Question Matched",
                                "Can you please give some more details, so that i can try to answer", "0.0"))
            else:
                possible_sentences = SentenceSimilarities.calculate_similarity(detailed_logging, question,perform_classification)
                for best_sentence, question, best_score in possible_sentences:
                    answer = SentenceSimilarities.get_the_answer_unclassified(detailed_logging, best_sentence, best_score, question)
                    if not answer:
                        print("Please ask questions related to DevOps")
                        results.append(
                            (question, "No Question Matched", "Please ask questions related to DevOps", "0.0"))
                    else:
                        print(answer, best_score)
                        results.append((question, best_sentence, answer, best_score))
                if not possible_sentences:
                    print("Please ask questions related to DevOps")
                    results.append((question, "No Question Matched", "Please ask questions related to DevOps", "0.0"))
        SentenceSimilarities.write_the_results(results)
        pass

    @staticmethod
    def perform_classification_on_test_data():
        SentenceSimilarities.dc.initialize_models()

    @staticmethod
    def perform_classification_and_sent_similarities():
        SentenceSimilarities.dc.initialize_models()
        SentenceSimilarities.get_questions_from_user(False, True)

    @staticmethod
    def perform_classification_and_sent_similarities_on_file():
        SentenceSimilarities.dc.initialize_models()
        SentenceSimilarities.get_questions_from_file(False, True)

    @staticmethod
    def perform_sent_similarities():
        SentenceSimilarities.get_questions_from_user(False, False)


if __name__ == '__main__':
    # SentenceSimilarities.perform_classification_and_sent_similarities_on_file()
    # SentenceSimilarities.perform_classification_and_sent_similarities()
    # SentenceSimilarities.perform_sent_similarities()
    # SentenceSimilarities.get_questions_from_user(False)
    # SentenceSimilarities.get_questions_from_file(False)
    SentenceSimilarities.test_classifier()