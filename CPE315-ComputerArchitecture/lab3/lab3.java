import java.util.ArrayList;
import java.util.List;

//Kaitlyn Carrillo and Kenton Rhoden

import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;


//takes in the input from the command line and gives it to the Assembler
public class lab3 {
    public static void main(String[] args) {
        // get lines from file
        if (args.length == 0){
            System.err.println("Error: No file provided");
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
            return;
        }

        //computes first and second pass of Assembler
        Assembler assembler = new Assembler();
        List<String> cleanedStrings = assembler.firstPass(AllStrings);
        List<Instruction> instList = assembler.secondPass(cleanedStrings);
        

        // create emulator
        Emulator emulator = new Emulator();
        
        if (args.length == 1){
            //interactive mode
            Scanner input = new Scanner(System.in);
            //continues running until q command is given
            while(true){
                // read user input
                System.out.print("mips> ");
                String command =  input.nextLine();
                if (command.equals("q")) {
                    break;
                }

                processCommand(emulator, command, instList);
            }
            input.close();

        }

        if (args.length == 2) {
            //script mode
            //goes through lines in file and adds them to List
            try(Scanner reader = new Scanner(new File(args[1]))){
                // runs until no lines or `q` is read
                while (reader.hasNextLine()) {
                    // read line
                    String command = reader.nextLine();
                    System.out.println("mips> " + command);
                    if (command.equals("q")) {
                        break;
                    }

                    processCommand(emulator, command, instList);
                }
            } catch (FileNotFoundException e) {
                System.err.println("No File Found");
                return;
            }
        }

        if (args.length > 2) {
            System.err.printf("Error: expected < 3 arguments, received `%d`\n", args.length);
            return;
        }
    }

    private static void processCommand(Emulator emulator, String command, List<Instruction> instList) {
        if(command.equals("h")){
            emulator.h_inst();
        }else if(command.equals("c")){
            emulator.c_inst();
        }
        else if(command.equals("d")){
            emulator.d_inst();
        }
        else if(command.startsWith("s")){
            if(command.equals("s")){
                emulator.s_inst(1, instList);
            }else{
                emulator.s_inst(Integer.parseInt(command.split(" ")[1]), instList);
            }
        }
        else if(command.equals("r")){
            emulator.r_inst(instList.size(), instList);
        }
        else if(command.startsWith("m")){
            emulator.m_inst(command);
        }
        else {
            System.err.printf("Unknown command %s\n", command);
        }
    }
}
