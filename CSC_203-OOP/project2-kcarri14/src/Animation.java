public class Animation extends Action {

    public Animation(EntityAnimation entity, int repeatCount) {
        super(entity, null , null, repeatCount);
    }

    public void execute(EventScheduler scheduler) {
        getEntity().updateImage();

        if (getRepeatCount() != 1) {
            Animation animationEvent = new Animation(getEntity(), Math.max(this.getRepeatCount() - 1, 0));
            scheduler.scheduleEvent(getEntity(), animationEvent, getEntity().getAnimationPeriod());
        }
    }
}
