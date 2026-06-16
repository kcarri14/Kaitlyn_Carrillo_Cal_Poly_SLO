#include <stdio.h>
#include <ctype.h>

//counter function to count the words, chars, and lines
void counter(FILE *fp, int *words, int *chars, int *lines){
    // checks if you are in a word
    int inWord = 0 ;
    int ch;
// reads the characters in the file as long as its not at the end of the file
    while ((ch = fgetc(fp)) != EOF){
        // goes through every character an adds one to the variable
        putchar(ch);
        (*chars)++;
        // goes through the lines to find either a\n or \0 and counts how many lines there are
        if(ch == '\n' || ch == '\0'){
            (*lines)++;
        }
        // checks if the program is in a word and if it is then itll return true and false if its not
        //and wil count how many words there are
        if (isspace(ch)){
            inWord = 0;
        }
        else if(!inWord){
            inWord =1;
            (*words)++;
        }
    }
    
    
}

int main(int argc, char *argv[]){
    // creates variables for lines, words, and chars and a place to put the file in 
    FILE* fp;
    int lines = 0;
    int words = 0;
    int chars = 0;
    // if the array of arguments is equal to 2 then it will open the file to be read
    if (argc == 2){

        fp = fopen(argv[1], "r");

    }else{ // if user doesnt have file they can input words 
        fp = stdin;
    }
    
    counter(fp, &lines, &words, &chars);

    // close file once done
    if (fp != stdin){
        fclose(fp);
    }
    // print the stats that were calculated 
    printf("Words: %d\nChars: %d\nLines: %d\n", lines, words, chars);

    return 0;
}
