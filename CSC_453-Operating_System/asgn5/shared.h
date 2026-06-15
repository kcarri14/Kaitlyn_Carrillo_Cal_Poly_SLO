#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


#define DIRECT_ZONES 7
#define READ_SIZE 512
#define PARTITION_OFFSET 0x1BE
#define PARTITION_SIZE 16
#define MINIX_MAGIC 0x4D5A

int fs_start_byte_offset;
struct superblock { 
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

struct inode {
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

struct parition_table_entry{
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

struct directory_entry{
    uint32_t inode;
    unsigned name[60];
};

int open_image(char *imagefile, int is_partitioned,
 int is_subpart, int part_num, int subpart_num, 
int verbose, char* path, char* dstpath, int swtch);

int validate_partition_table(FILE *fp, int part_num, int base_offset
        , int verbose);

int locate_superblock(FILE* imagefile, int offset, int verbose);

int compute_filesystem(FILE *imagefile,uint16_t blocksize, 
                        int16_t i_blocks, int16_t z_blocks, int verbose);


int walking_directories(FILE *imagefile, struct inode cur_inode, int verbose
, uint16_t blocksize);


int minls(FILE *imagefile, struct inode last_inode, 
uint16_t blocksize, int verbose);


int minget(FILE *imagefile, struct inode last_inode, uint16_t blocksize, 
int verbose);

int support_zones(FILE *imagefile, struct inode last_inode, uint16_t blocksize, 
int verbose, char token);

