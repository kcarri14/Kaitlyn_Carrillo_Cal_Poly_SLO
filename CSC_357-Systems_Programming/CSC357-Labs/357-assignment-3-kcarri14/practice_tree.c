#include <stdio.h>
#include <sys/stat.h>
#include <dirent.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

void print_entry(char *name, int level, int hidden_size){
    //print tabs for every level
    for(int i = 0; i < level-1; i++){
        printf("|   ");
    }
    //print tab when opening directory
    if(level > 0){
        printf("|-- ");
    }
    //print directory name
    printf("%s", name);
    //if the person wants to see the size of the files
    if(hidden_size){
        struct stat size_byte;
        if(stat(name, &size_byte)== 0){
            printf(" [size: %lld]", (long long)size_byte.st_size);
        }else{
            perror("Error: No size stats");
        }
    }
    //print newline
    printf("\n");
}

void list_dir(char *path,int level, int hidden_file, int hidden_size){
    //get the current directory with as much memory as needed
    char *previous_dir = getcwd(NULL, 0);
    if(previous_dir == NULL){
        perror("Error: failed to get absolute path");
        return;
    }
    
    if(chdir(path) != 0){
        perror("Error: Failed to change");
        free(previous_dir);
        return;
    }
    //open directory
    DIR *directory = opendir(".");
    if (directory == NULL){
        perror("Error: No directory here");
        chdir(previous_dir);
        free(previous_dir);
        return;
    }
    struct dirent *entry;
    while((entry = readdir(directory)) != NULL){
        //skip . and .. 
        if(strcmp(entry-> d_name, "." ) == 0 || strcmp(entry->d_name, "..") == 0){
            continue;
        }
        //skip hidden files unless they want to see them
        if(!hidden_file && entry ->d_name[0]== '.'){
            continue;
        }
        
        //print the entries
        print_entry(entry->d_name, level, hidden_size);

        struct stat more_directories;
        if(stat(entry->d_name, &more_directories) == 0 && S_ISDIR(more_directories.st_mode)){
            //allocate memory for the next path in the directory
            char *new_path = malloc(strlen(path) + strlen(entry ->d_name)+ 2);
            if(new_path == NULL){
                perror("Error: failed memory allocation");
                closedir(directory);
                chdir(previous_dir);
                free(previous_dir);
                return;
            }
            //construct the new path for the call
            sprintf(new_path, "%s/%s", path, entry ->d_name);
            list_dir(new_path, level + 1, hidden_file, hidden_size);
            free(new_path);
        }else if(stat(entry->d_name, &more_directories) != 0){
            perror("Error: cant access the entry names");
        }
    }
    //close directory
    closedir(directory);
    if(chdir(previous_dir) != 0){
        perror("Error: Failed to return to the previous directory");
    }
    free(previous_dir);
}


int main(int argc, char *argv[]){
    //initialize variables
    int hidden_file = 0;
    int hidden_size = 0;
    int index = 1;

    for (int i = 1; i < argc; i++){
        // if arguments have -a in them then change the variable
        if(strcmp(argv[i], "-a") == 0){
            hidden_file = 1;
        // if arguments have -s in them then change the variable    
        }else if(strcmp(argv[i], "-s") == 0){
            hidden_size = 1;
        }else{
            index = i;
            break;
        }
    }
    
    if(argc == 1 || index == argc){
        list_dir(".", 0, hidden_file, hidden_size);
    }else{
        for(int i = index; i< argc; i++){
            list_dir(argv[i], 1, hidden_file, hidden_size);
        }
    }
    return 0;
}
