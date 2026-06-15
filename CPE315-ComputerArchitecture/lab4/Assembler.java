
import java.util.List;
import java.util.ArrayList;
import java.util.HashMap;

public class Assembler {
    private List<Instruction> instructions = new ArrayList<>();
    private HashMap<String, Integer> labelMap = new HashMap<>();

    // runs through all lines in file to compute address of each label, returns list of just instruction strings
    public List<String> firstPass(List<String> fileLines) {
        int currAddress = 0;
        List<String> instructionLines = new ArrayList<>();
        for (String line : fileLines) {
            line = line.trim();

            // remove comment
            int commentIndex = line.indexOf('#');
            if (commentIndex != -1) {
                line = line.substring(0, commentIndex);
            }

            // handle label
            if (line.contains(":")) {
                String[] parts = line.split(":", 2);
                String label = parts[0].trim();
                labelMap.put(label, currAddress);
                // if label does not have instruction, dont increment address
                if (parts[1].trim().isEmpty()) {
                    continue;
                } else {
                    line = parts[1];
                }
            }

            // skip empty lines
            line = line.trim();
            if (line.isEmpty()) {
                continue;
            }

            // line is purely instruction
            instructionLines.add(line);
            currAddress++;
        }
        return instructionLines;
    }

    // runs through list of instruction strings and add to list of Instruction types
    // assumes lines are already trimmmed and each line has an instruction
    public List<Instruction> secondPass(List<String> instructionLines) {
        int currAddress = 0;
        for (String line : instructionLines) {
            //parses line 
            String[] parsedLine = line.split("[,$()\\s]+");

            Instruction instruction;
            try {
                //makes the line into an instruction 
                instruction = Instruction.newInstruction(parsedLine, labelMap, currAddress);
            } catch (IllegalArgumentException exception) {
                System.out.println("Invalid instruction: " + parsedLine[0]);
                return instructions;
            }
            
            instructions.add(instruction);
            currAddress++;
        }
        return instructions;
    }
}
