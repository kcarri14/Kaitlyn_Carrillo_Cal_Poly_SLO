import processing.core.PImage;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class Banana extends EntityAnimation{
    public static final String BANANA_KEY = "banana";
    public static final int BANANA_PARSE_PROPERTY_ANIMATION_PERIOD_INDEX = 0;
    public static final int BANANA_PARSE_PROPERTY_BEHAVIOR_PERIOD_INDEX = 1;

    public Banana(String id, Point position, List<PImage> images, double animationPeriod, double behaviorPeriod) {
        super(id, position, images, animationPeriod, behaviorPeriod);
    }

    @Override
    public void scheduleActions(EventScheduler scheduler, World world, ImageLibrary imageLibrary) {
        scheduler.scheduleEvent(this, new Animation(this, 0), getAnimationPeriod());
        scheduler.scheduleEvent(this, new Behavior(this, world, imageLibrary), getBehaviorPeriod());
    }

    @Override
   public void executeBehavior(World world, ImageLibrary imageLibrary, EventScheduler scheduler) {
        Optional<Entity> bananaTarget = world.findNearest(getPosition(), new ArrayList<>(List.of(Dude.class)));
        if (!transformBanana(world, (EntityAnimation) bananaTarget.get(), scheduler, imageLibrary)) {
            scheduleBehavior(scheduler, world, imageLibrary);
        }
    }
    public boolean transformBanana(World world, EntityAnimation target, EventScheduler scheduler, ImageLibrary imageLibrary) {
        if (getPosition().adjacentTo(target.getPosition())) {
            target.setAnimationPeriod(getAnimationPeriod() - 0.8);;
            target.setBehaviorPeriod(getBehaviorPeriod() + 0.1625);;
            if (target instanceof Dude){
                ((Dude) target).setResourceLimit(((Dude)target).getResourceLimit() + 1);
            }
            Entity bananasplit = new bananaSplit("bananaSplit.BANANA_SPLIT_KEY", getPosition(), imageLibrary.get("banana_split"));

            world.removeEntity(scheduler, this);

            world.addEntity(bananasplit);

            return true;
        }

        return false;
    }
    public void updateImage(){
        setImageIndex(getImageIndex() + 1);
    }
}
