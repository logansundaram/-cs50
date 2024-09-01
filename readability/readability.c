#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

float letters(string text, int word, float sentence);
float sentences(string text, int word);
int words(string text);

int main(void)
{
    string text = get_string("Text: ");
    int word = words(text);
    // printf("%i", word);
    float sentence = sentences(text, word);
    // printf("%f", sentence);
    float letter = letters(text, word, sentence);
    // printf("%f", letter);
    float ind = 0.0588 * letter - 0.296 * sentence - 15.8;
    int index = round(ind);
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

float letters(string text, int word, float sentence)
{
    int punctuation = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?' || text[i] == ',' || text[i] == '\"' || text[i] == '\'' ||
            text[i] == ':')
        {
            punctuation++;
        }
    }
    float counter = strlen(text) - word + 1 - punctuation;
    // printf("%f", counter);
    return counter / (float) word * 100;
}

float sentences(string text, int word)
{
    int counter = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            counter++;
        }
    }
    return counter / (float) word * 100;
}

int words(string text)
{
    int counter = 1;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == ' ')
        {
            counter++;
        }
    }
    return counter;
}
