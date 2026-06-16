/**
 * A partial linked list class. Modify as necessary.
 *
 * @author Vanessa Rivera
 */
public class BigNumber {

    BigNumberNode head;


    public BigNumber() {

        this.head = null;
    }

    // TODO: Write addition, multiplication, and exponentiation methods here or in another class
    public static BigNumber add(BigNumber a, BigNumber b){
                BigNumber result = new BigNumber();
                BigNumberNode currentA = a.head;
                BigNumberNode currentB = b.head;
                BigNumberNode currentResult = result.head;
                int carry = 0;
                while (currentA != null || currentB != null){
                    int dataA = (currentA != null) ? currentA.getData() : 0;
                    int dataB = (currentB != null) ? currentB.getData() : 0;
                    int sum = dataA + dataB + carry;
                    carry = sum / 10;

                    if (currentResult == null){
                        result.head = new BigNumberNode(sum % 10);
                        currentResult = result.head;
                    }else{
                        currentResult.setNext(new BigNumberNode(sum % 10));
                        currentResult = currentResult.getNext();
                    }
                    if (currentA != null) {
                        currentA = currentA.getNext();
                    }
                    if (currentB != null) {
                        currentB = currentB.getNext();
                    }

                }
                if (carry > 0){
                    currentResult.setNext(new BigNumberNode(carry));
                }

                return result;

        }

    public void addLeadingZero() {
        if (head == null) {
            head = new BigNumberNode(0);
            return;
        }


        BigNumberNode newHead = new BigNumberNode(0);
        newHead.setNext(head);
        head = newHead;
    }
    public static BigNumber multiply(BigNumber a, BigNumber b){
        BigNumber result = new BigNumber();
        BigNumberNode currentA = a.head;
        int position = 0;
        while (currentA != null){
            BigNumber resultTemp = new BigNumber();
            BigNumberNode resultTempCurrent = resultTemp.head;
            int carry = 0;
            int positionCarry = 0;
            BigNumberNode currentB = b.head;

            while (currentB != null || carry != 0 ){
                int dataA = (currentA != null) ? currentA.getData() : 0;
                int dataB = (currentB != null) ? currentB.getData() : 0;
                int product = dataA * dataB + carry;
                carry = product / 10;

                if (resultTempCurrent == null){
                    resultTemp.head = new BigNumberNode(product % 10);
                    resultTempCurrent = resultTemp.head;
                }else{
                    resultTempCurrent.setNext(new BigNumberNode(product % 10));
                    resultTempCurrent = resultTempCurrent.getNext();
                }
                if (currentB != null) {
                    currentB = currentB.getNext();
                }

                if (carry > 0 && currentB == null){
                    resultTempCurrent.setNext(new BigNumberNode(carry));
                }


            }
            for (int i = 0; i < position; i++) {
                resultTemp.addLeadingZero();
            }

            result = add(result, resultTemp);
            if (position == 0) {
                result = resultTemp;
            }

            currentA = currentA.getNext();
            position++;


        }

        return result;

    }
    public static BigNumber exponent(BigNumber a, int x){
        BigNumber result = new BigNumber();
        result.head = new BigNumberNode(1);
        while (x > 0) {
            if (x % 2 == 1) {
                result = multiply(result, a); // If last bit is set, multiply result by a
            }
            a = multiply(a, a); // Square a
            x /= 2; // Divide exponent by 2
        }

        return result;
    }
    public static BigNumber fromString(String string) {
        BigNumber number = new BigNumber();
        BigNumberNode current = null;
        for (int i = string.length() -1 ; i >= 0 ; i--){
            char digit = string.charAt(i);
            int digitValue = digit - '0';
            BigNumberNode newNode = new BigNumberNode(digitValue);

            if (current == null){
                number.head = newNode;
                current = number.head;
            } else{
                current.setNext(newNode);
                current = newNode;
            }

        }
        // TODO: Use the string to create your BigNumber here (Hint: use iteration or recursion)

        return number;
    }

    @Override
    public String toString() {
        String string = "";
        BigNumberNode current = head;
        while (current != null){
            string = current.getData() + string;
            current = current.getNext();
        }
        return string;
    }
}
