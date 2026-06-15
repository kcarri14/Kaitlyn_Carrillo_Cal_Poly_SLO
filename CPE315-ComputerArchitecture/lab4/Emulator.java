
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Emulator {
    int[] data_memory  = new int[8192];
    int prog_counter = 0; 
    public static Map<Integer, Integer> regs = new HashMap<>();
        
    static {
        regs.put(0, 0);
        regs.put(2, 0);
        regs.put(3, 0);
        regs.put(4, 0);
        regs.put(5, 0);
        regs.put(6, 0);
        regs.put(7, 0);
        regs.put(8, 0);
        regs.put(9, 0);
        regs.put(10, 0);
        regs.put(11, 0);
        regs.put(12, 0);
        regs.put(13, 0);
        regs.put(14, 0);
        regs.put(15, 0);
        regs.put(16, 0);
        regs.put(17, 0);
        regs.put(18, 0);
        regs.put(19, 0);
        regs.put(20, 0);
        regs.put(21, 0);
        regs.put(22, 0);
        regs.put(23, 0);
        regs.put(24, 0);
        regs.put(25, 0);
        regs.put(29, 0);
        regs.put(31, 0);
    }
        

    public void h_inst() {
        System.out.println();
        System.out.println("h = show help");
        System.out.println("d = dump register state");
        System.out.println("p = show pipeline registers");
        System.out.println("s = single step through the program (i.e. simulates 1 cycle and stop)");
        System.out.println("s num = step through num clock cycles");
        System.out.println("r = run until the program ends");
        System.out.println("m num1 num2 = display data memory from location num1 to num2");
        System.out.println("c = clear all registers, memory, and the program counter to 0");
        System.out.println("q = exit the program");
        System.out.println();
    }
    public void s_inst(int numLines, List<Instruction> instList) {
        // iterate through each instruction starting from pc
        for (int i = 0; i < numLines; i++) {
            if (prog_counter >= instList.size()) {
                System.err.printf("Error: pc out of bounds! (pc = %d)\n", prog_counter);
                return;
            }
            processInst(instList);
        }

        //System.out.println("\t  " + numLines + " instruction(s) executed");
    }
    public void r_inst(int numLines, List<Instruction> instList) {
        while (prog_counter < instList.size()) {
            processInst(instList);
        }
        System.out.println();
    }
    public void c_inst(){
        //reset the hashmap and program counter to all 0's 
        prog_counter = 0;
        for(Map.Entry<Integer, Integer> entry : regs.entrySet()){
            entry.setValue(0);
        }
        //reset the memory
        data_memory  = new int[8192];

        System.out.println("\tSimulator reset\n");
    }
    public void d_inst(){
        //display the register state
        System.out.println("\npc = " + prog_counter);
        int counter = 1;
        for(Map.Entry<Integer, Integer> entry : regs.entrySet()){
            String regName = "$" + Instruction.intToReg(entry.getKey());
            System.out.printf("%-3s = %-10d", regName, entry.getValue());
            if (counter % 4 == 0) {
                System.out.println();
            }
            counter++;
        }
        System.out.println("\n");

    }
    public void m_inst(String fileLine){
        // display data memory from locations 
        //split line into m, num1, and num2
        String[] parsedLine = fileLine.split(" ");
        int start = Integer.parseInt(parsedLine[1]);
        int finished = Integer.parseInt(parsedLine[2]);
        //find how many lines of data needed
        int total = finished - start;
        //go through the array and print all data needed
        System.out.println();
        for(int i = 0; i < total + 1; i++){
            int array_data = start + i;
            int memory_value = data_memory[array_data];
            System.out.println("[" + array_data + "] = " + memory_value);
        }
        System.out.println();

    }

    void processInst(List<Instruction> instList) {
        // System.out.println("pc: " + prog_counter);
        Instruction inst = instList.get(prog_counter);
        // System.out.println("inst: " + inst.name);
        switch(inst.name) {
            case "and": {
                RTypeInst RInst = (RTypeInst) inst;

                int result = regs.get(RInst.rs) & regs.get(RInst.rt);
                regs.put(RInst.rd, result);

                prog_counter++;
                break;
            }
            case "or": {
                RTypeInst RInst = (RTypeInst) inst;

                int result = regs.get(RInst.rs) | regs.get(RInst.rt);
                regs.put(RInst.rd, result);

                prog_counter++;
                break;
            }
            case "add": {
                RTypeInst RInst = (RTypeInst) inst;

                int result = regs.get(RInst.rs) + regs.get(RInst.rt);
                regs.put(RInst.rd, result);

                prog_counter++;
                break;
            }
            case "slt": {
                RTypeInst RInst = (RTypeInst) inst;

                int result = ((regs.get(RInst.rs) < regs.get(RInst.rt)) ? 1 : 0);
                regs.put(RInst.rd, result);

                prog_counter++;
                break;
            }
            case "sub": {
                RTypeInst RInst = (RTypeInst) inst;

                int result = regs.get(RInst.rs) - regs.get(RInst.rt);
                regs.put(RInst.rd, result);

                prog_counter++;
                break;
            }
            case "sll": {
                RTypeInst RInst = (RTypeInst) inst;

                int result = regs.get(RInst.rs) << regs.get(RInst.rt);
                regs.put(RInst.rd, result);

                prog_counter++;
                break;
            }
            case "jr": {
                RTypeInst RInst = (RTypeInst) inst;

                prog_counter = regs.get(RInst.rs);

                break;
            }
            case "addi": {
                ITypeInst IInst = (ITypeInst) inst;

                int result = regs.get(IInst.rs) + IInst.imm;
                regs.put(IInst.rt, result);

                prog_counter++;
                break;
            }
            case "beq": {
                ITypeInst IInst = (ITypeInst) inst;

                Boolean result = regs.get(IInst.rs) == regs.get(IInst.rt);
                if (result) {
                    prog_counter += 1 + IInst.imm;
                } else {
                    prog_counter++;
                }

                break;
            }
            case "bne": {
                ITypeInst IInst = (ITypeInst) inst;

                Boolean result = regs.get(IInst.rs) != regs.get(IInst.rt);
                if (result) {
                    prog_counter += 1 + IInst.imm;
                } else {
                    prog_counter++;
                }

                break;
            }
            case "lw": {
                ITypeInst IInst = (ITypeInst) inst;

                int addr = IInst.imm + regs.get(IInst.rs);
                regs.put(IInst.rt, data_memory[addr]);

                prog_counter++;
                break;
            }
            case "sw": {
                ITypeInst IInst = (ITypeInst) inst;

                int addr = IInst.imm + regs.get(IInst.rs);
                data_memory[addr] = regs.get(IInst.rt);

                prog_counter++;
                break;
            }
            case "j": {
                JTypeInst JInst = (JTypeInst) inst;

                prog_counter = JInst.address;

                break;
            }
            case "jal": {
                JTypeInst JInst = (JTypeInst) inst;

                regs.put(31, prog_counter + 1);
                prog_counter = JInst.address;

                break;
            }
            default:
            throw new IllegalArgumentException("Unknown instruction: " + inst.name);
        }
    }
}
