//Kaitlyn Carrillo and Kenton Rhoden
// Support following instructions: and, or, add, addi, sll, sub, slt, beq, bne, lw, sw, j, jr, jal

import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;
import java.util.ArrayList;


public class lab2 {
    public static void main(String[] args) {
        // get lines from file
        if (args.length == 0){
            System.out.println("Error: No file provided");
            return;
        }
        List<String> AllStrings = new ArrayList<>();
        //goes through lines in file and adds them to List
        try(Scanner reader = new Scanner(new File(args[0]))){
            while (reader.hasNextLine()) {
                String line = reader.nextLine();
                AllStrings.add(line);
            }
        } catch (FileNotFoundException e) {
            System.err.println("No File Found");
        }
        //computes first and second pass of Assembler
        Assembler assembler = new Assembler();
        List<String> cleanedStrings = assembler.firstPass(AllStrings);
        assembler.secondPass(cleanedStrings);
    }
}



