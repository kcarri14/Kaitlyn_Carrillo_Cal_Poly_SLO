#include <stdio.h>

void line_inter(char *str){
        if(str[0] == '-'){
            printf("%s\n", str);
        }
    
}


int main(int argc, char *argv[]){
    for (int i = 1; i < argc; i++){
        line_inter(argv[i]);
    }

    return 0;
}
