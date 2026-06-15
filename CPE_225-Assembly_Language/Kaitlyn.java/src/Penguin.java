public class Penguin {
    public String name;

    public int age;
    public int height;

    public Penguin( String name, int age, int height){
        this.name = name;
        this.age = age;
        this.height = height;
    }
    @Override

    public boolean equals(Object other){
        return false;
    }

    public static void main(String[] args){
        Penguin NewPenguin = new Penguin("Bob", 3, 5);
    }

}
