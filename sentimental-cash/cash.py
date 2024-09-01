from cs50 import get_float


def main():
    while True:
        change = get_float("Change: ")
        if change > 0.0:
            break

    coins = int(change / 0.25)
    change = round((change % 0.25), 2)
    coins += int(change / 0.10)
    change = round((change % 0.10), 2)
    coins += int(change / 0.05)
    change = round((change % 0.05), 2)
    coins += int(change / 0.01)
    print(f"{coins}")


main()
