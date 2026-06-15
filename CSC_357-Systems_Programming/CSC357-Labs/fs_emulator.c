#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>

#define INODES_MAX 1024
#define NAME_LENGTH_MAX 32
#define INODE_LIST_FILE "list_inodes"

//structure to represent an inode
typedef struct {
    uint32_t num_inode;
    char type; //'d' for directory, 'f' for file
}inode_e;
//structure to represent a dierectory entry
typedef struct {
    uint32_t num_inode;
    char name[NAME_LENGTH_MAX];
}directory_e;

//Array of inodes
inode_e inodes[INODES_MAX];

//current working direcoty inode
uint32_t current_inode = 0;

// function to check if a directory exists
int directory_exists(const char *path){
    struct stat statbuffer;
    return (stat(path, &statbuffer) == 0 && S_ISDIR(statbuffer.st_mode));
}
// function to convert an integer to a string
void integer_to_string(uint32_t num, char *buffer){
    snprintf(buffer, NAME_LENGTH_MAX, "%u", num);

}
//Load the inodes list from the file system directory
int load_inodeslist(){

    FILE *file = fopen("list_inodes", "rb");
    if(!file){
        perror("Error opening list");
        return -1;
    }

    fread(inodes, sizeof(inode_e), INODES_MAX, file);
    fclose(file);
    return 0;
          
}
// save the inode list back to the file system
void save_list(){
    FILE *file = fopen("list_inodes", "wb");
    if(!file){
        perror("Error opening list");
        exit(1);
    }
    fwrite(inodes, sizeof(inode_e), INODES_MAX, file);
    fclose(file);
}
//change the current directory
void change_directory(const char *name){
    char directory_filename[10];
    snprintf(directory_filename, sizeof(directory_filename), "%u", current_inode);
    FILE *directory_file = fopen("list_inodes", "rb");
    if(!directory_file){
        perror("Error opening directory\n");
        return;
    }
    directory_e entry;
    while(fread(&entry, sizeof(directory_e), INODES_MAX, directory_file)){
        if (strncmp(entry.name, name, NAME_LENGTH_MAX)==0){
            current_inode = entry.num_inode;
            if (inodes[entry.num_inode].type == 'd'){
                current_inode = entry.num_inode;
            }else{
                printf("Not a directory\n");
        }
        fclose(directory_file);
        return;
        }
    }
    printf("Directory not found\n");
    fclose(directory_file);
}
//list the contents of current directory
void list_contents(){
    char directory_filename[10];
    snprintf(directory_filename, sizeof(directory_filename), "%u", current_inode);
    FILE *directory_file = fopen("list_inodes", "rb");
    if(!directory_file){
        perror("Error opening directory\n");
        return;
    }
    directory_e entry;
    while(fread(&entry, sizeof(directory_e), INODES_MAX, directory_file)){
        printf("%u %s\n", entry.num_inode, entry.name);
    }
    fclose(directory_file);    
}
// create a new directory
void make_directory(const char *name){
    uint32_t new_inode = INODES_MAX;
    for(uint32_t i =0; i < INODES_MAX; i++){
        if(inodes[i].type == 0){ // Empty inode
            new_inode = i;
            break;
        }
    }
    if(new_inode == INODES_MAX){
        printf("No available inodes\n");
        return;
    }
    inodes[new_inode].num_inode = new_inode;
    inodes[new_inode].type = 'd';
    char directory_filename[10];
    snprintf(directory_filename, sizeof(directory_filename), "%u", current_inode);
    FILE *directory_file = fopen("list_inodes", "wb");
    if(!directory_file){
        perror("Error creating directory\n");
        return;
    }


}


int main(int argc, char *argv[]){
    if (argc != 2){
        fprintf(stderr, "Usage: %s <filename>\n", argv[0]);
        return 1;
    }

    if(chdir(*argv[1] != 0)){
        perror("Error changing directory\n");
        return 1;
    }

    load_inodeslist();


    if(inodes[0].type != 'd'){
        printf("Error: Root inode is not a directory\n");
        return 1;
    }


    char command[50];
    while(1){
        printf("> ");
        if(!fgets(command, sizeof(command), stdin)){
            break;
        }
        command[strcspn(command, "\n")] = "\0";

        if (strcmp(command, "exit") == 0){
            break;
        }else if (strncmp(command, "cd", 3) == 0){
            change_directory(command + 3);
        }else if (strncmp(command, "ls", 0) == 0){
            ls();
        }else if (strncmp(command, "mkdir", 6) == 0){
            make_directory(command +6);
        }else if (strncmp(command, "touch", 6) == 0){
            touch(command + 6);
        }else {
            printf("Error: unknown command\n");
        }
    }

    save_list();
}

struct inode_entry

{

   int inode_number;

   char type;

   struct entry *entries;

   int num_entries;

};






struct entry

{

   int reference_inode;

   char name[32]; 

};






char *uint32_to_str(uint32_t i)

{

   int length = snprintf(NULL, 0, "%lu", (unsigned long)i); 

   char *str = calloc(1, length + 1);                     

   snprintf(str, length + 1, "%lu", (unsigned long)i);      

   return str;

}