#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void unique_lines(FILE *fp){
    char *current = NULL; // pointer to hold current line
    char *prev = NULL; // pointer to hold previous line
    size_t len = 0;  // holds the size of the buffer for getline
    ssize_t read; 

    // Read each line from the file
    while ((read = getline(&current, &len, fp) != -1)){
        // compares the current line to pervious line
        if (prev == NULL || strcmp(current, prev) != 0 ){
            // if it is different then it will print line
            printf( "%s", current);
            // free previous line memory
           free(prev);
           prev = strdup(current);

        }

    }
    // clean up and free the memory
    free(current);
    free(prev);
}


int main(int argc, char *argv[]){
    FILE *fp;

    // if the array of arguments is equal to 2 then it will open the file to be read
    if (argc == 2){

        fp = fopen(argv[1], "r");

    }else{ // if user doesnt have file they can input words 
        fp = stdin;
    }
    
    unique_lines(fp);

    // close file once done
    if (fp != stdin){
        fclose(fp);
    }

    return 0; 

}