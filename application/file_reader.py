import json


def read_file(source, mode):
    file = open(source, mode)
    content = file.read()
    file.close()
    return content


def read_json_file(file_name):
    file = open(file_name, "r")
    json_data = json.loads(file.read())
    return json_data


def main():
    print(read_file("./resources/Single_FaQ.txt", "r"))


if __name__ == '__main__':
    main()
