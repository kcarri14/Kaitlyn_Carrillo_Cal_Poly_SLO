import java.util.List;

import processing.core.PImage;
public class Well extends Actor{
    public static final String WELL_KEY = "well";

    public Well( Point position, List<PImage> images, double updatePeriod) {
        super( position, images, updatePeriod);
    }


    /** Well update logic. */
    public void executeUpdate(World world, ImageLibrary imageLibrary, EventScheduler eventScheduler) {
        setImageIndex(getImageIndex() + 1);
        scheduleUpdate(world, imageLibrary, eventScheduler);
    }



}
