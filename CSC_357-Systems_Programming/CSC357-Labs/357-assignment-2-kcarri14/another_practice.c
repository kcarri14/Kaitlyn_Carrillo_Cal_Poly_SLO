#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

#define max_length 32
#define max_inodes 1024

// Structure to represent a directory entry
typedef struct {
    uint32_t num_inode;
    char name[max_length];
} Directory_Entry;

// Structure to hold inode data
typedef struct {
    uint32_t inode_num;
    char type;  // 'd' for directory, 'f' for file
    int is_used;
    Directory_Entry entries[max_length];
    int num_entries;
} Entry;

// Array of inodes
Entry inodes[max_inodes];
uint32_t current_directory = 0;  // root directory is inode 0

// Utility to find the next available inode
int find_next_available_inode() {
    for (int i = 0; i < max_inodes; i++) {
        if (!inodes[i].is_used) {
            return i;
        }
    }
    return -1;
}

// Load the inodes list from the file
int load_inodes() {
    FILE *file = fopen("inodes_list", "rb");
    if (!file) {
        perror("Error opening file");
        return 1;
    }

    uint32_t inode_number;
    char indicator;
    size_t count = 0;

    while (fread(&inode_number, sizeof(uint32_t), 1, file) == 1 &&
           fread(&indicator, sizeof(char), 1, file) == 1) {
        if (indicator == 'd' || indicator == 'f') {
            inodes[count].inode_num = inode_number;
            inodes[count].type = indicator;
            inodes[count].is_used = 1;  // Mark as used
            inodes[count].num_entries = 0;  // Initialize with no entries
            count++;
        }
    }

    fclose(file);
    return 0;
}

// Change to a directory by inode number
int cd(char *name) {
    unsigned long unsigned_inodes_num = strtoul(name, NULL, 10);
    if (unsigned_inodes_num >= max_inodes || !inodes[unsigned_inodes_num].is_used || inodes[unsigned_inodes_num].type != 'd') {
        printf("Invalid directory\n");
        return -1;
    }
    current_directory = unsigned_inodes_num;
    return 0;
}

// List the contents of the current directory
void ls() {
    if (inodes[current_directory].type == 'd') {
        for (int i = 0; i < inodes[current_directory].num_entries; i++) {
            Directory_Entry entry = inodes[current_directory].entries[i];
            printf("%u %s\n", entry.num_inode, entry.name);
        }
    } else {
        printf("Error: Current inode is not a directory.\n");
    }
}

// Create a new directory
int mkdir(char *name) {
    int inode_index = find_next_available_inode();
    if (inode_index == -1) {
        printf("Error: No available inodes\n");
        return -1;
    }

    // Mark the new inode as a directory
    inodes[inode_index].inode_num = inode_index;
    inodes[inode_index].type = 'd';
    inodes[inode_index].is_used = 1;
    inodes[inode_index].num_entries = 0;  // New directory has no entries initially

    // Add the new directory to the current directory's entries
    inodes[current_directory].entries[inodes[current_directory].num_entries].num_inode = inode_index;
    strcpy(inodes[current_directory].entries[inodes[current_directory].num_entries].name, name);
    inodes[current_directory].num_entries++;

    printf("Directory '%s' created with inode %d\n", name, inode_index);
    return 0;
}

// Create a new file
int touch(char *name) {
    int inode_index = find_next_available_inode();
    if (inode_index == -1) {
        printf("Error: No available inodes\n");
        return -1;
    }

    // Mark the new inode as a file
    inodes[inode_index].inode_num = inode_index;
    inodes[inode_index].type = 'f';
    inodes[inode_index].is_used = 1;

    // Add the new file to the current directory's entries
    inodes[current_directory].entries[inodes[current_directory].num_entries].num_inode = inode_index;
    strcpy(inodes[current_directory].entries[inodes[current_directory].num_entries].name, name);
    inodes[current_directory].num_entries++;

    printf("File '%s' created with inode %d\n", name, inode_index);
    return 0;
}

// Command interface for interacting with the filesystem
int interface() {
    char command[32];
    char file_command[32];
    char argument[32];
    char *token;
    char *delim = " ";

    while (1) {
        printf("> ");
        fgets(command, sizeof(command), stdin);
        command[strcspn(command, "\n")] = 0;
        token = strtok(command, delim);
        if (token != NULL) {
            strcpy(file_command, token);
        } else {
            printf("No token found\n");
            return 1;
        }
        token = strtok(NULL, delim);
        if (token != NULL) {
            strcpy(argument, token);
        } else {
            argument[0] = '\0';
        }

        if (strcmp(file_command, "exit") == 0) {
            break;
        } else if (strcmp(file_command, "ls") == 0) {
            ls();
        } else if (strcmp(file_command, "cd") == 0) {
            if (argument[0] != '\0') {
                cd(argument);
            } else {
                printf("No name given\n");
            }
        } else if (strcmp(file_command, "mkdir") == 0) {
            if (argument[0] != '\0') {
                mkdir(argument);
            } else {
                printf("No name given\n");
            }
        } else if (strcmp(file_command, "touch") == 0) {
            if (argument[0] != '\0') {
                touch(argument);
            } else {
                printf("No name given\n");
            }
        } else {
            printf("Error: Unknown command\n");
        }
    }
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <directory>\n", argv[0]);
        return 1;
    }

    if (chdir(argv[1]) != 0) {
        perror("Error: Could not change the directory\n");
        return 1;
    }

    if (load_inodes() == -1) {
        printf("Failed to load inode\n");
        return 1;
    }

    interface();
    return 0;
}