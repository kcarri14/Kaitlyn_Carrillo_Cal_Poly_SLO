import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class StudentTests {

    @Test
    public void testConstructorNoParameters(){
        Student student = new Student();
        Assertions.assertNull(student.getName());
        Assertions.assertEquals(0.0, student.getGrade());
    }
    @Test
    public void testStudentMethod(){
        String expectedName = "Grace";
        double expectedGrade = 98.45;
        Student student = new Student(expectedName, expectedGrade);
        Assertions.assertEquals(expectedName, student.getName());
        Assertions.assertEquals(expectedGrade, student.getGrade());
    }

    @Test
    public void testConstructorsandGetters(){
        Student student = new Student("Kaitlyn", 95.5);
        Assertions.assertEquals("Kaitlyn", student.getName());
        Assertions.assertEquals(95.5, student.getGrade());

    }
    @Test
    public void testGetLetterGradeA(){
        Student student = new Student("Kaveh", 100);
        Assertions.assertEquals('A', student.getLetterGrade());
    }
    @Test
    public void testGetLetterGradeB(){
        Student student = new Student("Annie", 89.9);
        Assertions.assertEquals('B', student.getLetterGrade());
    }
    @Test
    public void testGetLetterGradeC(){
        Student student = new Student("Trevor", 70.01);
        Assertions.assertEquals('C', student.getLetterGrade());
    }
    @Test
    public void testGetLetterGradeD(){
        Student student = new Student("Audrey", 65.934);
        Assertions.assertEquals('D', student.getLetterGrade());
    }
    @Test
    public void testGetLetterGradeF(){
        Student student = new Student("Gigi", 5.9);
        Assertions.assertEquals('F', student.getLetterGrade());
    }
    @Test
    public void testToString(){
        Student student = new Student("Diego", 45.995);
        Assertions.assertEquals("Diego (46.00)", student.toString());
    }
    @Test
    public void testEqualsAndHashCode() {
        Student student1 = new Student("Professor Rivera", 100);
        Student student2 = new Student("Professor Rivera", 100);
        Assertions.assertTrue(student1.equals(student2));
        Assertions.assertEquals(student1.hashCode(), student2.hashCode());


    }
    @Test
    public void testHashCode(){
        Student student1 = new Student("Karina", 80);
        String student2 = "Dominc";
        Assertions.assertNotEquals(student1.hashCode(), student2.hashCode());
        Assertions.assertFalse(student1.equals(student2));
    }
    @Test
    public void teststaticGetLetterGradeA() {

        Student student = new Student("Vincent", 97.0);
        Assertions.assertEquals('A', StudentUtil.getLetterGrade(student));
    }
    @Test
    public void teststaticGetLetterGradeB() {

        Student student = new Student("Jimmie", 85.02);
        Assertions.assertEquals('B', StudentUtil.getLetterGrade(student));
    }
    @Test
    public void teststaticGetLetterGradeC() {

        Student student = new Student("Noah", 79.9);
        Assertions.assertEquals('C', StudentUtil.getLetterGrade(student));
    }
    @Test
    public void teststaticGetLetterGradeD() {

        Student student = new Student("Alex", 65.9);
        Assertions.assertEquals('D', StudentUtil.getLetterGrade(student));
    }
    @Test
    public void teststaticGetLetterGradeF() {

        Student student = new Student("Bee", 15.2);
        Assertions.assertEquals('F', StudentUtil.getLetterGrade(student));
    }

}
