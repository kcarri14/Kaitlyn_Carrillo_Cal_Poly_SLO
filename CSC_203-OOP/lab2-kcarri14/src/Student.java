public class Student {
        private String name;
        private double grade;

        public Student() {}

        public Student(String name, double grade) {
           this.name = name;
           this.grade = grade;
        }
        public String getName(){
            return name;
        }
        public double getGrade(){
            return grade;
        }
        public char getLetterGrade(){
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
        @Override
        public String toString() {
            return name + " (" + String.format("%.2f", grade) + ")";
        }

        @Override
        public boolean equals(Object other) {
            if (other instanceof Student student) {
                return (name == null ? student.name == null : name.equals(student.name)) && student.grade == grade;
            }
            return false;
        }

        @Override
        public int hashCode() {
            double hash = 1;

            hash = hash * 31 + (name == null ? 0 : name.hashCode());
            hash = hash * 31 + grade;

            return (int) hash;
        }
    }

