import org.junit.jupiter.api.Test;
import  org.junit.jupiter.api.Assertions;
/**
 * An empty class for unit tests of your new classes.
 */
public class BigNumberTests {
    @Test
    public void testAdd() {
        BigNumber a = BigNumber.fromString("123");
        BigNumber b = BigNumber.fromString("456");
        BigNumber expectedSum1 = BigNumber.fromString("579");
        Assertions.assertEquals(expectedSum1.toString(), BigNumber.add(a, b).toString());

    }
    @Test
    public void testAdd2(){
        BigNumber c = BigNumber.fromString("999");
        BigNumber d = BigNumber.fromString("189");
        BigNumber expectedSum2 = BigNumber.fromString("1188");
        Assertions.assertEquals(expectedSum2.toString(), BigNumber.add(c, d).toString());
    }
    @Test
    public void testAdd3(){
        BigNumber c = BigNumber.fromString("983453457");
        BigNumber d = BigNumber.fromString("654345");
        BigNumber expectedSum2 = BigNumber.fromString("984107802");
        Assertions.assertEquals(expectedSum2.toString(), BigNumber.add(c, d).toString());
    }


    @Test
    public void testMultiply() {
        BigNumber a = BigNumber.fromString("983453457");
        BigNumber b = BigNumber.fromString("654345");
        BigNumber expectedProduct1 = BigNumber.fromString("643517852320665");
        Assertions.assertEquals(expectedProduct1.toString(), BigNumber.multiply(a, b).toString());
    }
    @Test
    public void testMultiplyWithNullResultTempCurrent() {
        BigNumber a = BigNumber.fromString("2");
        BigNumber b = BigNumber.fromString("3");
        b.head = null;
        BigNumber result = BigNumber.multiply(a, b);
        BigNumber expected = BigNumber.fromString("");
        Assertions.assertEquals(expected.toString(), result.toString());
    }

    @Test
    public void testExponent() {

        BigNumber base1 = BigNumber.fromString("2");
        int exponent1 = 10;
        BigNumber expectedExponentiation1 = BigNumber.fromString("1024");
        Assertions.assertEquals(expectedExponentiation1.toString(), BigNumber.exponent(base1, exponent1).toString());

    }
    @Test
    public void testexpon(){
        BigNumber base2 = BigNumber.fromString("5");
        int exponent2 = 0;
        BigNumber expectedExponentiation2 = BigNumber.fromString("1");
        Assertions.assertEquals(expectedExponentiation2.toString(), BigNumber.exponent(base2, exponent2).toString());
    }

    @Test
    public void testFromString() {
        String str1 = "123456789";
        BigNumber expectedNumber1 = BigNumber.fromString("123456789");
        Assertions.assertEquals(expectedNumber1.toString(), BigNumber.fromString(str1).toString());

        String str2 = "000987654321";
        BigNumber expectedNumber2 = BigNumber.fromString("000987654321");
        Assertions.assertEquals(expectedNumber2.toString(), BigNumber.fromString(str2).toString());
    }

    @Test
    public void testAddLeadingZeroToEmptyList() {
        BigNumber number = new BigNumber();
        number.addLeadingZero();
        Assertions.assertEquals(0, number.head.getData());
        Assertions.assertNull(number.head.getNext());
    }

    @Test
    public void testAddLeadingZeroToNonEmptyList() {
        BigNumber number = new BigNumber();
        number.head = new BigNumberNode(5);
        number.head.setNext(new BigNumberNode(3));
        number.addLeadingZero();
        Assertions.assertEquals(0, number.head.getData());
        Assertions.assertEquals(5, number.head.getNext().getData());
        Assertions.assertEquals(3, number.head.getNext().getNext().getData());
    }


}
