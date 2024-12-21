int i = 3;
while (i > 0)
{
    printf("meow\n");
    i--;
}


// This will create a function
// One thing to note is that you must define the function before you use it 

void meow(void)
{
    printf("meow\n");
}

int main(void)
{
    for (int i = 0; i < 3; i++)
    {
        meow();
    }
}

void meow(int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("meow\n")
    }
}

#include <cs50.h>
#include <stdio.h>

int main(void)

{
    int x = get_int("x: ");
    int y = get_int("y: ");

    printf("%i + y\n")
}

#include <stdio.h>
int main(void)
{
    for (int i = 0; i < 3; i++)
    {   
        for (int j = 0; j < 3; j++)
    }
}

// Calcuulator

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int x = get_int("x: ");
    int y = get_int("y: ");

    double z = (double) x / (double) y;
    printf("%.20f\n",z);
}