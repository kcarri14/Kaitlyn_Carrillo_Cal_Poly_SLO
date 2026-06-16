import java.util.*;
import processing.core.PImage;

/** Represents an actor that exists in the virtual world. */
public abstract class Actor {

    public static final int ACTOR_PROPERTY_KEY_INDEX = 0;
    public static final int ACTOR_PROPERTY_POSITION_X_INDEX = 1;
    public static final int ACTOR_PROPERTY_POSITION_Y_INDEX = 2;
    public static final int ACTOR_PROPERTY_UPDATE_PERIOD_INDEX = 3;
    public static final int ACTOR_PROPERTY_COUNT = 4;


    /** An x/y position in the world. */
    private Point position;
    /** Inanimate (singular) or animation (multiple) image graphics. */
    private List<PImage> images;
    /** Index of the element from 'images' used to draw the actor. */
    private int imageIndex;
    /** Positive (non-zero) time delay between the actor's updates. */
    private double updatePeriod;
    /** Current water level. */


    // TODO: Remove (interfaces) or refactor with super (superclasses).

    public Actor( Point position, List<PImage> images, double updatePeriod) {
        this.position = position;
        this.images = images;
        this.imageIndex = 0;
        this.updatePeriod = updatePeriod;
    }

//

    // Regular Methods

    /** Searches the world for the first entity of a given kind.*/
    public static Optional<Actor> findByKind(World world, Class<?> actorKind) {

        for (int y = 0; y < world.getNumRows(); y++) {
            for (int x = 0; x < world.getNumCols(); x++) {
                Point point = new Point(x, y);

                Optional<Actor> potentialOccupant = world.getOccupant(point);
                if (potentialOccupant.isPresent()) {
                    Actor occupant = potentialOccupant.get();

                    if (actorKind.isInstance(occupant)) {
                        return potentialOccupant;
                    }
                }
            }
        }

        return Optional.empty();
    }

    /** Schedules the next update for the actor. */
    public void scheduleUpdate(World world, ImageLibrary imageLibrary, EventScheduler eventScheduler) {
        eventScheduler.scheduleEvent(this, new Update(this, world, imageLibrary), updatePeriod);
    }

    /** Calls the actor specific update. */
    public abstract void executeUpdate(World world, ImageLibrary imageLibrary, EventScheduler eventScheduler);


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

    public void setImageIndex(int imageIndex) {
        this.imageIndex = imageIndex;
    }
}
