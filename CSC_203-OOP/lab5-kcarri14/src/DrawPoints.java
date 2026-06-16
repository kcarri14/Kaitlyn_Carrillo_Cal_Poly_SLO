import processing.core.*;

import java.io.File;
import java.io.FileNotFoundException;
import java.nio.file.Paths;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Stream;

public class DrawPoints extends PApplet {

	String s;

	public void settings() {
    	size(500, 500);
		s = Paths.get("").toAbsolutePath().getFileName().toString();
	}
  
	public void setup() {
    	background(128);
    	noLoop();
  	}

  	public void draw() {
		// You should create a stream of Points using either a list or stream builder.
		// TODO: Initialize either a stream builder or list here
		Stream.Builder<Point> builder = Stream.builder();
		try (Scanner scanner = new Scanner(new File("positions.txt"))) {
			while (scanner.hasNextLine()) {
				String line = scanner.nextLine();

				// Each line contains comma and space separated x, y, and z values
				// You will add a Point to the stream builder/list for each line
				// TODO: Process the line as a string here
				String[] coordinates = line.split("\\s+");
				 if (coordinates.length == 3){
					 double x = Double.parseDouble(coordinates[0].replaceAll(",", ""));
					 double y = Double.parseDouble(coordinates[1].replaceAll(",", ""));
					 double z = Double.parseDouble(coordinates[2].replaceAll(",", ""));
					 builder.accept(new Point(x,y,z));
				 }
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}

		// Initialize the stream
		// TODO: Create the stream here using the builder/list
		Stream<Point> pointStream = builder.build();

		// Process the stream
		List<Point> pointList = pointStream
		// TODO: Add additional operations here to transform the points
				.filter(point -> point.z <= 2.0)
				.map(point -> new Point((point.x *0.5)-150, ((point.y * 0.5) - 562) * -1, point.z *0.5))
				.toList();

		// Display the stream
		for (Point p : pointList){
			ellipse((int) p.x, (int) p.y, 1, 1);
			fill(126, 126, 126);
			text(s, 0, 500);
		}
  	}

  	public static void main(String[] args) {
      PApplet.main("DrawPoints");
   }
}
