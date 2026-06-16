import processing.core.PImage;

import java.util.List;

public abstract class EntityAnimation extends Entity {
    public  double animationPeriod;

    public double behaviorPeriod;

    public EntityAnimation(String id, Point position, List<PImage> images, double animationPeriod, double behaviorPeriod) {
        super(id, position, images);
        this.animationPeriod = animationPeriod;
        this.behaviorPeriod = behaviorPeriod;

    }
    public abstract void scheduleActions(EventScheduler scheduler, World world, ImageLibrary imageLibrary);

    public abstract void executeBehavior(World world, ImageLibrary imageLibrary, EventScheduler scheduler);
    public void scheduleBehavior(EventScheduler scheduler, World world, ImageLibrary imageLibrary) {
        scheduler.scheduleEvent(this, new Behavior(this, world, imageLibrary), behaviorPeriod);
    }

    public void scheduleAnimation(EventScheduler scheduler, World world, ImageLibrary imageLibrary) {
        scheduler.scheduleEvent(this, new Animation(this, 0), animationPeriod);
    }
    public double getAnimationPeriod() {
        return animationPeriod;
    }
    public double getBehaviorPeriod(){
        return behaviorPeriod;
    }

    public void setAnimationPeriod(double animationPeriod) {
        this.animationPeriod = animationPeriod;
    }

    public void setBehaviorPeriod(double behaviorPeriod) {
        this.behaviorPeriod = behaviorPeriod;
    }
}
