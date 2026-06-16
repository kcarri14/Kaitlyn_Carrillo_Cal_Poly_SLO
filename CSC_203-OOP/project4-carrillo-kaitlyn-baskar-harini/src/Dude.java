import processing.core.PImage;

import java.util.List;
import java.util.Optional;
import java.util.function.BiPredicate;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Stream;

public class Dude extends EntityAnimation implements PathingStrategy{
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
        if (dudeTarget.isEmpty() || !moveToDude(world, dudeTarget.get(), scheduler, imageLibrary) || !transformDude(world, scheduler, imageLibrary) || dudeTouchBanana(world, dudeTarget.get(), scheduler, imageLibrary)) {
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
    public boolean moveToDude(World world, Entity target, EventScheduler scheduler, ImageLibrary imageLibrary) {
        if (getPosition().adjacentTo(target.getPosition())) {
            if (target instanceof Tree tree) {
                tree.setHealth(tree.getHealth() - 1);
            }
            if (target instanceof Sapling sapling) {
                sapling.setHealth(sapling.getHealth() - 1);
            }
            if (target instanceof Banana banana){
                dudeTouchBanana(world, banana, scheduler, imageLibrary);
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
    public boolean dudeTouchBanana(World world, Entity target, EventScheduler scheduler, ImageLibrary imageLibrary ){
        if (target instanceof Banana) {
            EntityAnimation dude = new Dude(getId(), getPosition(), imageLibrary.get(DUDE_KEY), animationPeriod , behaviorPeriod  , resourceCount , resourceLimit + 1);

            world.removeEntity(scheduler, this);

            world.addEntity(dude);
            dude.scheduleActions(scheduler, world, imageLibrary);
        }
        return true;
    }
    /** Determines a Dude's next position when moving. */
    public Point nextPositionDude(World world, Point destination) {
        PathingStrategy pathingStrategy = new AStarPathingStrategy();
        Predicate<Point> canPassThrough = point -> world.inBounds(point) && !world.isOccupied(point) || world.getOccupant(point).isPresent() && world.getOccupant(point).get() instanceof Stump ;;
        BiPredicate<Point, Point> withinReach = (p1, p2) -> Math.abs(p1.x -p2.x) + Math.abs(p1.y - p2.y) == 1;
        List<Point> path = pathingStrategy.computePath(getPosition(), destination, canPassThrough, withinReach, CARDINAL_NEIGHBORS);

        if (path.isEmpty()) {
           return getPosition();
        } else {
            return path.get(0);
        }

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

        } else
        {
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

    public void setResourceLimit(int resourceLimit) {
        this.resourceLimit = resourceLimit;
    }

    public int getResourceLimit() {
        return resourceLimit;
    }

    @Override
    public List<Point> computePath(Point start, Point end, Predicate<Point> canPassThrough, BiPredicate<Point, Point> withinReach, Function<Point, Stream<Point>> potentialNeighbors) {
        return null;
    }

}
