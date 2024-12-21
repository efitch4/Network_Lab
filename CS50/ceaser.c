#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[])
{

    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }


    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

   
    int key = atoi(argv[1]) % 26;

    
    string plaintext = get_string("plaintext:  ");

    printf("ciphertext: ");

 
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (isupper(plaintext[i]))
        {
            printf("%c", (((plaintext[i] - 'A') + key) % 26) + 'A');
        }
        else if (islower(plaintext[i]))
        {
          
            printf("%c", (((plaintext[i] - 'a') + key) % 26) + 'a');
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }

    printf("\n");

    return 0;
}
