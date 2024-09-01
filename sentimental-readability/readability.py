from cs50 import get_string


def main():
    entry = get_string("Text: ")
    words = entry.count(" ") + 1
    sentences = entry.count(".") + entry.count("?") + entry.count("!")
    letters = len(entry) - sentences - entry.count(" ") - \
        entry.count(",") - entry.count("\'") - entry.count("\"")
    grade = round(0.0588 * (letters * 100/words) - 0.296 * (sentences * 100/words) - 15.8)
    if grade < 1:
        print("Before Grade 1")
    elif grade > 15:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")


main()
