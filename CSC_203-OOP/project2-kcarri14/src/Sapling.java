import processing.core.PImage;

import java.util.List;

public class Sapling extends EntityAnimation {
    public static final String SAPLING_KEY = "sapling";
    public static final int SAPLING_PARSE_PROPERTY_COUNT = 0;
    public static final int SAPLING_HEALTH_LIMIT = 5;
    public static final double SAPLING_BEHAVIOR_PERIOD = 2.0;
    public static final double SAPLING_ANIMATION_PERIOD = 0.0125; // Very small to react to health changes
    private int health;

    public Sapling(String id, Point position, List<PImage> images) {
        super(id, position, images, SAPLING_ANIMATION_PERIOD, SAPLING_BEHAVIOR_PERIOD);
    }

    public void scheduleActions(EventScheduler scheduler, World world, ImageLibrary imageLibrary) {
        scheduler.scheduleEvent(this, new Animation(this, 0), SAPLING_ANIMATION_PERIOD );
        scheduler.scheduleEvent(this, new Behavior(this, world, imageLibrary), SAPLING_BEHAVIOR_PERIOD);
    }

    /** Executes Sapling specific Logic. */
    public void executeBehavior(World world, ImageLibrary imageLibrary, EventScheduler scheduler) {
        health = health + 1;
        if (!transformSapling(world, scheduler, imageLibrary)) {
            scheduleBehavior(scheduler, world, imageLibrary);
        }
    }

    /** Checks the Sapling's health and transforms accordingly, returning true if successful. */
    public boolean transformSapling(World world, EventScheduler scheduler, ImageLibrary imageLibrary) {
        if (health <= 0) {
            Entity stump =  new Stump(Stump.STUMP_KEY + "_" + getId(), getPosition(), imageLibrary.get(Stump.STUMP_KEY));

            world.removeEntity(scheduler, this);

            world.addEntity(stump);

            return true;
        } else if (health >= SAPLING_HEALTH_LIMIT) {
            EntityAnimation tree =  new Tree(Tree.TREE_KEY + "_" + getId(),getPosition(), imageLibrary.get(Tree.TREE_KEY), NumberUtil.getRandomDouble(0.1, 1.0), NumberUtil.getRandomDouble(0.01, 0.10), NumberUtil.getRandomInt(1, 3));

            world.removeEntity(scheduler, this);

            world.addEntity(tree);
            tree.scheduleActions(scheduler, world, imageLibrary);

            return true;
        }

        return false;
    }

    public void updateImage(){
        if (health <= 0) {
            setImageIndex(0);
        } else if (health < SAPLING_HEALTH_LIMIT) {
            setImageIndex(getImages().size() * health / SAPLING_HEALTH_LIMIT);
        } else {
            setImageIndex(getImages().size() - 1);
        }
    }
    public int getHealth(){
        return health;
    }

    public void setHealth(int health){
        this.health = health;
    }
}
