#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int calculate(string word);

int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int main(void)
{
    string w1 = get_string("Player 1: ");
    string w2 = get_string("Player 2: ");
    int s1 = calculate(w1);
    int s2 = calculate(w2);
    string winner = "";
    if (s1 > s2)
    {
        winner = "Player 1 wins!\n";
    }
    else if (s1 == s2)
    {
        winner = "Tie!\n";
    }
    else
    {
        winner = "Player 2 wins!\n";
    }
    printf("%s", winner);
}

int calculate(string word)
{
    int score = 0;
    for (int i = 0, len = strlen(word); i < len; i++)
    {
        if (isupper(word[i]))
        {
            score += POINTS[word[i] - 'A'];
        }
        else if (islower(word[i]))
        {
            score += POINTS[word[i] - 'a'];
        }
    }
    return score;
}
