#define GNU_SOURCE
#include <stdio.h>
#include <string.h>

void get_line_thing(FILE *fp){
    char *line = NULL;
    size_t len = 0;
    ssize_t read; 

    char *second_last_line = NULL;
    char *last_line = NULL;

    while ((read = getline(&line, &len, fp)) != -1){
        if (second_last_line){
            free(second_last_line);
        }
        second_last_line = last_line;
        last_line = strdup(line);
    }

    if (last_line = NULL){
        printf("File is empty");
    }else if(second_last_line= NULL){
        printf("%s", last_line);
    }else{
        printf("%s\n%s\n", second_last_line, last_line);
    }

    free(second_last_line);
    free(last_line);
    free(line);


}


int main(char argc, char *argv[]){
    FILE *fp;

    if (argv == 2){
        fp = fopen(argv[1], "r");
    }else{
        perror("Error in file");
    }

    get_line_thing(fp);

    fclose(fp);

    return 0;

}