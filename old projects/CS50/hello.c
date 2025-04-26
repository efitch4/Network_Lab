#include <cs50.h>
#include <stdio.h>

int main(void) {
    int height;
    do {
        height = get_int("Height: ");
    }
    while (height < 1);
    for (int row = 0; row < height; row++) {
    for (int column = 0; column < height - row - 1; column++) {
            printf(" ");
        }

        for (int hash = 0; hash <= row; hash++) {
            printf("#");
        }

        printf("\n");
    }
}
