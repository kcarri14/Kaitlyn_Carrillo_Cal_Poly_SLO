import java.util.Scanner;

public class countedones{
    public static void main(String[] args){
        Scanner input = new Scanner(System.in);
        char choice;
        System.out.println("Welcome to the CountOnes program.");
        do {
            System.out.println("Please enter a number: ");
            long number = input.nextLong();
            int count = countSetBits((int) number);
            System.out.println("The number of bits set is: " + count);
            System.out.println("Continue (y/n)?: ");
            choice = input.next().charAt(0);

        } while (choice == 'y' || choice == 'Y');
        System.out.println("Exiting");
        input.close();
    }
    public static int countSetBits(int number){
        int count = 0;
        while (!(number == 0)){
            count += (number & 1);
            number >>>= 1;
        }
        return count;
    }
}
