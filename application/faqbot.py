from uuid import uuid4

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

import file_reader
from binary_classifier import TechnicalClassifier
from classifier import DevopsClassifier
from feedback_system import FeedbackSystem
from questions_io import append_user_suggestible_questions_in_file, get_all_questions
from db_functions import update_questions_for_which_not_able_to_find_answer_to_db

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


class Question:
    category = ''
    question = ''
    max_score_of_matched_sent = 0

    def is_feedback_required(self):
        return self.category != 'Generic' and 0.56 < self.max_score_of_matched_sent < 0.95


def exclude_typo(question):
    question = question.lower()
    print ("question in lower", question)
    question_tokens = question.split()
    print("Inside exclude typo")
    final_word = ""
    for question_token in question_tokens:
        root_json_obj = file_reader.read_json_file("resources/Topic_Typo_Tolerance_Set.json")
        tolerable_words_data_collection = root_json_obj["tolerable_words_data_collection"]
        word_exists_in_csv = 0
        print(question_token)

        for tolerable_word_data in tolerable_words_data_collection:
            if question_token in tolerable_word_data["tolerable_words"]:
                print(tolerable_word_data["correct_word"], "is miss spelt as", question_token)
                final_word = final_word + " " + tolerable_word_data["correct_word"]
                word_exists_in_csv = 1
                break

        if word_exists_in_csv == 0:
            final_word = final_word + " " + question_token

    print("corrected question is", final_word)
    return final_word


class SentenceSimilarities:
    dev_ops_classifier = DevopsClassifier('resources/Single_FaQ.json')
    technical_classifier = TechnicalClassifier('resources/Single_FaQ.json', 'resources/generic_dialogue.json')
    questionObj = Question()    # contains current question's attributes

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
    def calculate_similarity(print_possible_matches, question, perform_classification):
        score_array = []
        if perform_classification:
            bin_cat = SentenceSimilarities.technical_classifier.get_technical_category(question)
            print('[Debug]: Question is {}'.format(question))
            print('[Debug]: Category from layer 1 is {}'.format(bin_cat))
            if bin_cat == 'Generic':
                sentences = SentenceSimilarities.dev_ops_classifier.get_questions(category=bin_cat)
            else:
                cat = SentenceSimilarities.dev_ops_classifier.get_devops_category(question)
                print('[Debug]: Category from layer 2 is {}'.format(cat))
                sentences = SentenceSimilarities.dev_ops_classifier.get_questions(category=cat)
            SentenceSimilarities.questionObj.category = bin_cat
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

            filtered_matched_sentences = SentenceSimilarities.filter_matched_sentences(cumulative_average_score,
                                                                                       matched_sentences,
                                                                                       print_possible_matches,
                                                                                       max(matched_score_array))
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

                possible_sentences = SentenceSimilarities.calculate_similarity(detailed_logging, question,
                                                                               perform_classification)
                for best_sentence, question, best_score in possible_sentences:
                    answer = SentenceSimilarities.get_the_answer_unclassified(detailed_logging, best_sentence,
                                                                              best_score, question)
                    if not answer:
                        print("Please ask questions related to DevOps")
                    else:
                        print(answer, best_score)
                if not possible_sentences:
                    print("Please ask questions related to DevOps")
        return answer

    @staticmethod
    def get_questions_from_user_interface(question, detailed_logging, perform_classification):
        SentenceSimilarities.questionObj.question = question
        user_id = str(uuid4())
        suggestible_questions = []
        # Initialize response_dict with default values
        response_dict = {"user_id": user_id, "answer": "Sorry, I couldn't help you with this question! Please raise a ticket",
                                         "prompt_feedback": "N", "index": -1}
        if question.split(" ").__len__().__le__(1):     # question too short
            response_dict["answer"] = "Can you please give some more details, so that i can try to answer"
        else:   # calculate similarity
            corrected_question = exclude_typo(question)
            possible_sentences = SentenceSimilarities.calculate_similarity(detailed_logging, corrected_question,
                                                                           perform_classification)
            # sort in descending order of score
            sorted_possible_sentences = sorted(possible_sentences, key=lambda record: record[2], reverse=True)
            print(" sorted_possible_sentences ")
            print(sorted_possible_sentences)
            if len(sorted_possible_sentences) > 0:      # if there is more than one matched sentence
                max_score = sorted_possible_sentences[0][2]
                SentenceSimilarities.questionObj.max_score_of_matched_sent = max_score
                print("max score = ")
                print(max_score)
                if SentenceSimilarities.questionObj.is_feedback_required():    # bot is doubtful. go for feedback mechanism
                    print("I'm doubtful. Let me go for feedback mechanism")
                    SentenceSimilarities.write_possible_questions(detailed_logging, possible_sentences,
                                                                  suggestible_questions,
                                                                  user_id, corrected_question)
                    next_suggestible_question = FeedbackSystem.get_next_suggestible_question_for(user_id)
                    response_dict["prompt_feedback"] = "Y"
                    response_dict["answer"] = next_suggestible_question["answer"]
                    response_dict["index"] = next_suggestible_question["index"]
                else:   # bot is confident. go for the first question's answer in the sorted possible sentences
                    print("I'm confident. I'll respond with the first matched question's answer")
                    best_match = sorted_possible_sentences[0]
                    answer = SentenceSimilarities.get_the_answer_unclassified(detailed_logging, best_match[0],
                                                                              best_match[2], best_match[1])
                    if answer:
                        response_dict["answer"] = answer
                    else:
                        update_questions_for_which_not_able_to_find_answer_to_db(question,user_id)
            else:
                update_questions_for_which_not_able_to_find_answer_to_db(question, user_id)
        return response_dict

    @staticmethod
    def respond_to_user_feedback(feedback, user_id, index):
        positive_feedback_list = ["y", "yes", "ye", "yeah", "yea", "s", "ss", "absolutely", "yup", "yep", "yeh", "ya", "yo"]
        negative_feedback_list = ["n", "no", "noo", "nah", "na", "ne", "np", "never", "nil", "not", "nope", "dont", "nooo"]
        response_dict = {"user_id": user_id, "answer": "Sorry, I couldn't help you with this question! Please raise a ticket",
                         "prompt_feedback": "N", "index": -1}
        if feedback.lower() in positive_feedback_list:  # positive feedback
            FeedbackSystem.update_positive_feedback(user_id, index)
            response_dict["answer"] = "Thanks for your feedback! This will help me in my learning process."
        elif feedback.lower() in negative_feedback_list:    # negative feedback
            next_suggestible_question = FeedbackSystem.get_next_suggestible_question_for(user_id)
            answer = next_suggestible_question["answer"]
            if not answer:
                response_dict["answer"] = "Sorry, I couldn't help you with this question! Please raise a ticket"
            else:
                response_dict["answer"] = answer
                response_dict["prompt_feedback"] = "Y"
                response_dict["index"] = next_suggestible_question["index"]
        else:   # This doesn't look like a normal feedback. Treat this as a question
            print("This doesnt look like a valid feedback. So treating this as a question from the user and "
                  "performing similarity calculation. ")
            response_dict = SentenceSimilarities.get_questions_from_user_interface(feedback, False, True)
        return response_dict

    @staticmethod
    def write_possible_questions(detailed_logging, possible_sentences, suggestible_questions, user_id, user_question):
        index = -1
        for best_sentence, question, best_score in possible_sentences:
            index += 1
            answer = SentenceSimilarities.get_the_answer_unclassified(detailed_logging, best_sentence,
                                                                      best_score, question)
            suggestible_questions.append({
                "index": index,
                "question": best_sentence,
                "answer": answer,
                "score": best_score,
                "processed": "N",
                "accepted": "N"
            })

        suggestible_questions_json_file_name = "./resources/suggestible_questions.json"
        user_questions_data = {
                "user_id": user_id,
                "user_question": user_question,
                "suggestible_questions": suggestible_questions
        }
        append_user_suggestible_questions_in_file(user_questions_data, suggestible_questions_json_file_name)

    @staticmethod
    def get_the_answer_unclassified(print_answers, best_sentence, best_score, question):
        answers = ""
        questions_data = get_all_questions()
        for question_data in questions_data:
            if question_data["question"] == best_sentence:
                answers = question_data["answer"]

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
                possible_sentences = SentenceSimilarities.calculate_similarity(detailed_logging, question,
                                                                               perform_classification)
                for best_sentence, question, best_score in possible_sentences:
                    answer = SentenceSimilarities.get_the_answer_unclassified(detailed_logging, best_sentence,
                                                                              best_score, question)
                    if not answer:
                        print("Sorry, I couldn't help you with this question! Please raise a ticket")
                        results.append(
                            (question, "No Question Matched", "Sorry, I couldn't help you with this question! Please raise a ticket", "0.0"))
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
        SentenceSimilarities.dev_ops_classifier.initialize_models()
        SentenceSimilarities.technical_classifier.initialize_models()

    @staticmethod
    def perform_classification_and_sent_similarities():
        SentenceSimilarities.dev_ops_classifier.initialize_models()
        SentenceSimilarities.technical_classifier.initialize_models()
        SentenceSimilarities.get_questions_from_user(True, True)

    @staticmethod
    def perform_classification_and_sent_similarities_on_file():
        SentenceSimilarities.dev_ops_classifier.initialize_models()
        SentenceSimilarities.technical_classifier.initialize_models()
        SentenceSimilarities.get_questions_from_file(False, False)

    @staticmethod
    def perform_sent_similarities():
        SentenceSimilarities.get_questions_from_user(False, False)

    @staticmethod
    def test_classifier(save_result=False, accuracy=False):
        SentenceSimilarities.dev_ops_classifier.initialize_models()
        tot = len(SentenceSimilarities.dev_ops_classifier.raw_category_question)
        cur = 0
        for cat, question in SentenceSimilarities.dev_ops_classifier.raw_category_question:
            result = SentenceSimilarities.dev_ops_classifier.get_devops_category(question)
            if (result != cat):
                cur = cur + 1
                print('[Test] Question: {}'.format(question))
                print('[Test] True: {} <====> Predicted: {}'.format(cat, result))
                print()
        print('[Test]: Accuracy: {:.2f}%'.format(((tot - cur) / tot) * 100))
        print('[Test]: Completed ! ! !')


if __name__ == '__main__':
    SentenceSimilarities.perform_classification_and_sent_similarities_on_file()

    # SentenceSimilarities.perform_classification_and_sent_similarities()
    # SentenceSimilarities.perform_sent_similarities()
    # SentenceSimilarities.get_questions_from_user(False)
    # SentenceSimilarities.get_questions_from_file(False)
