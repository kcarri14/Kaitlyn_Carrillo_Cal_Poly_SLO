#include <stdio.h>
#include <sys/stat.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>

// Function to print directory entries with indentation based on level
void print_entry(const char *name, int level, int hidden_size){
    for(int i = 0; i < level - 1; i++){
        printf("|   ");
    }
    if(level > 0){
        printf("|-- ");
    }
    printf("%s", name);

    if(hidden_size){
        struct stat size_byte;
        if(stat(name, &size_byte) == 0){
            printf(" [size: %lld]", (long long)size_byte.st_size);
        }else{
            perror("Error: Could not retrieve size");
        }
    }
    printf("\n");
}

// Recursive function to list directory contents
void list_dir(const char *path, int level, int hidden_file, int hidden_size){
    DIR *directory = opendir(path);
    if(directory == NULL){
        perror("Error: Could not open directory");
        return;
    }

    struct dirent *entry;
    while((entry = readdir(directory)) != NULL){
        // Skip . and ..
        if(strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0){
            continue;
        }

        // Skip hidden files if not requested
        if(!hidden_file && entry->d_name[0] == '.'){
            continue;
        }

        // Build the full path of the entry
        char full_path[4096];
        snprintf(full_path, sizeof(full_path), "%s/%s", path, entry->d_name);

        // Print the entry
        print_entry(entry->d_name, level, hidden_size);

        // Check if the entry is a directory and recursively list it
        struct stat entry_info;
        if(stat(full_path, &entry_info) == 0 && S_ISDIR(entry_info.st_mode)){
            list_dir(full_path, level + 1, hidden_file, hidden_size);
        }
    }
    closedir(directory);
}

int main(int argc, char *argv[]){
    int hidden_file = 0;
    int hidden_size = 0;
    int index = 1;

    // Parse command-line arguments
    for(int i = 1; i < argc; i++){
        if(strcmp(argv[i], "-a") == 0){
            hidden_file = 1;
        }else if(strcmp(argv[i], "-s") == 0){
            hidden_size = 1;
        }else{
            index = i;
            break;
        }
    }

 //determine the directory to list for the root directory
    char *path = (argc == 1 || index == argc) ? ".": argv[index];
    list_dir(path, 1, hidden_file, hidden_size);
    return 0;
}