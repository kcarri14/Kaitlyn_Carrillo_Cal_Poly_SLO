import java.util.*;
import java.util.function.BiPredicate;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Stream;

public class AStarPathingStrategy implements PathingStrategy {

    /**
     * Return a list containing a single point representing the next step toward a goal
     * If the start is within reach of the goal, the returned list is empty.
     *
     * @param start the point to begin the search from
     * @param end the point to search for a point within reach of
     * @param canPassThrough a function that returns true if the given point is traversable
     * @param withinReach a function that returns true if both points are within reach of each other
     * @param potentialNeighbors a function that returns the neighbors of a given point, as a stream
     */

    public List<Point> computePath(
            Point start,
            Point end,
            Predicate<Point> canPassThrough,
            BiPredicate<Point, Point> withinReach,
            Function<Point, Stream<Point>> potentialNeighbors
    ) {
        List<Point> openSet = new ArrayList<>();
        Set<Point> closedSet = new HashSet<>();
        Map<Point, Point> cameFrom = new HashMap<>();
        Map<Point, Integer> gscore = new HashMap<>();
        Map<Point, Integer> fscore = new HashMap<>();

        gscore.put(start, 0);
        fscore.put(start, hscore(start, end));
        openSet.add(start);


        while (!openSet.isEmpty()) {
            Point current = openSet.stream().min(Comparator.comparingInt(fscore::get)).orElseThrow();
            openSet.remove(current);
            closedSet.add(current);

            if (withinReach.test(current, end)) {
                cameFrom.put(end, current);
                return reconstructpath(cameFrom, end, start);
            }


            List<Point> neighbors = potentialNeighbors.apply(current)
                    .filter(canPassThrough).toList();

            for (Point neighbor : neighbors) {
                if (closedSet.contains(neighbor)) {
                    continue;
                }
                if (!openSet.contains(neighbor)) {
                    openSet.add(neighbor);
                }

                int tentative_gscore = gscore.getOrDefault(current, Integer.MAX_VALUE) + 1;

                if (tentative_gscore < gscore.getOrDefault(neighbor, Integer.MAX_VALUE)) {
                    cameFrom.put(neighbor, current);
                    gscore.put(neighbor, tentative_gscore);
                    fscore.put(neighbor, tentative_gscore + hscore(neighbor, end));

                }
            }
        }
        return List.of();
    }

    private int hscore(Point a, Point b) {
        return Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
    }

    private List<Point> reconstructpath(Map<Point, Point> cameFrom, Point current, Point start) {
        List<Point> totalpath = new ArrayList<>();
        while (!current.equals(start)) {
            totalpath.add(current);
            current = cameFrom.get(current);
            if (current == null) {
                break;
            }
        }
        Collections.reverse(totalpath);
        return totalpath;
    }
}


