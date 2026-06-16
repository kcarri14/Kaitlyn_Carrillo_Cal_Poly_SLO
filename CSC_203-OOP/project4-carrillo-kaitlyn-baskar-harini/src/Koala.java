import processing.core.PImage;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.function.BiPredicate;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Stream;

public class Koala extends EntityAnimation implements PathingStrategy{
    public static final String KOALA_KEY = "koala";
    public Koala(String id, Point position, List<PImage> images, double animationPeriod, double behaviorPeriod) {
        super(id, position, images, animationPeriod, behaviorPeriod);
    }

    @Override
    public void scheduleActions(EventScheduler scheduler, World world, ImageLibrary imageLibrary) {
        scheduler.scheduleEvent(this, new Animation(this, 0), animationPeriod);
        scheduler.scheduleEvent(this, new Behavior(this, world, imageLibrary), behaviorPeriod);
    }

    @Override
    public void executeBehavior(World world, ImageLibrary imageLibrary, EventScheduler scheduler) {
        Optional<Entity> koalaTarget = world.findNearest(getPosition(), new ArrayList<>(List.of(bananaSplit.class)));

        if (koalaTarget.isPresent()) {
            Point tgtPos = koalaTarget.get().getPosition();

            if (moveToKoala(world, koalaTarget.get(), scheduler)) {
                EntityAnimation tree =  new Tree(Tree.TREE_KEY + "_" + koalaTarget.get().getId(),tgtPos, imageLibrary.get(Tree.TREE_KEY), NumberUtil.getRandomDouble(0.1, 1.0), NumberUtil.getRandomDouble(0.01, 0.10), NumberUtil.getRandomInt(1, 3));

                world.addEntity(tree);
                tree.scheduleActions(scheduler, world, imageLibrary);
            }
        }

        scheduleBehavior(scheduler, world, imageLibrary);
    }

    @Override
    public List<Point> computePath(Point start, Point end, Predicate<Point> canPassThrough, BiPredicate<Point, Point> withinReach, Function<Point, Stream<Point>> potentialNeighbors) {
        return null;
    }

    public boolean moveToKoala(World world, Entity target, EventScheduler scheduler) {
        if (getPosition().adjacentTo(target.getPosition())) {
            world.removeEntity(scheduler, target);
            return true;
        } else {
            Point nextPos = nextPositionKoala(world, target.getPosition());
            if (!getPosition().equals(nextPos)) {
                world.moveEntity(scheduler, this, nextPos);
            }
            return false;
        }
    }
    public Point nextPositionKoala(World world, Point destination) {
        PathingStrategy pathingStrategy = new AStarPathingStrategy();
        Predicate<Point> canPassThrough = point -> world.inBounds(point) && !world.isOccupied(point) || world.getOccupant(point).isPresent() && world.getOccupant(point).get() instanceof Banana;
        BiPredicate<Point, Point> withinReach = (p1, p2) -> Math.abs(p1.x -p2.x) + Math.abs(p1.y - p2.y) == 1;
        List<Point> path = pathingStrategy.computePath(getPosition(), destination, canPassThrough, withinReach, CARDINAL_NEIGHBORS);

        if (path.isEmpty()) {
            return getPosition();
        } else {
            return path.get(0);
        }
    }
    public void updateImage(){
        setImageIndex(getImageIndex() + 1);
    }
}
