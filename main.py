def read_subscribers(path):
    file = open(path)
    text = file.read()
    file.close()
    return text


def main():
    print("Hello from mailroom!")


if __name__ == "__main__":
    main()
