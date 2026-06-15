#include <minix/drivers.h>
#include <minix/driver.h>
#include <stdio.h>
#include <stdlib.h>
#include <minix/ds.h>
#include "secrets.h"

#include <minix/const.h>


/*
 * Function prototypes for the secret driver.
 */
FORWARD _PROTOTYPE( char * secret_name,   (void) );
FORWARD _PROTOTYPE( int secret_open,      (struct driver *d, message *m) );
FORWARD _PROTOTYPE( int secret_close,     (struct driver *d, message *m) );
FORWARD _PROTOTYPE( int secret_ioctl,     (struct driver *d, message *m) );
FORWARD _PROTOTYPE( struct device * secret_prepare, (int device) );
FORWARD _PROTOTYPE( int secret_transfer,  (int procnr, int opcode, 
                                          u64_t position, iovec_t *iov, 
                                          unsigned nr_req) );
FORWARD _PROTOTYPE( void secret_geometry, (struct partition *entry) );

/* SEF functions and variables. */
FORWARD _PROTOTYPE( void sef_local_startup, (void) );
FORWARD _PROTOTYPE( int sef_cb_init, (int type, sef_init_info_t *info) );
FORWARD _PROTOTYPE( int sef_cb_lu_state_save, (int) );
FORWARD _PROTOTYPE( int lu_state_restore, (void) );

/* Entry points to the secret driver. */
PRIVATE struct driver secret_tab =
{
    secret_name,
    secret_open,
    secret_close,
    secret_ioctl,
    secret_prepare,
    secret_transfer,
    nop_cleanup,
    secret_geometry,
    nop_alarm,
    nop_cancel,
    nop_select,
    nop_ioctl,
    do_nop,
};

/** Represents the /dev/secret device. */
PRIVATE struct device secret_device;

/** State variables */
PRIVATE int open_counter;
PRIVATE int read_counter;
PRIVATE uid_t owner;
PRIVATE size_t secret_len;
PRIVATE char secret_buf[SECRET_SIZE];
PRIVATE size_t read_pos;
PRIVATE size_t write_pos;



/*dont touch*/
PRIVATE char * secret_name(void)
{   
    printf("Kaitlyn was here");
    return "kaitlyn";
}

PRIVATE int secret_open(d, m)
    struct driver *d;
    message *m;
{
    /*check if secret is owned, if not, give ownership to user id
    if so, check if that owner is the one opening it, if so
    do what it says. if not dont open*/
    struct ucred cred;
    int r;
    int flags;
    //find flags from message
    flags = m->COUNT & (R_BIT | W_BIT);

    //check if it is read-write
    if(flags == (R_BIT | W_BIT)){
        return EACCES;
    }

    //get credentials from user
    r = getnucred(m->IO_ENDPT, &cred);
    if (r != OK){
        return r;
    }
    
    //check if it is owned already
    if(owner == (uid_t) - 1){
        owner = cred.uid;
        if(flags == R_BIT){
            open_counter++;
            read_counter++;
            return OK;
        }
        if(flags == W_BIT){
            open_counter++;
            return OK;
        }
    }else{
        //unallow writing in file again
        if(flags == W_BIT){
            return ENOSPC;
        }
        //make sure that only the owner can read it
        if(owner == cred.uid){
            if(flags == R_BIT){
                open_counter++;
                read_counter++;
                return OK;
            }    
        }
        return EACCES;
    }
    return OK;
}

PRIVATE int secret_close(d, m)
    struct driver *d;
    message *m;
{
    if(open_counter > 0){
        open_counter--;
    }
    //check if open counter is 0 and if it has been read at least once
    if(open_counter == 0 && read_counter > 0){
        owner = -1;
        secret_len = 0;
        read_pos = 0;
        write_pos = 0;
        read_counter = 0;
    }
    return OK;
}
/*dont touch*/
PRIVATE struct device * secret_prepare(dev)
    int dev;
{
    secret_device.dv_base.lo = 0;
    secret_device.dv_base.hi = 0;
    secret_device.dv_size.lo = SECRET_SIZE;
    secret_device.dv_size.hi = 0;
    return &secret_device;
}


PRIVATE int secret_transfer(proc_nr, opcode, position, iov, nr_req)
    int proc_nr;
    int opcode;
    u64_t position;
    iovec_t *iov;
    unsigned nr_req;
{
    int available, ret, space;
    size_t n;
    
    //transfer secret
    if(iov->iov_size == 0){
        return OK;
    }

    switch (opcode)
    {
        case DEV_GATHER_S:
            //check for space available in the buffer
            available = secret_len - read_pos;
            if (iov->iov_size > available){
                n = available;
            }else{
                n = iov->iov_size;
            }
            //copy to the user
            ret = sys_safecopyto(proc_nr, iov->iov_addr, 0,
                                (vir_bytes) (secret_buf + read_pos),
                                n, D);

            if (ret != OK){
                return ENOSPC;
            }
            //subtract from size
            iov->iov_size -=n;
            //move read position
            read_pos += n;
            break;

        case DEV_SCATTER_S:
            //make sure there is enough room
            space = SECRET_SIZE - write_pos;
            if(space == 0){
                    return ENOSPC;
            }
            //if the siz is too big, set it to the largest size
            if (iov->iov_size > SECRET_SIZE){
                n = SECRET_SIZE;
            }else{
                n = iov->iov_size;
            }
            //copy from user to driver
            ret = sys_safecopyfrom(proc_nr, iov->iov_addr, 0,
                                (vir_bytes)(secret_buf + write_pos),
                                n, D);
            iov->iov_size -=n;
            if (ret != OK){
                return ENOSPC;
            }
            write_pos +=n;
            if (secret_len > write_pos){
                secret_len = secret_len;
            }else{
                secret_len = write_pos;
            }
            break;

        default:
            return EINVAL;

        
        }
    return OK;
}
/*dont touch*/
PRIVATE void secret_geometry(entry)
    struct partition *entry;
{
    entry->cylinders = 0;
    entry->heads     = 0;
    entry->sectors   = 0;
}

PRIVATE int secret_ioctl(d, m) 
struct driver *d;
message *m;

{   
    int r;
    int res;
    struct ucred ucred;
    uid_t grantee;
    //if not SSGRANT, give error ENOTTY
    if(m->REQUEST != SSGRANT){
        return ENOTTY;
    }
    //get the credentials
    r = getnucred(m->IO_ENDPT, &ucred);
    if (r != OK){
        return ENOSPC;
    }
    //check that owner is correct
    if(ucred.uid == owner){
         /* the uid of the new owner of the secret */
        res = sys_safecopyfrom(m->IO_ENDPT, (vir_bytes)m->IO_GRANT,
            0, (vir_bytes)&grantee, sizeof(grantee), D);

        if (res != OK){
            return res;
        } 
        owner = grantee;
        return OK;
    }else{
        return EACCES;
    }
    
}

PRIVATE int sef_cb_lu_state_save(int state) {
/* Save the state. */
/*need to save the owner of the secret
 and the secret itself and where you are in the secret*/

    ds_publish_u32("open_counter", open_counter, DSF_OVERWRITE);
    ds_publish_u32("owner", owner, DSF_OVERWRITE);
    ds_publish_u32("secret_len", secret_len, DSF_OVERWRITE);
    ds_publish_u32("read_pos", read_pos, DSF_OVERWRITE);
    ds_publish_u32("write_pos", write_pos, DSF_OVERWRITE);
    ds_publish_u32("read_counter", read_counter, DSF_OVERWRITE);
    ds_publish_mem("secret_buf", secret_buf, SECRET_SIZE, DSF_OVERWRITE);

    return OK;
}

PRIVATE int lu_state_restore() {
/* Restore the state. */
    u32_t oc_value;
    u32_t owner_value;
    u32_t sl_value;
    u32_t rp_value;
    u32_t wp_value;
    u32_t rc_value;

    ds_retrieve_u32("read_counter", &rc_value);
    ds_delete_u32("read_counter");
    read_counter = (int) rc_value;

    ds_retrieve_u32("owner", &owner_value);
    ds_delete_u32("owner");
    owner = (int) owner_value;

    ds_retrieve_u32("open_counter", &oc_value);
    ds_delete_u32("open_counter");
    open_counter = (int) oc_value;


    ds_retrieve_u32("secret_len", &sl_value);
    ds_delete_u32("secret_len");
    secret_len = (int) sl_value;

    ds_retrieve_u32("read_pos", &rp_value);
    ds_delete_u32("read_pos");
    read_pos = (int) rp_value;

    ds_retrieve_u32("write_pos", &wp_value);
    ds_delete_u32("write_pos");
    write_pos = (int) wp_value;

    size_t len = SECRET_SIZE;
    ds_retrieve_mem("secret_buf", secret_buf, &len);
    ds_delete_mem("secret_buf");

    return OK;
}

PRIVATE void sef_local_startup()
{
    /*
     * Register init callbacks. Use the same function for all event types
     */
    sef_setcb_init_fresh(sef_cb_init);
    sef_setcb_init_lu(sef_cb_init);
    sef_setcb_init_restart(sef_cb_init);

    /*
     * Register live update callbacks.
     */
    /* - Agree to update immediately when LU is requested in a valid state. */
    sef_setcb_lu_prepare(sef_cb_lu_prepare_always_ready);
    /* - Support live update starting from any standard state. */
    sef_setcb_lu_state_isvalid(sef_cb_lu_state_isvalid_standard);
    /* - Register a custom routine to save the state. */
    sef_setcb_lu_state_save(sef_cb_lu_state_save);

    /* Let SEF perform startup. */
    sef_startup();
}

PRIVATE int sef_cb_init(int type, sef_init_info_t *info)
{
/* Initialize the secret driver. */
    int do_announce_driver = TRUE;
    switch(type) {
        case SEF_INIT_FRESH:
            open_counter = 0;
            owner = (uid_t)-1;
            secret_len = 0;
            read_pos = 0;
            write_pos = 0;
            read_counter =0;
            break;

        case SEF_INIT_LU:
            /* Restore the state. */
            lu_state_restore();
            do_announce_driver = FALSE;
            break;
        break;

        case SEF_INIT_RESTART:
            printf("The Secret Safe: I've just been restarted");
            open_counter = 0;
            owner = (uid_t)-1;
            secret_len = 0;
            read_pos = 0;
            write_pos = 0;
            read_counter =0;
            break;
    }

    /* Announce we are up when necessary. */
    if (do_announce_driver) {
        driver_announce();
    }

    /* Initialization completed successfully. */
    return OK;
}

PUBLIC int main(int argc, char **argv)
{
    /*
     * Perform initialization.
     */
    sef_local_startup();

    /*
     * Run the main loop.
     */
    printf("The Secret Safe ready for work.\n");
    driver_task(&secret_tab, DRIVER_STD);
    return OK;
}

