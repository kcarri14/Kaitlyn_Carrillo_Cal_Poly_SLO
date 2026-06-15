import java.util.HashMap;


public abstract class Instruction {
    protected String name;

    public Instruction(String name) {
        this.name = name;
    }

    public abstract String toBinaryString();

    // create new Instruction subclass given instruction data
    public static Instruction newInstruction(String[] instData, HashMap<String, Integer> labelMap, int instAddress) {
        String name = instData[0];

        // create new Instruction of specific subclass
        switch (name) {
            // RTtypeInst
            case "and":
            case "or":
            case "add":
            case "slt":
            case "sub": {
                int rd = regToInt(instData[1]);
                int rs = regToInt(instData[2]);
                int rt = regToInt(instData[3]);
                return new RTypeInst(name, rs, rt, rd, 0);
            }
            case "sll": {
                int rd = regToInt(instData[1]);
                int rt = regToInt(instData[2]);
                int shamt = Integer.parseInt(instData[3]);
                return new RTypeInst(name, 0, rt, rd, shamt);
            }
            case "jr": {
                int rs = regToInt(instData[1]);
                return new RTypeInst(name, rs, 0, 0, 0);
            }
            // ITypeInst
            case "addi": {
                int rt = regToInt(instData[1]);
                int rs = regToInt(instData[2]);
                int imm = Integer.parseInt(instData[3]);
                return new ITypeInst(name, rs, rt, imm);
            }
            case "beq":
            case "bne": {
                int rs = regToInt(instData[1]);
                int rt = regToInt(instData[2]);
                String label = instData[3];
                int offset = labelMap.get(label) - (instAddress + 1);
                return new ITypeInst(name, rs, rt, offset);
            }
            case "lw":
            case "sw": {
                int rt = regToInt(instData[1]);
                int imm = Integer.parseInt(instData[2]);
                int rs = regToInt(instData[3]);
                return new ITypeInst(name, rs, rt, imm);
            }
            // JTypeInst
            case "j":
            case "jal": {
                String label = instData[1];
                int addr = labelMap.get(label);
                return new JTypeInst(name, addr);
            }
            // Unknown instruction
            default:
                throw new IllegalArgumentException("Invalid instruction: " + name);
        }
    }

    // helper method for converting register to int
    private static int regToInt(String reg) {
        switch (reg) {
            case "zero":
            case "0": return 0;
            case "v0": return 2;
            case "v1": return 3;
            case "a0": return 4;
            case "a1": return 5;
            case "a2": return 6;
            case "a3": return 7;
            case "t0": return 8;
            case "t1": return 9;
            case "t2": return 10;
            case "t3": return 11;
            case "t4": return 12;
            case "t5": return 13;
            case "t6": return 14;
            case "t7": return 15;
            case "s0": return 16;
            case "s1": return 17;
            case "s2": return 18;
            case "s3": return 19;
            case "s4": return 20;
            case "s5": return 21;
            case "s6": return 22;
            case "s7": return 23;
            case "t8": return 24;
            case "t9": return 25;
            case "sp": return 29;
            case "ra": return 31;
            default:
                throw new IllegalArgumentException("Invalid register: " + reg);
        }
    }

    // helper method for converting value to binary, padding to specified bit amount
    protected static String toBinary(int value, int bits) {
        // mask to ensure binary doesnt exceed bit num
        int mask = (1 << bits) - 1;
        String binary = Integer.toBinaryString(value & mask);
        return String.format("%" + bits + "s", binary).replace(' ', '0');
    }
}

class RTypeInst extends Instruction {
    private int rs, rt, rd, shamt, funct;

    public RTypeInst(String name, int rs, int rt, int rd, int shamt) {
        super(name);
        this.rs = rs;
        this.rt = rt;
        this.rd = rd;
        this.shamt = shamt;
        this.funct = getFunct(name);
    }

    // convert name to funct
    private int getFunct(String name) {
        switch (name) {
            case "add": return 32;
            case "sub": return 34;
            case "and": return 36;
            case "or": return 37;
            case "slt": return 42;
            case "sll": return 0;
            case "jr": return 8;
            default:
                throw new IllegalArgumentException("Invalid RType: " + name);
        }
    }

    // return binary string for full instruction
    public String toBinaryString() {
        return String.format("%s %s %s %s %s %s",
            Instruction.toBinary(0, 6), Instruction.toBinary(rs, 5),
            Instruction.toBinary(rt, 5), Instruction.toBinary(rd, 5),
            Instruction.toBinary(shamt, 5), Instruction.toBinary(funct, 6));
    }
}

class ITypeInst extends Instruction {
    private int rs, rt, imm, opcode;

    public ITypeInst(String name, int rs, int rt, int imm) {
        super(name);
        this.rs = rs;
        this.rt = rt;
        this.imm = imm;
        this.opcode = getOpcode(name);
    }

    // convert name to opcode
    private int getOpcode(String name) {
        switch (name) {
            case "addi": return 8;
            case "beq": return 4;
            case "bne": return 5;
            case "lw": return 35;
            case "sw": return 43;
            default:
                throw new IllegalArgumentException("Invalid IType: " + name);
        }
    }

    // return binary string for full instruction
    public String toBinaryString() {
        return String.format("%s %s %s %s",
            Instruction.toBinary(opcode, 6), Instruction.toBinary(rs, 5),
            Instruction.toBinary(rt, 5), Instruction.toBinary(imm, 16));
    }
}

class JTypeInst extends Instruction {
    private int address, opcode;

    public JTypeInst(String name, int address) {
        super(name);
        this.address = address;
        this.opcode = getOpcode(name);
    }

    // convert name to opcode
    private int getOpcode(String name) {
        switch (name) {
            case "j": return 2;
            case "jal": return 3;
            default:
                throw new IllegalArgumentException("Invalid JType: " + name);
        }
    }

    // return binary string for full instruction
    public String toBinaryString() {
        return String.format("%s %s",
            Instruction.toBinary(opcode, 6), Instruction.toBinary(address, 26));
    }
}
