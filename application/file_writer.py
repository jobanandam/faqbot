import json
from uuid import uuid4

from application.file_reader import read_json_file


def write_file(target, content, mode):
    file = open(target, mode)
    if len(str(content)) != 0:
        file.write(str(content))
        file.write("\n")
    file.close()


def append_json_into_array_file(data, file_name):
    tuples = read_json_file(file_name)
    obj_list = list(tuples)
    obj_list.append(data)
    tuples = tuple(obj_list)
    write_json_file(tuples, file_name)


def write_json_file(json_data, target_file):
    file = open(target_file, "w")
    json.dump(json_data, file)


def main():
    data = {str(uuid4()): {"suggestible_questions": [
                {"answer": "How are you1?", "processed": "N"},
                {"answer": "How are you2?", "processed": "N"},
                {"answer": "How are you3?", "processed": "N"},
                {"answer": "How are you4?", "processed": "N"}
            ]}}
    append_json_into_array_file(data, "./resources/test.txt")

    # print(write_file("./resources/test.txt", data, "a"))


if __name__ == '__main__':
    main()
