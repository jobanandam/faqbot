from operator import itemgetter


def get_next_suggestible_question(user_id, suggestible_questions):
    sorted_suggestible_questions = sorted(suggestible_questions, key=itemgetter(1), reverse=True)

    for index in range(len(sorted_suggestible_questions)):
        sorted_suggestible_question = sorted_suggestible_questions[index]
        if sorted_suggestible_question[2] == "N":
            sorted_suggestible_question = mark_question_as_processed(sorted_suggestible_question)
            sorted_suggestible_questions[index] = sorted_suggestible_question
            return sorted_suggestible_question, sorted_suggestible_questions

    return (), []


def mark_question_as_processed(sorted_suggestible_question):
    sorted_suggestible_question_properties = list(sorted_suggestible_question)
    sorted_suggestible_question_properties[2] = "Y"
    sorted_suggestible_question = tuple(sorted_suggestible_question_properties)
    return sorted_suggestible_question


def main():
    suggestible_test_questions = [("How is it going?", 1, "N"), ("Are you ok?", 2, "N"),
                                  ("How do you feel?", 3, "N"), ("How you are doing?", 4, "N")]
    user_id = "b029199e-2214-45e9-bcf4-62c90b377b00"

    next_suggestible_question, suggestible_test_questions = get_next_suggestible_question(user_id, suggestible_test_questions)

    while next_suggestible_question != ():
        print("Is this what you are looking for?")
        print(next_suggestible_question)
        feedback = input()
        if feedback == "Y":
            print("Suggestion accepted: ", next_suggestible_question[0])
            break
        else:
            next_suggestible_question, suggestible_test_questions = get_next_suggestible_question(user_id, suggestible_test_questions)


if __name__ == '__main__':
    main()
