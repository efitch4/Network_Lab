#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include<stdio.h>
#include<string.h>

int main(void)
{
int main(void)
{
    // Prompt the user for some text
    string text = get_string("Text: ");

    // Count the number of letters, words, and sentences in the text
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // Calculate L and S
    float L = ((float) letters / words) * 100;
    float S = ((float) sentences / words) * 100;

    // Compute the Coleman-Liau index
    float index = 0.0588 * L - 0.296 * S - 15.8;

    // Print the grade level
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %.0f\n", round(index));  // Round to nearest integer
    }
}
