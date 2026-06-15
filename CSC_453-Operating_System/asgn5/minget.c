#include <stdio.h>
#include <stdlib.h>
#include "shared.h"
#include <string.h>
#include <unistd.h>

int parse_int(char *s, int *out){
    char *end = NULL;
    long val = strtol(s, &end, 10);

    // No digits were found
    if (end == s) {
        return 0;
    }
    if (*end != '\0') {
        return 0;
    }
    if (val < 0 || val > 3) {
        return 0;
    }

    *out = (int)val;
    return 1;
}

int main(int argc, char *argv[]){
    int partition_flag = 0;
    int subpartition_flag = 0;
    int verbose_flag = 0;
    int partition_num = -1; 
    int subpartition_num = -1;
    char *srcpath;
    char *imagefile;
    char *dstpath;
    int opt;

    if (argc == 1){
        fprintf(stderr, 
    "Usage: ./minget [-v] [-p part] [-s sub] imagefile srcpath [ dstpath ]\n");
    fprintf(stderr, 
    "Options:\n"); 
    fprintf(stderr, 
    "-p part --- select partition for filesystem (default: none)\n");
    fprintf(stderr, 
    "-s sub --- select subpartition for filesystem (default: none)\n");
    fprintf(stderr, "-h help --- print usage information and exit\n");
    fprintf(stderr, "-v verbose --- increase verbosity level\n");
        exit(EXIT_FAILURE);
    }

    while((opt = getopt(argc, argv, "vp:s:")) != -1){
        switch(opt){
        case 'v':
            verbose_flag = 1;
            break;
        case 'p':
            partition_flag = 1;
            partition_num = atoi(optarg);
            break;
        case 's':
            subpartition_flag = 1;
            subpartition_num = atoi(optarg);
            break;
        case ':':
            fprintf(stderr, "Option -%c requires an argument\n", optopt);
            fprintf(stderr, 
    "Usage: ./minget [-v] [-p part] [-s sub] imagefile srcpath [ dstpath ]\n");
    fprintf(stderr, 
    "Options:\n"); 
    fprintf(stderr, 
    "-p part --- select partition for filesystem (default: none)\n");
    fprintf(stderr, 
    "-s sub --- select subpartition for filesystem (default: none)\n");
    fprintf(stderr, "-h help --- print usage information and exit\n");
    fprintf(stderr, "-v verbose --- increase verbosity level\n");
            exit(EXIT_FAILURE);
        case '?':
            fprintf(stderr, 
    "Usage: ./minget [-v] [-p part] [-s sub] imagefile srcpath [ dstpath ]\n");
    fprintf(stderr, 
    "Options:\n"); 
    fprintf(stderr, 
    "-p part --- select partition for filesystem (default: none)\n");
    fprintf(stderr, 
    "-s sub --- select subpartition for filesystem (default: none)\n");
    fprintf(stderr, "-h help --- print usage information and exit\n");
    fprintf(stderr, "-v verbose --- increase verbosity level\n");
            exit(EXIT_FAILURE);
        }

    }
    if(subpartition_flag && !partition_flag){
        fprintf(stderr, "Error: -s requires -p\n");
        fprintf(stderr, 
    "Usage: ./minget [-v] [-p part] [-s sub] imagefile srcpath [dstpath]\n");
    fprintf(stderr, 
    "Options:\n"); 
    fprintf(stderr, 
    "-p part --- select partition for filesystem (default: none)\n");
    fprintf(stderr, 
    "-s sub --- select subpartition for filesystem (default: none)\n");
    fprintf(stderr, "-h help --- print usage information and exit\n");
    fprintf(stderr, "-v verbose --- increase verbosity level\n");
        exit(EXIT_FAILURE);
    }
    
    int remaining_args = argc - optind; 
    //printf("remaining: %d\n", remaining_args);
    if (remaining_args < 2 || remaining_args > 3){
        fprintf(stderr, "Wrong number of arguments: %d\n", remaining_args);
        return -1;
    }else{
        imagefile = argv[optind];
        if (remaining_args == 3){
            srcpath = argv[optind + 1];
            dstpath = argv[optind + 2];
        }else{
            srcpath = argv[optind + 1];
            dstpath = NULL;
        }
    }
    //printf("imagefile: %s\n", imagefile);
    //printf("srcpath: %s\n", srcpath);
    //printf("dstpath: %s\n", dstpath);
    //printf("verbose: %d\n", verbose_flag);

    open_image(imagefile, partition_flag, subpartition_flag,
    partition_num, subpartition_num, verbose_flag, srcpath, dstpath, 2);

    return 0;
}