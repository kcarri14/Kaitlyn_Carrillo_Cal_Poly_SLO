import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

/**
 * Contains file processing behavior for the project.
 * You will modify only the following methods:
 * - parseLineUsingLittleNumber()
 * - parseLineUsingBigNumber()
 * You do not need to run this class directly.
 *
 * @author Vanessa Rivera
 */
public class FileProcessor {
    /**
     * Automatically called multiple times when parsing an input text file, once for each line.
     * The included tests control whether the LittleNumber or BigNumber version is used.
     *
     * @param line The line from the input file, including any newline characters
     */
    public static void parseLineUsingLittleNumber(String line) {

            String[] parsed_line = line.split("\\s+");

            if (parsed_line.length != 3) {
                return;
            }

            LittleNumber number1 = LittleNumber.fromString(parsed_line[0]);
            LittleNumber number2 = LittleNumber.fromString(parsed_line[2]);

            String operator = parsed_line[1];
            if (operator.equals("+")){
                LittleNumber add1 = LittleNumber.add(number1, number2);
                System.out.println(number1 + " " + operator + " " + number2 + " " + "= " + add1);
            } else if (operator.equals("*")){
                LittleNumber multiply1 = LittleNumber.multiply(number1, number2);
                System.out.println(number1 + " " + operator + " " + number2 + " " + "= " + multiply1);
            }else{
                LittleNumber expon1 = LittleNumber.exponentiate(number1, Integer.parseInt(parsed_line[2]));
                System.out.println(number1 + " " + operator + " " + number2 + " " + "= " + expon1);

            }

    }

    /**
     * Automatically called multiple times when parsing an input text file, once for each line.
     * The included tests control whether the LittleNumber or BigNumber version is used.
     *
     * @param line The line from the input file, including any newline characters
     */
    public static void parseLineUsingBigNumber(String line) {
        String[] parsed_line = line.split("\\s+");

        if (parsed_line.length != 3) {
            return;
        }

        BigNumber number1 = BigNumber.fromString(parsed_line[0]);
        BigNumber number2 = BigNumber.fromString(parsed_line[2]);

        String operator = parsed_line[1];
        if (operator.equals("+")){

            BigNumber add1 = BigNumber.add(number1, number2);
            System.out.println(number1 + " " + operator + " " + number2 + " " + "= " + add1);
        } else if (operator.equals("*")){

            BigNumber multiply1 = BigNumber.multiply(number1, number2);
            System.out.println(number1 + " " + operator + " " + number2 + " " + "= " + multiply1);
        }else{

            BigNumber expon1 = BigNumber.exponent(number1, Integer.parseInt(parsed_line[2]));
            System.out.println(number1 + " " + operator + " " + number2 + " " + "= " + expon1);

        }
    }

    /**
     * Called by the included test file. You do not need to run this method directly.
     * <strong>Do not</strong> modify this method.
     *
     * @param args Command-line arguments
     *             0: The input file path. (Required)
     *             1: Option to use "little" or "big" number parsing. (Required)
     */
    public static void main(String[] args) {
        try (BufferedReader reader = new BufferedReader(new FileReader(args[0]))) {
            String line;
            try {
                while ((line = reader.readLine()) != null) {
                    switch (args[1]) {
                        case "little":
                            parseLineUsingLittleNumber(line);
                            break;
                        case "big":
                            parseLineUsingBigNumber(line);
                            break;
                        default:
                            throw new IllegalArgumentException(String.format("Option %s is invalid, must be 'little' or 'big'.%n", args[1]));
                    }
                }
            } catch (NumberFormatException | ArrayIndexOutOfBoundsException e) {
                e.printStackTrace();
            }
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.printf("Expected 2 command-line arguments, got %d.%n", args.length);
        } catch (IOException e) {
            System.out.printf("Failed to read file %s.%n", args[0]);
        } catch (IllegalArgumentException e) {
            e.printStackTrace();
        }
    }
}
