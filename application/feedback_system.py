from application.file_reader import read_json_file
from application.questions_io import update_user_suggestible_questions


class FeedbackSystem:

    @staticmethod
    def get_next_suggestible_question_from(user_id, sorted_suggestible_questions):
        sorted_suggestible_questions = list(sorted_suggestible_questions)

        for index in range(len(sorted_suggestible_questions)):
            next_suggestible_question = sorted_suggestible_questions[index]
            if next_suggestible_question["processed"] == "N":
                next_suggestible_question = FeedbackSystem.mark_question_as_processed(next_suggestible_question)
                sorted_suggestible_questions[index] = next_suggestible_question

                update_user_suggestible_questions(user_id, sorted_suggestible_questions)

                return next_suggestible_question

        return None

    @staticmethod
    def mark_question_as_processed(sorted_suggestible_question):
        sorted_suggestible_question["processed"] = "Y"
        return sorted_suggestible_question

    @staticmethod
    def main():
        user_id = "4186950e-3c72-40fa-88c5-28aa278fccd6"
        # next_suggestible_question = get_next_suggestible_question_for(user_id)
        # main_run_feedback_system(next_suggestible_question, user_id)

        accepted_question_index = 1
        FeedbackSystem.update_positive_feedback(user_id, accepted_question_index)

    @staticmethod
    def update_positive_feedback(user_id, accepted_question_index):
        suggestible_questions = FeedbackSystem.get_user_specific_suggestible_questions(user_id)

        for index in range(len(suggestible_questions)):
            question = suggestible_questions[index]
            if question.get("index") == accepted_question_index:
                question["accepted"] = "Y"
                suggestible_questions[index] = question
                update_user_suggestible_questions(user_id, suggestible_questions)

    @staticmethod
    def main_run_feedback_system(next_suggestible_question, user_id):
        while next_suggestible_question.get("question") is not None:
            print("Is this what you are looking for?")
            print(next_suggestible_question.get("question"))
            feedback = input()
            if feedback == "Y":
                print("Suggestion accepted: ", next_suggestible_question["question"])
                next_suggestible_question["accepted"] = "Y"
                break
            else:
                next_suggestible_question = FeedbackSystem.get_next_suggestible_question_for(user_id)

    @staticmethod
    def get_next_suggestible_question_for(user_id):
        user_suggestible_questions = FeedbackSystem.get_user_specific_suggestible_questions(user_id)

        no_questions_left = {"answer": ""}
        if len(user_suggestible_questions) == 0:
            return no_questions_left
        else:
            sorted_suggestible_questions = sorted(user_suggestible_questions, key=lambda record: record["score"], reverse=True)
            next_suggestible_question = FeedbackSystem.get_next_suggestible_question_from(user_id, sorted_suggestible_questions)

            if next_suggestible_question is not None:
                return next_suggestible_question
            else:
                return no_questions_left

    @staticmethod
    def get_user_specific_suggestible_questions(user_id):
        all_user_suggestible_questions = read_json_file("../application/resources/suggestible_questions.json")
        user_suggestible_questions = all_user_suggestible_questions.get(user_id)
        return user_suggestible_questions


if __name__ == '__main__':
    FeedbackSystem.main()
