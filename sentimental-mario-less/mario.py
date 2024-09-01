from cs50 import get_int


def main():
    while True:
        value = get_int("Height: ")
        if value < 9 and value > 0:
            break

    for i in range(value):
        for j in range(value - i - 1):
            print(" ", end="")
        for j in range(i + 1):
            print("#", end="")
        print()


main()
