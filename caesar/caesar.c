#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

string encrypt(string usertext, string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Error, please enter one command line argument\n");
        return 1;
    }
    string key = argv[1];

    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (!isdigit(key[i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    string usertext = get_string("plaintext:  ");
    string ciphertext = encrypt(usertext, key);
    printf("ciphertext: %s\n", ciphertext);
    return 0;
}

string encrypt(string usertext, string key)
{
    int val = atoi(key);
    if (val > 26)
    {
        val = val % 26;
    }
    string encrypt = usertext;
    for (int i = 0, n = strlen(usertext); i < n; i++)
    {
        if (!isalpha(usertext[i]))
        {
            encrypt[i] = usertext[i];
        }
        else
        {
            char temp = usertext[i];
            if (isupper(usertext[i]) && temp + val > 90)
            {
                temp -= 26;
            }
            else if (islower(usertext[i]) && temp + val > 122)
            {
                temp -= 26;
            }
            encrypt[i] = temp + val;
        }
    }
    return encrypt;
}
