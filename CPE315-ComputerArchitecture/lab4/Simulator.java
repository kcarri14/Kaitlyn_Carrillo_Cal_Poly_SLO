
import java.util.List;

public class Simulator {
    String ifid;
    String idexe;
    String exemem;
    String memwb;
    Instruction ifid_inst;
    Instruction idexe_inst;
    int cycles;
    int instcomp;
    int stall;
    int stall_b;
    int stall_j;


    public Simulator() {
        ifid = "empty";
        idexe = "empty";
        exemem = "empty";
        memwb = "empty";
        cycles = 0;
        instcomp = 0;
        stall = 0;
    }

    public void stepCycles(Emulator emulator, int snum, List<Instruction> instList){
        for(int i = 0; i < snum; i++){
            cycles++;
            if (memwb != "empty" && !memwb.equals("stall") && !memwb.equals("squash")) {
                instcomp++;
            }

            if(stall > 0){
                memwb = exemem;
                exemem = idexe;
                idexe = "stall";
                stall--;
                continue;
            }
            if(stall_j > 0){
                memwb = exemem;
                exemem = idexe;
                idexe = ifid;
                ifid = "squash";
                stall_j--;
                continue;
            }
            if(stall_b > 0){
                if (memwb.equals("beq") || memwb.equals("bne") ){
                    exemem = "squash";
                    idexe = "squash";
                    ifid = "squash";
                    stall_b--;
                    continue;
                }
                
            }
            memwb = exemem;
            exemem = idexe;
            idexe = ifid;
            idexe_inst = ifid_inst;

            Instruction get = processNewInst(instList, emulator);

            if (hasLoadUse(idexe_inst, get)) {
                stall = Math.max(stall, 1);
            }

            if (isUnconditionalJump(get)) {
                stall_j = Math.max(stall_j, 1);
            }

            if (isTakenBranch(get, emulator)) {
                //System.out.println(isTakenBranch(get, emulator));
                stall_b = Math.max(stall_b, 1);
            }
            //System.out.println(get);
            if (get == null) {
                ifid = "empty";
                ifid_inst = null;
            } else {
                ifid = get.name;
                ifid_inst = get;
            }
        }
    }
   

    public boolean isProgComp(Emulator emulator, List<Instruction> instList){
        return emulator.prog_counter >= instList.size() && ifid == "empty" && idexe == "empty" && exemem == "empty" && memwb == "empty";
    }

    public void p_inst(Emulator emulator){
        System.out.println();
        System.out.println("pc\tif/id\tid/exe\texe/mem\tmem/wb");
        System.out.println(emulator.prog_counter + "\t"  + ifid + "\t" + idexe + "\t" + exemem + "\t" + memwb);
        System.out.println();
    }
    public void s_inst(Emulator emulator, int numLines, List<Instruction> instList){
        
        stepCycles(emulator, numLines, instList);
        p_inst(emulator);
    }
    public void r_inst(Emulator emulator, List<Instruction> instList){
        while (!isProgComp(emulator, instList)) {
            stepCycles(emulator, 1, instList);
        }
        double cpi = (double) cycles/ instcomp;
        System.out.println();
        System.out.println("Program complete");
        System.out.printf("CPI = %.3f\t\tCycles = %d\t\tInstructions = %d\n", cpi, cycles, instcomp);
        System.out.println();
    }

    public boolean isTakenBranch(Instruction inst, Emulator emulator) {
        if (inst == null) {
            return false;
        }

        if (inst.name.equals("beq")) {
            ITypeInst branch = (ITypeInst) inst;
            // System.out.println(Emulator.regs.get(branch.rs));
            // System.out.println(Emulator.regs.get(branch.rt));
            return Emulator.regs.get(branch.rs).equals(Emulator.regs.get(branch.rt));
        }

        if (inst.name.equals("bne")) {
            ITypeInst branch = (ITypeInst) inst;
            return !Emulator.regs.get(branch.rs).equals(Emulator.regs.get(branch.rt));
        }

        return false;
    }

    public boolean isUnconditionalJump(Instruction inst){
        if (inst == null) {
            return false;
        }
        if(inst.name.equals("j") ||inst.name.equals("jal") || inst.name.equals("jr") ){
            return true;
        }else{
            return false;
        }
    }

    public boolean hasLoadUse(Instruction prev, Instruction curr){
        if (prev == null || curr == null) {
            return false;
        }
        if (!prev.name.equals("lw")) {
            return false;
        }
    
        ITypeInst lw = (ITypeInst) prev;
        int loadedRegister = lw.rt;

        if (loadedRegister == 0) {
            return false;
        }

        switch (curr.name) {
            case "add":
            case "sub":
            case "and":
            case "or":
            case "slt": {
                RTypeInst r = (RTypeInst) curr;
                return r.rs == loadedRegister || r.rt == loadedRegister;
            }

            case "sll": {
                RTypeInst r = (RTypeInst) curr;
                return r.rs == loadedRegister;
            }

            case "jr": {
                RTypeInst r = (RTypeInst) curr;
                return r.rs == loadedRegister;
            }

            case "addi":
            case "lw": {
                ITypeInst i = (ITypeInst) curr;
                return i.rs == loadedRegister;
            }

            case "sw":
            case "beq":
            case "bne": {
                ITypeInst i = (ITypeInst) curr;
                return i.rs == loadedRegister || i.rt == loadedRegister;
            }

            default:
                return false;
        }
    }




    public Instruction processNewInst(List<Instruction> instList, Emulator emulator){
        if (emulator.prog_counter >= instList.size()) {
            return null;
        }
        Instruction inst = instList.get(emulator.prog_counter);
        emulator.processInst(instList);
        return inst;
    }
//     Tracks pipeline registers
//   - Tracks cycles
//   - Tracks completed instructions
//   - Handles p, s, r behavior
//   - Adds branch/jump/load-use timing delays
}
