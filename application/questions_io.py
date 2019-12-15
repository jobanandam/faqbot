from application import file_reader
from application.file_reader import read_json_file
from application.file_writer import write_json_file


def update_user_suggestible_questions(user_id, updated_suggestible_questions):
    suggestible_questions_file = "../application/resources/suggestible_questions.json"
    root_json_obj = read_json_file(suggestible_questions_file)
    exiting_results_of_one_question = root_json_obj[user_id]
    user_question = exiting_results_of_one_question["user_question"]

    user_questions_data = {
        "user_id": user_id,
        "user_question": user_question,
        "suggestible_questions": updated_suggestible_questions
    }

    append_user_suggestible_questions_in_file(user_questions_data, suggestible_questions_file)


def append_user_suggestible_questions_in_file(data, file_name):
    results_of_one_question = {
        "user_question": data["user_question"],
        "suggestible_questions": data["suggestible_questions"]
    }

    root_json_obj = read_json_file(file_name)
    root_json_obj[data["user_id"]] = results_of_one_question
    write_json_file(root_json_obj, file_name)


def get_all_questions(file="resources/Single_FaQ.json"):
    single_faq_json_file = file
    root_json_obj = file_reader.read_json_file(single_faq_json_file)
    return root_json_obj["questions"]
