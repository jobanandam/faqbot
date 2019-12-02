def read_file(source, mode):
    file = open(source, mode)
    content = file.read()
    file.close()
    return content


def main():
    print(read_file("./resources/Single_FaQ.txt", "r"))


if __name__ == '__main__':
    main()
