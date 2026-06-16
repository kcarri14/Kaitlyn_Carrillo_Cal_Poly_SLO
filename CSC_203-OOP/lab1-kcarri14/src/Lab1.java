import java.util.ArrayList;
import java.util.List;

public class Lab1 {
    public static boolean contains(List<String> items, String desired) {
        for (String item : items) {
            if (item.equals(desired)){
                return true;
            }
        }
        return false;
    }
    public static void main(String[] args){
        int x = 3;
        double y = 4.0;
        int z = (int)Math.sqrt(Math.pow(x,2) + Math.pow(y,2));

        System.out.println("x: " + x);
        String formatted = String.format("y: %s", y);
        System.out.println(formatted);
        System.out.print("z: ");
        System.out.println(z);
        String a = "hello";
        char b = 'j';
        String c = a.replace('h', b);
        for (int i =0; i<c.length(); i++){
            System.out.print(c.charAt(i));
        }
        System.out.println();
        List<String> cats = new ArrayList<>();
        cats.add("Mochi");
        cats.add("Harvest");
        cats.remove(0);
        cats.add("Pearl");
        boolean has_mochi = contains(cats, "Mochi");
        if (!has_mochi) {
            System.out.println("Bye bye, Mochi! Farewell!");
        }

    }

}