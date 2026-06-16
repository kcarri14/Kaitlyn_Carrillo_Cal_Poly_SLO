#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#define max_length 32
#define inodes_list "inodes_list"
#define max_inodes 1024
//structure to represent a directory entry
typedef struct{
    uint32_t num_inode;
    char name[max_length];
}Directory_Entry;
// strcuture to hold data for inodes like number and character
typedef struct{
    uint32_t inode_num;
    char type;
    int is_used;
    Directory_Entry entries[max_length];
    int num_entries;
}Entry;

//Array of inodes from entry
Entry inodes[max_inodes];
//initalixations 0 as the current/root directory
uint32_t current_directory = -1;

// check the memory allocation
void *checked_malloc(int len)
{
    void *p = malloc(len);
    if (!p)
    {
        fprintf(stderr,"\nRan out of memory!\n");
        exit(1);
    }
    return p;
}
// take a unisgned long integer and turn it into a string
char *uint32_to_str(uint32_t i)
{
   int length = snprintf(NULL, 0, "%lu", (unsigned long)i);       // pretend to print to a string to get length
   char* str = checked_malloc(length + 1);                        // allocate space for the actual string
   snprintf(str, length + 1, "%lu", (unsigned long)i);            // print to string

   return str;
}
//find the next avaiable inode num to be able to make a directory or a file
int find_next_available_inode(){
    for(int i=0; i < max_inodes; i++){
        if(!inodes[i].is_used){
            return i;
        }
    }
    return -1;
}

int load_inodes() {
    FILE *file = fopen("inodes_list", "rb"); //open inodes list
    if (!file) {                        // see if file exists
        perror("Error opening file\n");
        return 1;
    }

    uint32_t inode_number; //buffer for binary number
    char indicator;       // buffer for type descriptor
    size_t count = 0;     // tells me how many inodes are already in use

    while (fread(&inode_number, sizeof(uint32_t), 1, file) == 1 &&
           fread(&indicator, sizeof(char), 1, file) == 1) {
        if (indicator == 'd' || indicator == 'f') {
            printf("Inode: %u, Type: %c\n", inode_number, indicator);
        } else {
            fprintf(stderr, "Invalid file type indicator: %c for Inode: %u\n", indicator, inode_number);
        }
        inodes[count].inode_num = inode_number; // stores inode number in array
        inodes[count].type = indicator;  // stores inode type in array
        inodes[count].is_used = 1;  // marks inode as used
        count++;
    }
    if (inodes[0].type == 'd'){  // makes sure the first inode is the root directory
        current_directory = 0;
    }

    fclose(file);
    return 0;
}




void cd(uint32_t cwd, char *name) {
    char *cwd_str = uint32_to_str(cwd); // Convert cwd (inode) to directory path string
    FILE *readDirect = fopen(cwd_str, "rb"); // Open the directory as a binary file
    uint32_t inode_holder;
    char directoryRead[max_length + 1]; // Buffer to hold the directory name (33 includes space for null terminator)

    free(cwd_str); // Free dynamically allocated string after use

    if (readDirect == NULL) {
        perror("Error: unable to open directory file\n");
        return;
    }

    // Read directory entries until we find a match for the provided name
    while (fread(&inode_holder, sizeof(uint32_t), 1, readDirect) == 1) {
        // Read the directory name
        fread(directoryRead, sizeof(char), max_length, readDirect);
        directoryRead[max_length] = '\0'; // Ensure null-termination

        // Check if the directory name matches the provided name
        if (strcmp(directoryRead, name) == 0) {
            // Check if the inode corresponds to a directory
            if (inodes[inode_holder].type == 'd') {
                // Change current directory to the new inode
                current_directory = inode_holder;
                fclose(readDirect);
                return;
            } else {
                perror("Error: not a directory\n");
                fclose(readDirect);
                return;
            }
        }
    }

    // If the loop completes without finding the directory, it doesn't exist
    fprintf(stderr, "Error: directory '%s' not found in current directory\n", name);
    fclose(readDirect);
}

void ls(){
    if (inodes[current_directory].type == 'd') {
        // Get the file name of the directory using its inode number
        char *file_name = uint32_to_str(inodes[current_directory].inode_num);
        FILE *readDirect = fopen(file_name, "rb");

        // Free the dynamically allocated string after use
        free(file_name);

        if (readDirect == NULL) {
            perror("Error: unable to open directory file");
            return;
        }

        // Read and print directory entries
        Directory_Entry dir_entry;
        while (fread(&dir_entry, sizeof(Directory_Entry), 1, readDirect) == 1) {
            printf("%u %s\n", dir_entry.num_inode, dir_entry.name);
        }

        fclose(readDirect);
    } else {
        printf("Error: Current inode is not a directory.\n");
    
    } 
}     

int mkdir(uint32_t cwd,char *name){
    // finds the next available inode
    uint32_t inode_index = find_next_available_inode();

    //marks it as used
    inodes[inode_index].is_used = 1;

    if(inode_index == -1){ //makes sure that there are still inodes
        printf("Error: No avaiable inodes\n");
        return -1;
    }

    //converts inode to str in order to open the file
    char *new_inode = uint32_to_str(inode_index);

    FILE *fp = fopen(new_inode, "wb");
    if(fp == NULL){
        perror("Error opening inodes list file\n");
        return 1;
    }
    // used to show the new directory
    char new[max_length] = ".";
    // used to show the parent directory
    char parent[max_length] = "..";

    // add to new to currrent
    fwrite(&inode_index, sizeof(uint32_t), 1, fp);
    fwrite(new, sizeof(char), sizeof(new), fp);

    // add parent to current
	fwrite(&cwd, sizeof(uint32_t), 1, fp);
    fwrite(parent, sizeof(char), sizeof(parent), fp);
    fclose(fp);

    //puts the binary rep of inode and the char type into the inodes list
    char c = 'd';
    FILE *file = fopen("inodes_list", "ab");
    if(file == NULL){
        perror("Error opening inodes list file\n");
        return 1;
    }
    fwrite(&inode_index, sizeof(uint32_t),1, file);
    fwrite(&c, sizeof(char), 1, file);
    fclose(file);

    // writes the new directory into the parent directory
    FILE *parent_file;
    char *parent_inode = uint32_to_str(cwd);
    parent_file = fopen(parent_inode, "ab");
    if(!parent_file) {
        printf("Error: Could not open the inode parent %s for appending\n", parent_inode);
        return 0;
    }

    char current_name[32];
    strncpy(current_name, name, max_length - 1);
    current_name[max_length - 1] = '\0';

    fwrite(&inode_index, sizeof(uint32_t), 1, parent_file);
    fwrite(current_name, sizeof(current_name), 1, parent_file);

    fclose(parent_file);
    // rereads the inodes list so that the new directory can be used
    FILE *inode_file = fopen("inodes_list", "rb");
    if (!inode_file) {
        perror("Error opening file\n");
        return 1;
    }

    uint32_t inode_number;
    char indicator;
    size_t count = 0;

    while (fread(&inode_number, sizeof(uint32_t), 1, inode_file) == 1 &&
           fread(&indicator, sizeof(char), 1, inode_file) == 1) {
        inodes[count].inode_num = inode_number;
        inodes[count].type = indicator;
        inodes[count].is_used = 1;  // Mark as used
        count++;
    }

    fclose(inode_file);
    return 0;
 

}


int touch(uint32_t cwd, char *name){
    // finds the next available inode
    int inode_index = find_next_available_inode();

    //marks it as used
    inodes[inode_index].is_used = 1;

    if(inode_index == -1){ //makes sure that there are still inodes
        printf("Error: No avaiable inodes\n");
        return -1;
    }
    // takes the inode and makes it into a string 
    char inodes_name[20];
    snprintf(inodes_name, sizeof(inodes_name), "%d", inode_index);

    FILE *fp = fopen(inodes_name, "wb");
    fwrite(name, sizeof(char), strlen(name), fp);
    
    fclose(fp);

    if(fp == NULL){
        perror("Error opening inodes list file\n");
        return 1;
    }

    //puts the binary rep of inode and the char type into the inodes list
    char c = 'f';
    FILE *file = fopen("inodes_list", "ab");
    if(file == NULL){
        perror("Error opening inodes list file\n");
        return 1;
    }
    fwrite(&inode_index, sizeof(uint32_t),1, file);
    fwrite(&c, sizeof(char), 1, file);
    fclose(file);

    // writes the new directory into the parent directory
    FILE *parent_file;
    char *parent_inode = uint32_to_str(cwd);
    parent_file = fopen(parent_inode, "ab");
    if(!parent_file) {
        printf("Error: Could not open the inode parent %s for appending\n", parent_inode);
        return 0;
    }

    char current_name[32];
    strncpy(current_name, name, max_length - 1);
    current_name[max_length - 1] = '\0';

    fwrite(&inode_index, sizeof(uint32_t), 1, parent_file);
    fwrite(current_name, sizeof(current_name), 1, parent_file);

    fclose(parent_file);
    return 0;
}

int interface(){
    //input commands
    char command[32];
    char file_command[32];
    char argument[32];
    char *token;
    char *delim = " ";
    
    while (1){
        printf("> ");
        //parses the stdin and puts them into different strings to be read for
        // differet functions
        fgets(command, sizeof(command), stdin); 
        command[strcspn(command, "\n")] = 0;
        token = strtok(command, delim);
        if(token != NULL){
            strcpy(file_command, token);
        }else{
            printf("No token found\n");
            return 1;
        }
        token = strtok(NULL, delim);
        if(token != NULL){
            strcpy(argument, token);
        }else{
            argument[0] = '\0';
        }

        if (strcmp(file_command, "exit") == 0){
            break;
        }else if(strcmp(file_command, "ls") == 0){
            ls();
        }else if(strcmp(file_command, "cd") == 0){
            if (argument[0] != '\0'){
                cd(current_directory, argument);
            }else{
                printf("No name given\n");
            }
                
        }else if(strcmp(file_command, "mkdir") == 0){
            if (argument[0] != '\0'){
                mkdir(current_directory, argument);
            }else{
                printf("No name given\n");
            }
        }else if(strcmp(file_command, "touch") == 0){
            if (argument[0] != '\0'){
                touch(current_directory, argument);
            }else{
                printf("No name given\n");
            }
        }else{
            printf("Error: Unknown command\n");
        }
    }
    return 0;

}



int main(int argc, char *argv[]){
    //REQ 1
    if(argc != 2){
        printf("Usage: %s <filename>\n", argv[0]);
        return 1;
    }
    //REQ 2
    
    if(chdir(argv[1]) != 0){
        perror("Error: Could not change the directory\n");
        return 1;
    }

    if(load_inodes() == -1){
        printf("Failed to load inode\n");
        return 1;
    }

    interface();
    return 0;

}