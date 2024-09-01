// Implements a dictionary's functionality

#include <ctype.h>
#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 25000;

// Count of words
unsigned int counter = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int bucket = hash(word);
    node *node = table[bucket];
    while (node != NULL)
    {
        if (strcasecmp(word, node->word) == 0)
        {
            return true;
        }
        else
        {
            node = node->next;
        }
    }
    // TODO
    return false;
}

// Hashes word from dict to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned int val = 0;
    unsigned int squared = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        squared = toupper(word[i]) * toupper(word[i]);
        val = (squared * strlen(word)) + val;
    }
    return val % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the dictionary file
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        return false;
    }

    // Read each word in the file
    char word[LENGTH + 1];
    while (fscanf(source, "%s", word) != EOF)
    {
        // Add each word to the hash table
        node *n = malloc(sizeof(node));
        strcpy(
            n->word,
            word); // fills node, make sure out  address of the next node is in next of current node
        n->next = NULL;
        int bucket = hash(word);
        if (table[bucket] == NULL)
        {
            table[bucket] = n;
        }
        else
        {
            n->next = table[bucket];
            table[bucket] = n;
        }
        counter++;
    }

    // Close the dictionary file
    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        // temp and node starting
        node *holder = table[i];
        node *node = table[i];

        while (holder != NULL)
        {
            node = node->next;
            // free holder while setting holder to the next to be freed
            free(holder);
            holder = node;
        }
    }
    return true;
}
