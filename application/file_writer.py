import json
from uuid import uuid4


def write_file(target, content, mode):
    file = open(target, mode)
    if len(str(content)) != 0:
        file.write(str(content))
        file.write("\n")
    file.close()


def write_json_file(json_data, target_file):
    file = open(target_file, "w")
    json.dump(json_data, file)


def main():
    data = {"user_id": str(uuid4()), "suggestible_questions": [
                {"answer": "How are you1?", "processed": "N"},
                {"answer": "How are you2?", "processed": "N"},
                {"answer": "How are you3?", "processed": "N"},
                {"answer": "How are you4?", "processed": "N"}
            ]}
    # append_user_suggestible_questions_in_file(data, "./resources/suggestible_questions.json")


if __name__ == '__main__':
    main()
