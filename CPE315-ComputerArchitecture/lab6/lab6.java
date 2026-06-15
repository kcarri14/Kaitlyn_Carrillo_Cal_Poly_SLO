//Kaitlyn Carrillo and Kenton Rhoden

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class lab6 {
    public static void main(String[] args){
        //checks if file is in 
        if(args.length != 1){
            System.err.println("Error: No file provided");
            return;
        }

        //create a list of caches to go through
        ArrayList<cache> caches = new ArrayList<>();

        caches.add(new cache(2048, 1, 1));
        caches.add(new cache(2048, 1, 2));
        caches.add(new cache(2048, 1, 4));
        caches.add(new cache(2048, 2, 1));
        caches.add(new cache(2048, 4, 1));
        caches.add(new cache(2048, 4, 4));
        caches.add(new cache(4096, 1, 1));

        //read file
        try(Scanner reader = new Scanner(new File(args[0]))){
            while (reader.hasNextLine()) {
                String line = reader.nextLine();
                //splits the line by a space
                String[] parts = line.trim().split("\\s+");
                //gets the address and not the valid bit
                int address = Integer.parseUnsignedInt(parts[1], 16);

                //process each address in all of the caches
                for(cache ca : caches){
                    ca.access_addr(address);
                }
            }
        } catch (FileNotFoundException e) {
            System.err.println("No File Found");
            return;
        }
        //used for printing
        int cache_counter = 1;
        for(cache ca: caches){
            System.out.printf("Cache #%d\n", cache_counter);
            System.out.printf("Cache size: %dB \tAssociativity: %d \tBlock size: %d\n", ca.cacheSize, ca.assoc, ca.blockSize/4 );
            System.out.printf("Hits: %d \tHit Rate: %.2f%%\n", ca.hits, ca.hitRate());
            System.out.println("---------------------------\n");
            cache_counter++;
        }
    }
}

