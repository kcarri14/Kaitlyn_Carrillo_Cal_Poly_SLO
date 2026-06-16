import processing.core.PImage;

import java.util.List;
import java.util.Optional;

public class Dude extends EntityAnimation {
    public static final String DUDE_KEY = "dude";
    public static final int DUDE_PARSE_PROPERTY_ANIMATION_PERIOD_INDEX = 0;
    public static final int DUDE_PARSE_PROPERTY_BEHAVIOR_PERIOD_INDEX = 1;
    public static final int DUDE_PARSE_PROPERTY_RESOURCE_LIMIT_INDEX = 2;
    public static final int DUDE_PARSE_PROPERTY_COUNT = 3;
    private int resourceCount;

    private int resourceLimit;



    public Dude(String id, Point position, List<PImage> images, double animationPeriod, double behaviorPeriod, int resourceCount, int resourceLimit) {
        super(id, position, images, animationPeriod, behaviorPeriod);
        this.resourceCount = resourceCount;
        this.resourceLimit = resourceLimit;
    }

    public void scheduleActions(EventScheduler scheduler, World world, ImageLibrary imageLibrary) {
        scheduler.scheduleEvent(this, new Animation(this, 0), animationPeriod);
        scheduler.scheduleEvent(this, new Behavior(this, world, imageLibrary), behaviorPeriod);
    }

    /** Executes Dude specific Logic. */
    public void executeBehavior(World world, ImageLibrary imageLibrary, EventScheduler scheduler) {
        Optional<Entity> dudeTarget = findDudeTarget(world);
        if (dudeTarget.isEmpty() || !moveToDude(world, dudeTarget.get(), scheduler) || !transformDude(world, scheduler, imageLibrary)) {
            scheduleBehavior(scheduler, world, imageLibrary);
        }
    }

    /** Returns the (optional) entity a Dude will path toward. */
    public Optional<Entity> findDudeTarget(World world) {
        List<Class<?>> potentialTargets;

        if (resourceCount == resourceLimit) {
            potentialTargets = List.of(House.class);
        } else {
            potentialTargets = List.of(Tree.class, Sapling.class);
        }

        return world.findNearest(getPosition(), potentialTargets);
    }

    /** Attempts to move the Dude toward a target, returning True if already adjacent to it. */
    public boolean moveToDude(World world, Entity target, EventScheduler scheduler) {
        if (getPosition().adjacentTo(target.getPosition())) {
            if (target instanceof Tree tree) {
                tree.setHealth(tree.getHealth() - 1);
            }
            if (target instanceof Sapling sapling) {
                sapling.setHealth(sapling.getHealth() - 1);
            }
            return true;
        } else {
            Point nextPos = nextPositionDude(world, target.getPosition());

            if (!getPosition().equals(nextPos)) {
                world.moveEntity(scheduler, this, nextPos);
            }

            return false;
        }
    }

    /** Determines a Dude's next position when moving. */
    public Point nextPositionDude(World world, Point destination) {
        // Differences between the destination and current position along each axis
        int deltaX = destination.x - getPosition().x;
        int deltaY = destination.y - getPosition().y;

        // Positions one step toward the destination along each axis
        Point horizontalPosition = new Point(getPosition().x + Integer.signum(deltaX), getPosition().y);
        Point verticalPosition = new Point(getPosition().x, getPosition().y + Integer.signum(deltaY));

        // Assumes all destinations are within bounds of the world
        // If this is not the case, also check 'World.inBounds()'
        boolean horizontalOccupied = world.isOccupied(horizontalPosition) && !(world.getOccupant(horizontalPosition).get() instanceof Stump);
        boolean verticalOccupied = world.isOccupied(verticalPosition) && !(world.getOccupant(verticalPosition).get() instanceof Stump);

        // Move along the farther direction, preferring horizontal
        if (Math.abs(deltaX) >= Math.abs(deltaY)) {
            if (!horizontalOccupied) {
                return horizontalPosition;
            } else if (!verticalOccupied) {
                return verticalPosition;
            }
        } else {
            if (!verticalOccupied) {
                return verticalPosition;
            } else if (!horizontalOccupied) {
                return horizontalPosition;
            }
        }

        return getPosition();
    }

    /** Changes the Dude's graphics. */
    public boolean transformDude(World world, EventScheduler scheduler, ImageLibrary imageLibrary) {
        if (resourceCount < resourceLimit) {
            resourceCount += 1;
            if (resourceCount == resourceLimit) {
                EntityAnimation dude = new Dude(getId(), getPosition(), imageLibrary.get(DUDE_KEY + "_carry"), animationPeriod, behaviorPeriod, resourceCount, resourceLimit);

                world.removeEntity(scheduler, this);

                world.addEntity(dude);
                dude.scheduleActions(scheduler, world, imageLibrary);

                return true;
            }
        } else {
            EntityAnimation dude = new Dude(getId(), getPosition(), imageLibrary.get(DUDE_KEY), animationPeriod, behaviorPeriod, 0, resourceLimit);

            world.removeEntity(scheduler, this);

            world.addEntity(dude);
            dude.scheduleActions(scheduler, world, imageLibrary);

            return true;
        }

        return false;
    }
public void updateImage(){
    setImageIndex(getImageIndex() + 1);
}

}
