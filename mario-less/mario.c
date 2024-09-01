#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int size;
    do
    {
        size = get_int("Height: ");
    }
    while (size < 1 || size > 8);

    for (int i = 0; i < size; i++)
    {
        int g = 0;
        do
        {
            if (i == size - 1)
            {
                g++;
            }
            else
            {
                printf(" ");
                g++;
            }
        }
        while (g < size - i - 1);
        for (int j = 0; j < i + 1; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
