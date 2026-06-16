import processing.core.PImage;

import java.util.List;
import java.util.Random;

public class Nymph implements Actor, Repositionable{
    public static final String NYMPH_KEY = "nymph";
    private Point position;
    private List<PImage> images;

    private int imageIndex;

    private double updatePeriod;
    public Nymph(Point position, List<PImage> images, double updatePeriod) {
    }
    public void scheduleUpdate(World world, ImageLibrary imageLibrary, EventScheduler eventScheduler) {
        eventScheduler.scheduleEvent(this, new Update(this, world, imageLibrary), updatePeriod);
    }

    public void reposition(World world, EventScheduler eventScheduler) {
        int nextX = position.x;
        int nextY = position.y;

        Random rand = new Random();
        if (rand.nextDouble() < 0.25) {
            if (rand.nextDouble() < 0.50) {
                if (rand.nextDouble() < 0.50) {
                    nextX += 1;
                } else {
                    nextX -= 1;
                }
            } else {
                if (rand.nextDouble() < 0.50) {
                    nextY += 1;
                } else {
                    nextY -= 1;
                }
            }
        }

        Point destination = new Point(nextX, nextY);
        if (world.inBounds(destination) && !world.isOccupied(destination)) {
            world.moveEntity(eventScheduler, this, destination);
        }
    }
    public void executeUpdate(World world, ImageLibrary imageLibrary, EventScheduler eventScheduler) {
        imageIndex += 1;
        reposition(world, eventScheduler);
        scheduleUpdate(world, imageLibrary, eventScheduler);
    }

    public int getImageIndex() {
        return imageIndex;
    }

    public List<PImage> getImages() {
        return images;
    }

    public Point getPosition() {
        return position;
    }

    public void setPosition(Point position) {
        this.position = position;
    }
}