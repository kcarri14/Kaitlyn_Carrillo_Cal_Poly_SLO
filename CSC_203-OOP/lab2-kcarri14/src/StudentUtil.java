import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class StudentUtil {
    public static char getLetterGrade(Student student){
        double grade = student.getGrade();
        if (grade >= 90) {
            return 'A';
        }
        else if (grade >= 80) {
            return 'B';
        }
        else if (grade >= 70) {
            return 'C';
        }
        else if (grade >= 60){
            return 'D';
        }
        else{
            return 'F';
        }
    }


}


