#include <stdio.h>
#include <sys/stat.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>

void print_entry(char *path, char *name, int level, int hidden_size){
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
        if(stat(path, &size_byte)== 0){
            printf(" [size: %lld]", (long long)size_byte.st_size);
        }else{
            perror("Error: No size stats");
        }
    }
    //print newline
    printf("\n");
}

void list_dir(char *path,int level, int hidden_file, int hidden_size){
    DIR *directory = opendir(path);
    if (directory == NULL){
        perror("Error: No directory here");
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
        char entire_path[4096];
        snprintf(entire_path, sizeof(entire_path), "%s/%s", path, entry ->d_name);

        print_entry(entire_path, entry->d_name, level, hidden_size);
        //check if 
        struct stat more_directories;
        if(stat(entire_path, &more_directories) == 0 && S_ISDIR(more_directories.st_mode)){
            list_dir(entire_path, level + 1, hidden_file, hidden_size);
        }
    }
    //close directory
    closedir(directory);
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
