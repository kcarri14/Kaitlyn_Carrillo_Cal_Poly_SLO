import java.util.Scanner;

public class leadingZeros {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        char choice;
        System.out.println("Welcome to the Zeros program.");
        do {
            System.out.println("Please enter a number: ");
            int number = input.nextInt();
            int count = countLeadingZeros(number);
            System.out.println("The number of bits set is: " + count);
            System.out.println("Continue (y/n)?: ");
            choice = input.next().charAt(0);

        } while (choice == 'y' || choice == 'Y');
        System.out.println("Exiting");
        input.close();
    }

    public static int countLeadingZeros(int number) {
        int count = 0;
        int mask = 0x80000000; // Most significant bit mask
        while ((number & mask) == 0 && mask != 0) {
            count++;
            mask >>>= 1;
        }
        return count;
    }
}