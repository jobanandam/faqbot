from uuid import uuid4


def write_file(target, content, mode):
    file = open(target, mode)
    if len(str(content)) != 0:
        file.write(str(content))
        file.write("\n")
    file.close()


def main():
    data = {"user_id": str(uuid4()), "suggestible_questions": [
                {"answer": "How are you1?", "processed": "N"},
                {"answer": "How are you2?", "processed": "N"},
                {"answer": "How are you3?", "processed": "N"},
                {"answer": "How are you4?", "processed": "N"}
            ]}
    print(write_file("./resources/test.txt", data, "a"))


if __name__ == '__main__':
    main()
