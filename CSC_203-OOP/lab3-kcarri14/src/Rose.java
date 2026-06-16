import processing.core.PImage;

import java.util.List;

public class Rose implements Actor, Waterable{
    public static final String ROSE_KEY = "rose";
    public static final double ROSE_TO_NYMPH_UPDATE_PERIOD = 0.125;
    public static final int ROSE_WATER_LIMIT = 9;
    private Point position;

    private List<PImage> images;

    private int imageIndex;

    private double updatePeriod;

    private int water;
    public Rose(Point position, List<PImage> images, double updatePeriod) {
    }
    public void scheduleUpdate(World world, ImageLibrary imageLibrary, EventScheduler eventScheduler) {
        eventScheduler.scheduleEvent(this, new Update(this, world, imageLibrary), updatePeriod);
    }

    public void executeUpdate(World world, ImageLibrary imageLibrary, EventScheduler eventScheduler) {
        imageIndex = images.size() * water / ROSE_WATER_LIMIT;
        if (water >= ROSE_WATER_LIMIT) {
            Nymph nymph = new Nymph(position, imageLibrary.get(Nymph.NYMPH_KEY), ROSE_TO_NYMPH_UPDATE_PERIOD);

            world.removeEntity(eventScheduler, this);
            world.addEntity(nymph);
            nymph.scheduleUpdate(world, imageLibrary, eventScheduler);
        } else {
            scheduleUpdate(world, imageLibrary, eventScheduler);
        }
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
    public int getWater(){
        return water;
    }
    public void setWater(int water){
        this.water = water;
    }
}