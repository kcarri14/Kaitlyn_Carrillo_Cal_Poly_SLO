import processing.core.PImage;

import java.util.*;
import java.util.function.BiPredicate;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Monkey extends EntityAnimation implements PathingStrategy {
    public static final String MONKEY_KEY = "monkey";
    protected Point lastTreePosition;

    public Monkey(String id, Point position, List<PImage> images, double animationPeriod, double behaviorPeriod) {
        super(id, position, images, animationPeriod, behaviorPeriod);
        this.lastTreePosition = null;
    }

    public void setLastTreePosition(Point lastTreePosition) {
        this.lastTreePosition = lastTreePosition;
    }


    @Override
    public void scheduleActions(EventScheduler scheduler, World world, ImageLibrary imageLibrary) {
        scheduler.scheduleEvent(this, new Animation(this, 0), animationPeriod);
        scheduler.scheduleEvent(this, new Behavior(this, world, imageLibrary), behaviorPeriod);
    }

    @Override
    public void executeBehavior(World world, ImageLibrary imageLibrary, EventScheduler scheduler) {
        Optional<Entity> monkeyTarget = world.findNearest(getPosition(), new ArrayList<>(List.of(Tree.class)));

        if (monkeyTarget.isPresent()) {
            Point tgtPos = monkeyTarget.get().getPosition();

            if (moveToMonkey(world, monkeyTarget.get(), scheduler)) {
                EntityAnimation banana = new Banana(Banana.BANANA_KEY + "_" + monkeyTarget.get().getId(), tgtPos, imageLibrary.get(Banana.BANANA_KEY), animationPeriod, behaviorPeriod);

                world.addEntity(banana);
                banana.scheduleActions(scheduler, world, imageLibrary);
            }
        }

        scheduleBehavior(scheduler, world, imageLibrary);
    }

    public List<Point> computePath(Point start, Point end, Predicate<Point> canPassThrough, BiPredicate<Point, Point> withinReach, Function<Point, Stream<Point>> potentialNeighbors) {
        // Use the A* algorithm to compute the path
        AStarPathingStrategy pathingStrategy = new AStarPathingStrategy();
        return pathingStrategy.computePath(start, end, canPassThrough, withinReach, potentialNeighbors);
    }


    public boolean moveToMonkey(World world, Entity target, EventScheduler scheduler) {
        if (getPosition().adjacentTo(target.getPosition())) {
            if (target instanceof Tree) {
                world.removeEntity(scheduler, target);
            }
            return true;
        } else {
            Point nextPos = nextPositionMonkey(world, target.getPosition());
            if (!getPosition().equals(nextPos)) {
                world.moveEntity(scheduler, this, nextPos);
            }
            return false;
        }
    }
    public Point nextPositionMonkey(World world, Point destination) {
        // Define the canPassThrough predicate
        PathingStrategy pathingStrategy = new AStarPathingStrategy();
        Predicate<Point> canPassThrough = point ->  world.inBounds(point) && !world.isOccupied(point) || world.getOccupant(point).isPresent() && world.getOccupant(point).get() instanceof Stump ;

        // Define the withinReach predicate
        BiPredicate<Point, Point> withinReach = (point1, point2) -> point1.adjacentTo(point2);

        // Get all trees in the world
        List<Entity> trees = world.getEntities().stream()
                .filter(entity -> entity instanceof Tree)
                .toList();

        if (!trees.isEmpty()) {
            // Find the nearest tree using A*
            Entity nearestTree = null;
            double minDistance = Double.MAX_VALUE;
            List<Point> bestPath = null;

            for (Entity tree : trees) {
                List<Point> path = pathingStrategy.computePath(
                        getPosition(), tree.getPosition(), canPassThrough, withinReach, PathingStrategy.CARDINAL_NEIGHBORS);

                if (path != null && !path.isEmpty()) {
                    double distance = path.size(); // Assuming each step has a cost of 1
                    if (distance < minDistance) {
                        minDistance = distance;
                        nearestTree = tree;
                        bestPath = path;
                    }
                }
            }

            if (nearestTree != null && bestPath != null && !bestPath.isEmpty()) {
                return bestPath.get(0); // Return the next position in the path
            }
        }

        // If no trees found or path to any tree not found, return the current position
        return getPosition();
    }






    public void updateImage(){
        setImageIndex(getImageIndex() + 1);
    }
}