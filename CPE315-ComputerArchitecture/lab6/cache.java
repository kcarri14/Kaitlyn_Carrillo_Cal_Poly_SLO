
public class cache {
    public int hits;
    public int intoCache;
    public int blockSize;
    public int assoc;
    public int cacheSize;
    public int chunks;
    public int[][] tags;
    public boolean[][] beingUsed;
    public int[][] LRU;

    public cache(int cacheSize, int assoc, int blockSize){
        //set up all variables
        this.cacheSize = cacheSize;
        this.blockSize = blockSize * 4;
        this.assoc = assoc;
        //gets the total blocks that can fit
        int totalBlocks = cacheSize / this.blockSize;
        //gets number of blocks in each chunk
        this.chunks = totalBlocks / assoc;
        //keeps track of tag
        this.tags = new int[chunks][assoc];
        //keeps track if block is being used
        this.beingUsed = new boolean[chunks][assoc];
        //keeps track of least recently used
        this.LRU = new int[chunks][assoc];
        
        //initialize the LRU
        for (int i = 0; i < chunks; i++) {
            for (int j = 0; j < assoc; j++) {
                LRU[i][j] = j;
            }
        }
    }


    public void access_addr(int addr) {
        //used to count how many times accessed the cache
        intoCache++;
        int index = (addr / blockSize) % chunks;
        int tag = (addr / blockSize) / chunks;

        //looks though the tags to see if the one wantng access is in the cache
        for(int i = 0; i < assoc; i++){
            if(beingUsed[index][i] && tags[index][i] == tag){
                hits++;
                updateLRU(index, i);
                return;
            }
        }
        //if not it checks if any other chunks have an opening at the index or way
        for(int i = 0; i < assoc; i++){
            if(!beingUsed[index][i]){
                beingUsed[index][i] = true;
                tags[index][i] = tag;
                updateLRU(index, i);
                return;
            }
        }

        //if not then use LRU to replace
        //initialize for use in for loop
        int lru = 0 ;
        int maxLRU = LRU[index][0];
        
        for(int i = 1; i < assoc; i++){
            if(LRU[index][i]> maxLRU){
                maxLRU = LRU[index][i];
                lru = i;
            }
        }
        beingUsed[index][lru] = true;
        tags[index][lru] = tag;
        updateLRU(index, lru);

    }

    public void updateLRU(int index, int block){
        int value = LRU[index][block];

        //increase all of the blocks in the index
        for(int i = 0; i < assoc; i++){
            if(LRU[index][i] < value){
                LRU[index][i]++;
            }
        }

        //set the most recently used to 0
        LRU[index][block] = 0;

    }

    public float hitRate() {
        float accuracy = ((float)hits / intoCache) * 100;
        return accuracy;
    } 
}
