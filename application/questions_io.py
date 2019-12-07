from application.file_reader import read_json_file
from application.file_writer import write_json_file


def update_user_suggestible_questions(user_id, suggestible_questions):
    data = {"user_id": user_id, "suggestible_questions": suggestible_questions}
    append_user_suggestible_questions_in_file(data, "../application/resources/suggestible_questions.json")


def append_user_suggestible_questions_in_file(data, file_name):
    root_json_obj = read_json_file(file_name)
    root_json_obj[data["user_id"]] = data["suggestible_questions"]
    write_json_file(root_json_obj, file_name)
