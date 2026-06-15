#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>


#define DIRECT_ZONES 7
#define READ_SIZE 512
unsigned char buffer[READ_SIZE];
#define PARTITION_OFFSET 0x1BE
#define SUPERBLOCK_OFFSET 1024
#define BYTE_OFFSET 16
#define VALID_PART_TABLE_BYTE_510 0x55
#define VALID_PART_TABLE_BYTE_511 0xAA
#define MINIX_PART_TYPE 0x81
#define MAGIC_NUMBER 0x4d5a
#define FT_MASK 0170000
#define DIRECTORY 0040000
#define REG_FILE 0100000
#define DIRECTORY_SIZE 64
#define NAME_LENGTH 60
#define ORP 0000400
#define OWP 0000200
#define OEP 0000100
#define GRP 0000040
#define GWP 0000020
#define GEP 0000010
#define OTRP 0000004
#define OTWP 0000002
#define OTEP 0000001

int fs_start_byte_offset;
char *g_srcpath;
char* g_dstpath;
int inode_table_region;
int log_size;

int ls_or_get;

struct __attribute__ (( __packed__ )) superblock { 
    /* on disk. These fields and orientation are non–negotiable */
    uint32_t ninodes; /* number of inodes in this filesystem */
    uint16_t pad1; /* make things line up properly */
    int16_t i_blocks; /* # of blocks used by inode bit map */
    int16_t z_blocks; /* # of blocks used by zone bit map */
    uint16_t firstdata; /* number of first data zone */
    int16_t log_zone_size; /* log2 of blocks per zone */
    int16_t pad2; /* make things line up again */
    uint32_t max_file; /* maximum file size */
    uint32_t zones; /* number of zones on disk */
    int16_t magic; /* magic number */
    int16_t pad3; /* make things line up again */
    uint16_t blocksize; /* block size in bytes */
    uint8_t subversion; /* filesystem sub–version */
};

struct __attribute__ (( __packed__ )) inode {
    uint16_t mode; /* mode */
    uint16_t links; /* number or links */
    uint16_t uid;
    uint16_t gid;
    uint32_t size;
    int32_t atime;
    int32_t mtime;
    int32_t ctime;
    uint32_t zone[DIRECT_ZONES];
    uint32_t indirect;
    uint32_t two_indirect;
    uint32_t unused;
};

struct __attribute__ (( __packed__ )) parition_table_entry{
    uint8_t bootind;
    uint8_t start_head;
    uint8_t start_sec;
    uint8_t start_cyl;
    uint8_t type; 
    uint8_t end_head; 
    uint8_t end_sec;
    uint8_t end_cyl;
    uint32_t lFirst; 
    uint32_t size; 
};

struct __attribute__ (( __packed__ )) directory_entry{
    uint32_t inode;
    unsigned char name[NAME_LENGTH];
};

int validate_partition_table(FILE *fp, int part_num, int base_offset
        , int verbose);
int locate_superblock(FILE* imagefile, int offset, int verbose);

int compute_filesystem(FILE *imagefile,uint16_t blocksize, 
                        int16_t i_blocks, int16_t z_blocks, int verbose);

int walking_directories(FILE *imagefile, struct inode cur_inode, int verbose
, uint16_t blocksize);

int minls(FILE *imagefile, struct inode last_inode, uint16_t blocksize, 
int verbose);
int minget(FILE *imagefile, struct inode last_inode, uint16_t blocksize, 
int verbose);


int open_image(char *imagefile, int is_partitioned, 
int is_subpart, int part_num, int subpart_num, int verbose, 
char* srcpath, char* dstpath, int switch_num){

    //set globals for later
    g_srcpath = srcpath;
    g_dstpath = dstpath;
    ls_or_get = switch_num;
    
    // open image and read file for reading
    FILE *fp = fopen(imagefile, "rb");
    if(fp == NULL){
        fprintf(stderr, "open_image: Cannot open imagefile\n");
        exit(EXIT_FAILURE);
    }
    // compute offset
    // if unpartitioned start is 0
    if (is_partitioned == 0){
        fs_start_byte_offset = 0; 
    }else{
        // if partitioned, read partition table and pick the 
        if(is_subpart == 0){
            int start = validate_partition_table(fp, 
            part_num, fs_start_byte_offset, verbose);
            fs_start_byte_offset = start; 
        }else{
        // if subpartitioned, find primary parition
            int primary_start = validate_partition_table(fp, 
                                part_num, fs_start_byte_offset, verbose);
            int sub_start = validate_partition_table(fp, 
                                subpart_num, primary_start, verbose);
            fs_start_byte_offset = sub_start;
        }
        
    }
    locate_superblock(fp, fs_start_byte_offset, verbose);

    return 0;
}

int validate_partition_table(FILE *fp, int part_num, int base_offset
                            , int verbose){
    // read the first sector
    if (fseek(fp, base_offset, SEEK_SET) != 0){
        fprintf(stderr, "validate_partition_table: fseek \n");
        exit(EXIT_FAILURE);
    }
    
    if (!fread(buffer, 1, READ_SIZE, fp)) {
        fprintf(stderr, "validate_partition_table: fread MBR\n");
        exit(EXIT_FAILURE);
    }
    //verbose
    if(verbose){
        fprintf(stderr, "buffer 510: %d\n", buffer[510]);
        fprintf(stderr, "buffer 511: %d\n", buffer[511]);
    }
    // validate the parition table signature bytes
    if(buffer[510] != VALID_PART_TABLE_BYTE_510 
    || buffer[511] != VALID_PART_TABLE_BYTE_511){
        fprintf(stderr, "Not a valid partition table\n");
        exit(EXIT_FAILURE);
    }
    // locate the 4 parition entires at offset 0x1BE
    struct parition_table_entry pte;
    if (fseek(fp, base_offset+ PARTITION_OFFSET + part_num * 
        BYTE_OFFSET, SEEK_SET) != 0){
        fprintf(stderr, "validate_partition_table: fseek 2\n");
        exit(EXIT_FAILURE);
    }
    size_t pte_read = fread(&pte, 1, sizeof(pte), fp);
    if (!pte_read) {
        fprintf(stderr, "validate_partition_table: fread pte_read\n");
        exit(EXIT_FAILURE);
    }
    
    if(verbose){
        fprintf(stderr, "Partition entry %d:\n", part_num);
        fprintf(stderr, "  bootind:     0x%02X\n", pte.bootind);
        fprintf(stderr, "  type:        0x%02X\n", pte.type);
        fprintf(stderr, "  lFirst:      %u (sectors)\n", pte.lFirst);
        fprintf(stderr, "  size:        %u (sectors)\n", pte.size);
        fprintf(stderr, "  start CHS:   head=%u sec=%u cyl=%u\n",
            pte.start_head, pte.start_sec, pte.start_cyl);
        fprintf(stderr, "  end CHS:     head=%u sec=%u cyl=%u\n",
            pte.end_head, pte.end_sec, pte.end_cyl);
    }
    //check the type is Minix (0x81)
    if(pte.type != MINIX_PART_TYPE){
        fprintf(stderr, 
        "validate_partition_table: Wrong Partition type for MINIX\n");
        exit(EXIT_FAILURE);
    }
    // covert chosen lFirst to a byte offset(lFirst * 512) 
    //and add it to the apropriate base
    return pte.lFirst * READ_SIZE;
}

int locate_superblock(FILE* imagefile, int offset, int verbose){
    // filesystem offest 1024 bytes
    if (fseek(imagefile, offset + SUPERBLOCK_OFFSET, SEEK_SET) != 0){
        fprintf(stderr, "locate_superblock: fseek\n");
        exit(EXIT_FAILURE);
    }
    // read the superblock fields and validate the magic number
    struct superblock sup;
    // everything into the superblock struct
    if (fread(&sup, 1, sizeof(sup), imagefile) != sizeof(sup)) {
        fprintf(stderr, "locate_superblock: fread superblock\n");
        exit(EXIT_FAILURE);
    }

    // Minix 0x4D5A
    if(sup.magic != MAGIC_NUMBER){
        fprintf(stderr, "Bad Magic Number. %d\n", sup.magic);
        exit(EXIT_FAILURE);
    }
    //if -v is set, print superblock info to stderr
    if(verbose){
        fprintf(stderr, "Superblock Contents:\n");
        fprintf(stderr, "Stored Fields:\n");
        fprintf(stderr, "  blocksize:   %u\n", sup.blocksize);
        fprintf(stderr, "  firstdata:   %u\n", sup.firstdata);
        fprintf(stderr, "  i_blocks:    %u\n", sup.i_blocks);
        fprintf(stderr, "  z_blocks:    %u\n", sup.z_blocks);
        fprintf(stderr, "  log_zone:    %u  (zone size: %u)\n", 
        sup.log_zone_size, sup.blocksize);
        fprintf(stderr, "  magic:       %u\n", sup.magic);
        fprintf(stderr, "  max_size:    %u\n", sup.max_file);
        fprintf(stderr, "  ninodes:     %u\n", sup.ninodes);
        fprintf(stderr, "  pad1:        %u\n", sup.pad1);
        fprintf(stderr, "  pad2:        %u\n", sup.pad2);
        fprintf(stderr, "  pad3:        %u\n", sup.pad3);
        fprintf(stderr, "  subversion:  %u\n", sup.subversion);
    }
    log_size = sup.log_zone_size;

    compute_filesystem(imagefile, sup.blocksize, sup.i_blocks, 
    sup.z_blocks, verbose);

    return 0;
}

int compute_filesystem(FILE *imagefile,uint16_t blocksize, 
                        int16_t i_blocks, int16_t z_blocks, int verbose){
    //compute imap region (inodes are 64 bytes each)
    int imap_region = i_blocks * blocksize;
    //compute zone bitmap region
    int zone_region = z_blocks * blocksize;
    // compute inode table region
    inode_table_region = fs_start_byte_offset + (2 * blocksize + 
    imap_region + zone_region);
    
    if (fseek(imagefile, inode_table_region, SEEK_SET) != 0){
        fprintf(stderr, "compute_filesystem: fseek\n");
        exit(EXIT_FAILURE);
    }
    // compute where inode #1 is located in the inode table, then read it
    struct inode i;
    if (fread(&i, 1, sizeof(i), imagefile) != sizeof(i)) {
        fprintf(stderr, "compute_filesystem: fread inodes\n");
        exit(EXIT_FAILURE);
    }
    // validate it is a directory
    if((i.mode & FT_MASK) != DIRECTORY){
        fprintf(stderr, "compute_filesystem: Not a valid directory\n");
        exit(EXIT_FAILURE);
    }
    
    // if -v, print inode fields to stderr
    if(verbose){
        fprintf(stderr, "Inode 1 :\n");
        fprintf(stderr, "  mode:         %u\n", i.mode);
        fprintf(stderr, "  links:        %u\n", i.links);
        fprintf(stderr, "  uid:          %u\n", i.uid);
        fprintf(stderr, "  gid:          %u\n", i.gid);
        fprintf(stderr, "  size:         %u\n", i.size);
        fprintf(stderr, "  atime:        %u\n", i.atime);
        fprintf(stderr, "  mtime:        %u\n", i.mtime);
        fprintf(stderr, "  ctime:        %u\n", i.ctime);
        fprintf(stderr, "  Direct zones:         \n");
        fprintf(stderr, "       zone[0]:         %d\n", i.zone[0]);
        fprintf(stderr, "       zone[1]:         %d\n", i.zone[1]);
        fprintf(stderr, "       zone[2]:         %d\n", i.zone[2]);
        fprintf(stderr, "       zone[3]:         %d\n", i.zone[3]);
        fprintf(stderr, "       zone[4]:         %d\n", i.zone[4]);
        fprintf(stderr, "       zone[5]:         %d\n", i.zone[5]);
        fprintf(stderr, "       zone[6]:         %d\n", i.zone[6]);
        fprintf(stderr, "  indirect:     %u\n", i.indirect);
        fprintf(stderr, "  two_indirect: %u\n", i.two_indirect);
        fprintf(stderr, "  unused:       %u\n", i.unused);
    }

    walking_directories(imagefile, i, verbose, blocksize);
   
    return 0;
}

struct inode read_inode(FILE *imagefile, uint32_t inode_number){
    //find offest to the next inode
    int next_inode_offset = inode_table_region + 
    (inode_number -1) * sizeof(struct inode);
    //seek to the offset
    if (fseek(imagefile, next_inode_offset, SEEK_SET) != 0){
        fprintf(stderr, "read_inode: fseek \n");
        exit(EXIT_FAILURE);
    }
    //read the inode into a struct
    struct inode next_inode;
    if (fread(&next_inode, 1, sizeof(next_inode),
        imagefile) != sizeof(next_inode)) {
        fprintf(stderr, "read_inode: fread next_inode\n");
        exit(EXIT_FAILURE);
    }

    return next_inode;
}


int walking_directories(FILE *imagefile, struct inode cur_inode, int verbose
, uint16_t blocksize){
    //if the path is not root
    if(strcmp(g_srcpath, "/") != 0){
        // start at root inode
        int current_inode_num = 1;

        char *path_copy = strdup(g_srcpath);

        char *token = strtok(path_copy, "/");
        int zone_size = blocksize << log_size;
        // for each path component:
        while (token != NULL){
            if (token[0] == '\0'){
                token = strtok(NULL, "/");
                continue;
            }
            // confirm current inode is a directory
            if((cur_inode.mode & FT_MASK) != DIRECTORY){
                fprintf(stderr, 
                "walking_directories: Current inode is not a directory: %s\n"
                , token);
                free(path_copy);
                exit(EXIT_FAILURE);
            }
            
            // read its direcotry file data(from its zone)
            uint32_t remaining = cur_inode.size;
            uint32_t next_inode_num = 0;
            unsigned char zone_buf[blocksize];
            int i;
            // use direct zones first
            for(i = 0; i < DIRECT_ZONES && remaining > 0 && 
            next_inode_num == 0; i++){
                uint32_t zone = cur_inode.zone[i];
                if(zone == 0){
                    uint32_t take;
                    if (remaining < blocksize){
                        take = remaining;
                    }else{
                        take = blocksize;
                    }
                    remaining -= take;
                    continue;
                }
                

                int zone_byte_offset = fs_start_byte_offset + 
                (zone * zone_size);

                if (fseek(imagefile, zone_byte_offset, SEEK_SET) != 0){
                    fprintf(stderr, 
                    "walking_directories: fseek zone- %d\n",
                    i);
                    exit(EXIT_FAILURE);
                }
                if (fread(zone_buf, 1, blocksize, imagefile) != blocksize) {
                    fprintf(stderr, 
                    "walking_directories: fread zones zone- %d\n", i);
                    free(path_copy);
                    exit(EXIT_FAILURE);
                }

                uint32_t take;
                if (remaining < blocksize){
                    take = remaining;
                }else{
                    take = blocksize;
                }
                remaining -= take;
                int entries = take / DIRECTORY_SIZE;
                // scan directory entries or a matching name
                int entry;
                for(entry = 0; entry < entries; entry++){
                    struct directory_entry *direct = 
                    (struct directory_entry *)(zone_buf + 
                    entry * DIRECTORY_SIZE);
                    char namebuf[NAME_LENGTH + 1];
                    memcpy(namebuf, direct->name, NAME_LENGTH);
                    namebuf[NAME_LENGTH] = '\0'; 
                    if(verbose){
                        fprintf(stderr, "Directory Name: %s\n", namebuf);
                        fprintf(stderr, "Directory Inode: %u\n", 
                    direct->inode);
                    }
                    if(direct->inode == 0){
                        continue;
                    }
                    size_t tlen = strlen(token);
                    if(strcmp(namebuf, token) == 0){
                        // filenames are stored in a fixed 60-byte field
                        if (tlen == NAME_LENGTH || direct->name[tlen] == '\0'){
                            // extract the inode number from that entry
                            next_inode_num = direct->inode;
                            
                        }
                        break;
                    }

                }
                
            }

            //indirect
            if(next_inode_num == 0 && cur_inode.indirect != 0){
                uint32_t zone = cur_inode.indirect;
                

                unsigned char indirect_buf[blocksize];
                
                int zone_byte_offset = fs_start_byte_offset + 
                (zone * zone_size);

                if (fseek(imagefile, zone_byte_offset, SEEK_SET) != 0){
                    fprintf(stderr, "walking_directories: fseek\n");
                    exit(EXIT_FAILURE);
                }

                if (fread(indirect_buf, 1, blocksize, 
                imagefile) != blocksize) {
                    fprintf(stderr, "walking_directories: fread zones\n");
                    exit(EXIT_FAILURE);
                }
                uint32_t n = blocksize / 4;
                uint32_t *tbl = (uint32_t *)indirect_buf;
                unsigned char zone_buf[zone_size];
                int i;
                for(i = 0; i < n && remaining > 0; i++){
                    uint32_t data_zone = tbl[i];
                    if(data_zone == 0){
                        continue;
                    }
                    
                    int zone_byte_offset = fs_start_byte_offset + 
                    (data_zone * zone_size);
                    
                    if (fseek(imagefile, zone_byte_offset, SEEK_SET) != 0){
                        fprintf(stderr, 
                        "walking_directories: fseek indirect\n");
                        exit(EXIT_FAILURE);
                    }
                    if (fread(zone_buf, 1, zone_size,
                     imagefile) != zone_size) {
                        fprintf(stderr, 
                        "walking_directories: fread zones indirect\n");
                        exit(EXIT_FAILURE);
                    }
                    
                    
                    int entries = zone_size / DIRECTORY_SIZE;
                   
                    // scan directory entries or a matching name
                    int entry;
                    for(entry = 0; entry < entries; entry++){
                        struct directory_entry *direct = 
                        (struct directory_entry *)(zone_buf + 
                        entry * DIRECTORY_SIZE);
                        char namebuf[NAME_LENGTH + 1];
                        memcpy(namebuf, direct->name, NAME_LENGTH);
                        namebuf[NAME_LENGTH] = '\0'; 
                        if(verbose){
                            fprintf(stderr, "Directory Name: %s\n", namebuf);
                            fprintf(stderr, "Directory Inode: %u\n", 
                        direct->inode);
                        }
                        if(direct->inode == 0){
                            continue;
                        }
                        size_t tlen = strlen(token);
                        if(strcmp(namebuf, token) == 0){
                            // filenames are stored in a fixed 60-byte field
                            if (tlen == NAME_LENGTH || 
                            direct->name[tlen] == '\0'){
                                // extract the inode number from that entry
                                next_inode_num = direct->inode;
                                
                            }
                            break;
                        }
                    }
                }
            }
            //double indirect zone
            if(remaining > 0){
                uint32_t n = blocksize / sizeof(uint32_t);
                uint32_t take;
                
                if(cur_inode.two_indirect == 0){
                    uint32_t span = n * zone_size;
                    if (remaining < span){
                        take = remaining;
                    }else{
                        take = span;
                    }
                    remaining -= take;
                }
                uint32_t double_indirect_zone = cur_inode.two_indirect;

                unsigned char double_indirect_buf[blocksize];
                
                uint64_t zone_byte_offset = fs_start_byte_offset + 
                (double_indirect_zone * zone_size);
                
                if (fseek(imagefile, zone_byte_offset, SEEK_SET) != 0){
                    fprintf(stderr,
                    "walking_directories: fseek double indirect\n");
                    exit(EXIT_FAILURE);
                }
                if (fread(double_indirect_buf, 1, blocksize, 
                imagefile) != blocksize) {
                    fprintf(stderr,
                     "walking_directories: fread zones double indirect\n");
                    exit(EXIT_FAILURE);
                }
                
                uint32_t *tbl = (uint32_t *)double_indirect_buf;
                unsigned char double_indirect_zone_buffer[blocksize];
                int j;
                for(j = 0; j < n && remaining > 0; j++){
                    uint32_t indirect_data_zone = tbl[j];
                    //if the data zone is 0, then skip it
                    if(indirect_data_zone == 0){
                        continue;
                    }else{

                        uint64_t zone_byte_offset = fs_start_byte_offset + 
                        (indirect_data_zone * zone_size);

                        if (fseek(imagefile, zone_byte_offset,
                         SEEK_SET) != 0){
                            fprintf(stderr, 
                    "walking_directories: fseek double indirect data zone\n");
                            exit(EXIT_FAILURE);
                        }
                        if (fread(double_indirect_zone_buffer, 1, 
                        blocksize, imagefile) != blocksize) {
                            fprintf(stderr, 
                    "walking_directories: fread double indirect data zone\n");
                            exit(EXIT_FAILURE);
                        }
                         
                        int entries = zone_size / DIRECTORY_SIZE;
                    
                        // scan directory entries or a matching name
                        int entry;
                        for(entry = 0; entry < entries; entry++){
                            struct directory_entry *direct = 
                            (struct directory_entry *)(zone_buf + 
                            entry * DIRECTORY_SIZE);
                            char namebuf[NAME_LENGTH + 1];
                            memcpy(namebuf, direct->name, NAME_LENGTH);
                            namebuf[NAME_LENGTH] = '\0'; 
                            if(verbose){
                                fprintf(stderr, 
                                "Directory Name: %s\n", namebuf);
                                fprintf(stderr, "Directory Inode: %u\n", 
                            direct->inode);
                            }
                            if(direct->inode == 0){
                                continue;
                            }
                            size_t tlen = strlen(token);
                            if(strcmp(namebuf, token) == 0){
                                // filenames are stored in a fixed 60-byte field
                                if (tlen == NAME_LENGTH || 
                                direct->name[tlen] == '\0'){
                                    // extract the inode number from that entry
                                    next_inode_num = direct->inode;
                                    
                                }
                                break;
                            }
                        }
                    }
                }
            }
            //read that inode and continue
            struct inode next_inode = read_inode(imagefile, next_inode_num);
            current_inode_num = next_inode_num;
            cur_inode = next_inode;
            if (verbose) {
                fprintf(stderr, "%s -> inode %u\n", token, current_inode_num);
            }
            if(verbose){
                fprintf(stderr, "Inode 1 :\n");
                fprintf(stderr, "  mode:         %u\n", next_inode.mode);
                fprintf(stderr, "  links:        %u\n", next_inode.links);
                fprintf(stderr, "  uid:          %u\n", next_inode.uid);
                fprintf(stderr, "  gid:          %u\n", next_inode.gid);
                fprintf(stderr, "  size:         %u\n", next_inode.size);
                fprintf(stderr, "  atime:        %u\n", next_inode.atime);
                fprintf(stderr, "  mtime:        %u\n", next_inode.mtime);
                fprintf(stderr, "  ctime:        %u\n", next_inode.ctime);
                fprintf(stderr, "  Direct zones:         \n");
                fprintf(stderr, "       zone[0]:         %d\n", 
                next_inode.zone[0]);
                fprintf(stderr, "       zone[1]:         %d\n", 
                next_inode.zone[1]);
                fprintf(stderr, "       zone[2]:         %d\n",
                 next_inode.zone[2]);
                fprintf(stderr, "       zone[3]:         %d\n",
                 next_inode.zone[3]);
                fprintf(stderr, "       zone[4]:         %d\n", 
                next_inode.zone[4]);
                fprintf(stderr, "       zone[5]:         %d\n", 
                next_inode.zone[5]);
                fprintf(stderr, "       zone[6]:         %d\n",
                 next_inode.zone[6]);
                fprintf(stderr, "  indirect:     %u\n", next_inode.indirect);
                fprintf(stderr, "  two_indirect: %u\n", 
                next_inode.two_indirect);
                fprintf(stderr, "  unused:       %u\n", next_inode.unused);
            }

            token = strtok(NULL, "/");
        
        }
        free(path_copy);
        
    }
    if(ls_or_get == 1){
        minls(imagefile, cur_inode, blocksize, verbose);
    }else{
        minget(imagefile, cur_inode, blocksize, verbose);
    }

    return 0;
}
int perm(uint16_t mode, char permissions[11]){
    if((mode & FT_MASK) == DIRECTORY){
            permissions[0] = 'd';
        }else{
            permissions[0] = '-';
        }
        if(mode & ORP){
            permissions[1] = 'r';
        }else{
            permissions[1] = '-';
        }
        if(mode & OWP){
            permissions[2] = 'w';
        }else{
            permissions[2] = '-';
        }
        if(mode & OEP){
            permissions[3] = 'x';
        }else{
            permissions[3] = '-';
        }
        if(mode & GRP){
            permissions[4] = 'r';
        }else{
            permissions[4] = '-';
        }
        if(mode & GWP){
            permissions[5] = 'w';
        }else{
            permissions[5] = '-';
        }
        if(mode & GEP){
            permissions[6] = 'x';
        }else{
            permissions[6] = '-';
        }
        if(mode & OTRP){
            permissions[7] = 'r';
        }else{
            permissions[7] = '-';
        }
        if(mode & OTWP){
            permissions[8] = 'w';
        }else{
            permissions[8] = '-';
        }
        if(mode & OTEP){
            permissions[9] = 'x';
        }else{
            permissions[9] = '-';
        }
        permissions[10] = '\0';

        return 0;
}


int minls(FILE *imagefile, struct inode last_inode, uint16_t blocksize, 
int verbose){
    // if its a file
    if((last_inode.mode & FT_MASK) == REG_FILE){
        // print permissions string, then file size, then canonicalized path
        char permissions[11];
        perm(last_inode.mode, permissions);
        int i;
        if(g_srcpath[0] == '/'){
            for (i = 0; g_srcpath[i] != '\0'; i++) {
                g_srcpath[i] = g_srcpath[i + 1]; 
            }
        }
        if(verbose){
            fprintf(stderr, "Inode Mode: %d\n", last_inode.mode);
        }
        printf("%s  %u  %s\n", permissions, last_inode.size, g_srcpath);
        return 0;

    // if its a directory
    }else if ((last_inode.mode & FT_MASK) == DIRECTORY){
        // print path:
        if(g_srcpath[0] != '/'){
            printf("/");
        }
        printf("%s: \n", g_srcpath);
        // list every direcotry entry as if each were file/directory line:
        uint32_t remaining = last_inode.size;
        uint32_t next_inode_num = 0;
        int zone_size = blocksize << log_size;
        
        int i;
        // use direct zones first
        for(i = 0; i < DIRECT_ZONES && remaining > 0 && 
        next_inode_num == 0; i++){
            uint32_t zone = last_inode.zone[i];
            uint32_t take;
            if (remaining < blocksize){
                take = remaining;
            }else{
                take = blocksize;
            }
            remaining -= take;
            if(verbose){
                fprintf(stderr, "remaining: %d\n", remaining);
            }
    
            unsigned char zone_buf[zone_size];

            int zone_byte_offset = fs_start_byte_offset + 
            (zone * zone_size);

            if (fseek(imagefile, zone_byte_offset, SEEK_SET) != 0){
                fprintf(stderr, "minls: fseek zone- %d\n", i);
                exit(EXIT_FAILURE);
            }
            if (fread(zone_buf, 1, zone_size, imagefile) != zone_size) {
                fprintf(stderr, "minls: fread zone- %d\n", i);
                exit(EXIT_FAILURE);
            }
            

            int entries = take / DIRECTORY_SIZE;
            // scan directory entries or a matching name
            int entry;
            for(entry = 0; entry < entries; entry++){
                struct directory_entry *direct = 
                (struct directory_entry *)(zone_buf + 
                entry * DIRECTORY_SIZE);

                if (direct->inode != 0){
                    char namebuf[NAME_LENGTH + 1];
                    memcpy(namebuf, direct->name, NAME_LENGTH);
                    namebuf[NAME_LENGTH] = '\0'; 

                    struct inode more_inodes = read_inode(imagefile,
                    direct->inode);
                    char permissions[11];
                    perm(more_inodes.mode, permissions);
                    printf("%s  %u  %s\n", permissions, 
                    more_inodes.size, namebuf);

                }
            }
        }
        //indirect_zone
        if(remaining > 0){
            uint32_t n = blocksize / sizeof(uint32_t);
            uint32_t take;
            //if indirect is 0, then there are no files or directories
            //so just pass them and subtract from remaining
            if(last_inode.indirect == 0){
                uint32_t span = n * zone_size;
                if (remaining < span){
                    take = remaining;
                }else{
                    take = span;
                }
                remaining -= take;
                if(verbose){
                    fprintf(stderr, "remaining: %d\n", remaining);
                }
            }

            uint32_t zone = last_inode.indirect;
            int zone_size = blocksize << log_size;

            unsigned char indirect_buf[blocksize];

            int zone_byte_offset = fs_start_byte_offset + 
            (zone * zone_size);

            if (fseek(imagefile, zone_byte_offset, SEEK_SET) != 0){
                fprintf(stderr, "minls: fseek indirect\n");
                exit(EXIT_FAILURE);
            }
            if (fread(indirect_buf, 1, blocksize, imagefile)!= blocksize){
                fprintf(stderr, "minls: fread zones indirect\n");
                exit(EXIT_FAILURE);
            }
            uint32_t *tbl = (uint32_t *)indirect_buf;
            unsigned char zone_buf[zone_size];
            for(i = 0; i < n && remaining > 0; i++){
                uint32_t data_zone = tbl[i];
                if (remaining < blocksize){
                    take = remaining;
                }else{
                    take = zone_size;
                }
                
                if(data_zone == 0){
                    if (remaining < blocksize){
                        take = remaining;
                    }else{
                        take = zone_size;
                    }
                    remaining -= take;
                    if(verbose){
                        fprintf(stderr, "remaining: %d\n", remaining);
                    }
                }

                int zone_byte_offset = fs_start_byte_offset + 
                (data_zone * zone_size);

                if (fseek(imagefile, zone_byte_offset, SEEK_SET) != 0){
                    fprintf(stderr, "minls: fseek indirect zone\n");
                    exit(EXIT_FAILURE);
                }
                if (fread(zone_buf, 1, take, imagefile) != take) {
                    fprintf(stderr, 
                    "minls: fread zones indirect zone\n");
                    exit(EXIT_FAILURE);
                }
                
                
                int entries = take / DIRECTORY_SIZE;

                // scan directory entries or a matching name
                int entry;
                for(entry = 0; entry < entries; entry++){
                    struct directory_entry *direct = 
                    (struct directory_entry *)(zone_buf + 
                    entry * DIRECTORY_SIZE);

                    if (direct->inode != 0){
                        char namebuf[NAME_LENGTH + 1];
                        memcpy(namebuf, direct->name, NAME_LENGTH);
                        namebuf[NAME_LENGTH] = '\0'; 

                        struct inode more_inodes = read_inode(imagefile,
                        direct->inode);
                        char permissions[11];
                        perm(more_inodes.mode, permissions);
                        printf("%s  %u  %s\n", permissions, 
                        more_inodes.size, namebuf);

                    }
                }
                remaining -= take;
                if(verbose){
                    fprintf(stderr, "remaining: %d\n", remaining);
                }
            }
        }
        //double indirect zone
        if(remaining > 0){
            uint32_t n = blocksize / sizeof(uint32_t);
            uint32_t take;
            
            if(last_inode.two_indirect == 0){
                uint32_t span = n * zone_size;
                if (remaining < span){
                    take = remaining;
                }else{
                    take = span;
                }
                remaining -= take;
                if(verbose){
                    fprintf(stderr, "remaining: %d\n", remaining);
                }
            }
            uint32_t double_indirect_zone = last_inode.two_indirect;

            unsigned char double_indirect_buf[blocksize];
            
            uint64_t zone_byte_offset = fs_start_byte_offset + 
            (double_indirect_zone * zone_size);
            
            if (fseek(imagefile, zone_byte_offset, SEEK_SET) != 0){
                fprintf(stderr, "minls: fseek double indirect zone\n");
                exit(EXIT_FAILURE);
            }
            if (fread(double_indirect_buf, 1, blocksize, 
            imagefile) != blocksize) {
                fprintf(stderr, "minls: fread zones double indirect zone\n");
                exit(EXIT_FAILURE);
            }
            
            uint32_t *tbl = (uint32_t *)double_indirect_buf;
            unsigned char double_indirect_zone_buffer[blocksize];
            int j;
            for(j = 0; j < n && remaining > 0; j++){
                uint32_t indirect_data_zone = tbl[j];
                //if the data zone is 0, then skip it
                if(indirect_data_zone == 0){
                    continue;
                }else{

                    uint64_t zone_byte_offset = fs_start_byte_offset + 
                    (indirect_data_zone * zone_size);

                    if (fseek(imagefile, zone_byte_offset, SEEK_SET) != 0){
                        fprintf(stderr, 
                        "minls: fseek double indirect data zone\n");
                        exit(EXIT_FAILURE);
                    }
                    if (fread(double_indirect_zone_buffer, 1, 
                    blocksize, imagefile) != blocksize) {
                        fprintf(stderr, 
                        "minls: fread double indirect data zone\n");
                        exit(EXIT_FAILURE);
                    }

                    int entries = take / DIRECTORY_SIZE;
                    // scan directory entries or a matching name
                    int entry;
                    for(entry = 0; entry < entries; entry++){
                        struct directory_entry *direct = 
                        (struct directory_entry *)(double_indirect_zone_buffer 
                        + entry * DIRECTORY_SIZE);

                        if (direct->inode != 0){
                            char namebuf[NAME_LENGTH + 1];
                            memcpy(namebuf, direct->name, NAME_LENGTH);
                            namebuf[NAME_LENGTH] = '\0'; 

                            struct inode more_inodes = read_inode(imagefile,
                            direct->inode);
                            char permissions[11];
                            perm(more_inodes.mode, permissions);
                            printf("%s  %u  %s\n", permissions, 
                            more_inodes.size, namebuf);

                        }
                    }
                    
                }
            }
            remaining -= take;
            if(verbose){
                fprintf(stderr, "remaining: %d\n", remaining);
            }
        }
        return 0;   
    }else{
        fprintf(stderr, 
        "minls: Unsupported file type my dude! Only files and directories\n");
        exit(EXIT_FAILURE);
        return 1;
    }
    
}

int minget(FILE *imagefile, struct inode last_inode, uint16_t blocksize, 
int verbose){
    // after resolving the srcpath
    // verify final inode is a regualr file
    if((last_inode.mode & FT_MASK) == REG_FILE){
        // if dstpath omitted: write to stdout
        FILE *out = stdout;
        if(g_dstpath != NULL){
            // else create/write that output file
            out = fopen(g_dstpath, "wb");
            if(!out){
                fprintf(stderr, "minget: cannot open dst %s", g_dstpath);
                return 1;
            }
        }
    
        uint32_t remaining = last_inode.size;
        uint32_t zone_size = blocksize << log_size;

        if (verbose) {
            fprintf(stderr, "minget: size=%u blocksize=%u zone_size=%u\n",
                    remaining, (unsigned)blocksize, zone_size);
        }

        unsigned char zone_buf[zone_size];
        
        int i;
        // use direct zones first
        for(i = 0; i < DIRECT_ZONES && remaining > 0; i++){
            uint32_t zone = last_inode.zone[i];
            uint32_t take;
            if (remaining < zone_size){
                take = remaining;
            }else{
                take = zone_size;
            }

            if(zone == 0){
                // handle holes: if any zone pointer is 0, 
                //output zero bytes for that zone region
                unsigned char *zero_buffer = calloc(1, take);
                if (fwrite(zero_buffer, 1, take, out) != take) {
                    fprintf(stderr, "minget: write failed\n");
                    free(zero_buffer);
                    if(out != stdout){
                        fclose(out);
                    }
                    return 1;
                }
                free(zero_buffer);

            }else{
                uint64_t zone_byte_offset = fs_start_byte_offset + 
                (zone * zone_size);
                if (fseek(imagefile, zone_byte_offset, SEEK_SET) != 0){
                    fprintf(stderr, 
                    "minget: fseek zone- %d\n", i);
                    exit(EXIT_FAILURE);
                }
                if (fread(zone_buf, 1, zone_size, imagefile) != zone_size){
                    fprintf(stderr, "minget: fread zone- %d\n", i);
                    exit(EXIT_FAILURE);
                }
                // copy exactly inode.size bytes 
                //by reading the file's zone in order
                if (fwrite(zone_buf, 1, take, out) != take){
                    fprintf(stderr, "minget: write failed\n");
                    free(zone_buf);
                    if(out != stdout){
                        fclose(out);
                    }
                    return 1;
                }
                
            }
            remaining -= take;
            if(verbose){
                fprintf(stderr, "remaining: %d\n", remaining);
            }
        }
        
        //indirect
        if(remaining > 0){
            uint32_t n = blocksize / sizeof(uint32_t);
                fprintf(stderr, "we are in the indirect\n");
                uint32_t indirect_zone = last_inode.indirect;
                fprintf(stderr, "indirect_zone: %d\n", indirect_zone);

                unsigned char indirect_buf[blocksize];

                if(indirect_zone == 0){
                    int whole_indirect = zone_size * n;
                    unsigned char *zero_buffer = calloc(1, whole_indirect);
                    if (fwrite(zero_buffer, 1, whole_indirect, out) 
                    != whole_indirect) {
                        fprintf(stderr, "minget: write failed\n");
                        free(zero_buffer);
                        if(out != stdout){
                            fclose(out);
                        }
                        return -1;
                    }
                    free(zero_buffer);
                    remaining -= whole_indirect;
                    if(verbose){
                        fprintf(stderr, "remaining: %d\n", remaining);
                    }

                }else{

                    uint64_t zone_byte_offset = fs_start_byte_offset + 
                    (indirect_zone * zone_size);


                    if (fseek(imagefile, zone_byte_offset, SEEK_SET) != 0){
                        fprintf(stderr, "minget: fseek indirect\n");
                        exit(EXIT_FAILURE);
                    }
                    if (fread(indirect_buf, 1, blocksize, 
                    imagefile) != blocksize) {
                        fprintf(stderr, "minget: fread zones indirect\n");
                        exit(EXIT_FAILURE);
                    }
                    uint32_t *tbl = (uint32_t *)indirect_buf;
                    unsigned char zone_buffer[zone_size];
                    int j;
                    for(j = 0; j < n && remaining > 0; j++){
                        uint32_t data_zone = tbl[j];
                        uint32_t take;
                        if (remaining < zone_size){
                            take = remaining;
                        }else{
                            take = zone_size;
                        }
                        
                        if(data_zone == 0){
                            // handle holes: if any zone pointer is 0, 
                            //output zero bytes for that zone region
                            unsigned char *zero_buffer = calloc(1, take);
                            if (fwrite(zero_buffer, 1, take, out) != take) {
                                fprintf(stderr, "minget: write failed\n");
                                free(zero_buffer);
                                if(out != stdout){
                                    fclose(out);
                                }
                                return -1;
                            }
                            free(zero_buffer);

                        }else{

                            uint64_t zone_byte_offset = fs_start_byte_offset + 
                            (data_zone * zone_size);

                            if (fseek(imagefile, 
                            zone_byte_offset, SEEK_SET) != 0){
                                fprintf(stderr, 
                                "minget: fseek indirect data zone\n");
                                exit(EXIT_FAILURE);
                            }

                            if (fread(zone_buffer, 1, zone_size,
                            imagefile) != zone_size) {
                                fprintf(stderr,
                                 "minget: fread indirect data zone\n" );
                                exit(EXIT_FAILURE);
                            }
                            // copy exactly inode.size bytes 
                            //by reading the file's zone in order

                            if (fwrite(zone_buffer, 1, take, out) != take){
                                fprintf(stderr, "minget: write failed\n");
                                free(zone_buffer);
                                if(out != stdout){
                                    fclose(out);
                                }
                                return 1;
                            }
                            
                        }
                        remaining -= take;
                        if(verbose){
                            fprintf(stderr, "remaining: %d\n", remaining);
                        }

                    }
                }
                
        }
        //double indirect zone
        if(remaining > 0 && last_inode.two_indirect != 0){
            uint32_t n = blocksize / sizeof(uint32_t);
            unsigned char double_indirect_buf[blocksize];
            uint32_t double_indirect_zone = last_inode.two_indirect;       
            uint64_t zone_byte_offset = fs_start_byte_offset + 
            (double_indirect_zone * zone_size);
            
            if (fseek(imagefile, zone_byte_offset, SEEK_SET) != 0){
                fprintf(stderr, "minget: fseek\n");
                exit(EXIT_FAILURE);
            }

            if (fread(double_indirect_buf, 1, blocksize, 
            imagefile) != blocksize) {
                fprintf(stderr, "minget fread zone\n");
                exit(EXIT_FAILURE);
            }
            uint32_t *tbl = (uint32_t *)double_indirect_buf;

            unsigned char double_indirect_zone_buffer[blocksize];
            unsigned char data_buffer[zone_size];
            int j;
            uint32_t take;         
            for(j = 0; j < blocksize && remaining > 0; j++){
                uint32_t indirect_data_zone = tbl[j];
                if(indirect_data_zone == 0){
                        uint32_t span = n * zone_size;
                        if (remaining < span){
                            take = remaining;
                        }else{
                            take = span;
                        }
                        // handle holes: if any zone pointer is 0, 
                        //output zero bytes for that zone region
                        unsigned char *zero_buffer = calloc(1, take);
                        if (fwrite(zero_buffer, 1, take, out) != take) {
                            fprintf(stderr, "minget: write failed\n");
                            free(zero_buffer);
                            if(out != stdout){
                                fclose(out);
                            }
                            return 1;
                        }
                        free(zero_buffer);
                        remaining -= take;
                        if(verbose){
                            fprintf(stderr, "remaining: %d\n", remaining);
                        }
                        continue;                   
                }else{
                    uint64_t zone_byte_offset = fs_start_byte_offset + 
                    (indirect_data_zone * zone_size);

                    if (fseek(imagefile, zone_byte_offset, SEEK_SET) != 0){
                        fprintf(stderr, 
                        "minget: fseek double indirect level 1\n");
                        exit(EXIT_FAILURE);
                    }
                    if (fread(double_indirect_zone_buffer,
                        1, blocksize, imagefile) != blocksize) {
                        fprintf(stderr,
                        "minget: fread double indirect level 1\n");
                        exit(EXIT_FAILURE);
                    }
                    
                    uint32_t *double_indirect = (uint32_t *)
                    double_indirect_zone_buffer;

                    int k; 
                    for(k = 0; k< n && remaining > 0; k++){
                        uint32_t data_zone = double_indirect[k];
                        if (remaining < zone_size){
                            take = remaining;
                        }else{
                            take = zone_size;
                        }

                        uint64_t zone_byte_offset = 
                        fs_start_byte_offset + (data_zone * zone_size);

                        if (fseek(imagefile,
                            zone_byte_offset, SEEK_SET) != 0){
                            fprintf(stderr, 
                            "minget: fseek double indirect data zone\n");
                            exit(EXIT_FAILURE);
                        }

                        if (fread(data_buffer, 1, 
                        zone_size, imagefile) != zone_size) {
                            fprintf(stderr, 
                            "minget: fread double indirect data zone\n");
                            exit(EXIT_FAILURE);
                        }
                        // copy exactly inode.size bytes 
                        //by reading the file's zone in order
                        ;
                        if (fwrite(data_buffer, 1, take, out) != take){
                            fprintf(stderr, "minget: write failed\n");
                            free(data_buffer);
                            if(out != stdout){
                                fclose(out);
                            }
                            return 1;
                        }
                        remaining -= take;
                        if(verbose){
                            fprintf(stderr, "remaining: %d\n", remaining);
                        }
                    }
                    
                }
            }
        }
        if(out != stdout){
            fclose(out);
            return 0;
        }
    }else{
        fprintf(stderr, "minget not a File\n");
        exit(EXIT_FAILURE);
    }
    return -1;
}

