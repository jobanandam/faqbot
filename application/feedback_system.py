from application.file_reader import read_json_file
from application.questions_io import update_user_suggestible_questions


def get_next_suggestible_question_from(suggestible_questions):
    sorted_suggestible_questions = sorted(suggestible_questions, key=lambda record: record["score"], reverse=True)
    sorted_suggestible_questions = list(sorted_suggestible_questions)

    for index in range(len(sorted_suggestible_questions)):
        next_suggestible_question = sorted_suggestible_questions[index]
        if next_suggestible_question["processed"] == "N":
            next_suggestible_question = mark_question_as_processed(next_suggestible_question)
            sorted_suggestible_questions[index] = next_suggestible_question
            return next_suggestible_question, sorted_suggestible_questions

    return (), []


def mark_question_as_processed(sorted_suggestible_question):
    sorted_suggestible_question["processed"] = "Y"
    return sorted_suggestible_question


def main():
    user_id = "4186950e-3c72-40fa-88c5-28aa278fccd6"
    next_suggestible_question, user_suggestible_questions = get_next_suggestible_question_for(user_id)

    while next_suggestible_question != ():
        update_user_suggestible_questions(user_id, user_suggestible_questions)
        print("Is this what you are looking for?")
        print(next_suggestible_question)
        feedback = input()
        if feedback == "Y":
            print("Suggestion accepted: ", next_suggestible_question["question"])
            break
        else:
            next_suggestible_question, user_suggestible_questions = get_next_suggestible_question_from(
                user_suggestible_questions)


def get_next_suggestible_question_for(user_id):
    user_suggestible_questions = get_user_specific_suggestible_questions(user_id)
    next_suggestible_question, user_suggestible_questions = \
        get_next_suggestible_question_from(user_suggestible_questions)
    return next_suggestible_question, user_suggestible_questions


def get_user_specific_suggestible_questions(user_id):
    all_user_suggestible_questions = read_json_file("../application/resources/suggestible_questions.json")
    user_suggestible_questions = all_user_suggestible_questions.get(user_id)
    return user_suggestible_questions


if __name__ == '__main__':
    main()
